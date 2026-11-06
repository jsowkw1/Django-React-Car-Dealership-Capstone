import json
import logging
import re
from datetime import date

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from . import restapis
from .models import CarMake, CarModel
from .populate import initiate

logger = logging.getLogger(__name__)
USERNAME_RE = re.compile(r'^[\w.@+-]{3,150}$')


def error(status, message, **extra):
    return JsonResponse({'status': status, 'error': message, **extra}, status=status)


def parse_json(request):
    try:
        data = json.loads(request.body or b'{}')
    except (ValueError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def backend_call(func, *args, **kwargs):
    """Runs a call to the Express service, translating its errors to JSON responses."""
    try:
        return func(*args, **kwargs), None
    except restapis.BackendError as exc:
        return None, error(exc.status, exc.message)


@ensure_csrf_cookie
def frontend(request, *args, **kwargs):
    index = settings.FRONTEND_DIST / 'index.html'
    if not index.exists():
        return HttpResponse(
            '<h1>Frontend not built</h1><p>Run <code>npm run build</code> in <code>frontend/</code>.</p>',
            status=503,
        )
    return render(request, 'index.html')


# ---------- Authentication ----------

def user_payload(user):
    if not user.is_authenticated:
        return {'userName': '', 'isAuthenticated': False}
    return {
        'userName': user.username,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'email': user.email,
        'isStaff': user.is_staff,
        'isAuthenticated': True,
    }


@require_GET
@ensure_csrf_cookie
def current_user(request):
    return JsonResponse(user_payload(request.user))


@require_POST
def login_user(request):
    data = parse_json(request)
    if data is None:
        return error(400, 'Invalid JSON body')
    username = str(data.get('userName', '')).strip()
    password = str(data.get('password', ''))
    if not username or not password:
        return error(400, 'Username and password are required')
    user = authenticate(request, username=username, password=password)
    if user is None:
        return error(401, 'Invalid username or password', userName=username)
    login(request, user)
    return JsonResponse({'userName': username, 'status': 'Authenticated', 'user': user_payload(user)})


@require_POST
def logout_user(request):
    username = request.user.username if request.user.is_authenticated else ''
    logout(request)
    return JsonResponse({'userName': '', 'loggedOut': username, 'status': 'Logged out'})


@require_POST
def registration(request):
    data = parse_json(request)
    if data is None:
        return error(400, 'Invalid JSON body')
    username = str(data.get('userName', '')).strip()
    first_name = str(data.get('firstName', '')).strip()
    last_name = str(data.get('lastName', '')).strip()
    email = str(data.get('email', '')).strip()
    password = str(data.get('password', ''))

    errors = {}
    if not USERNAME_RE.match(username):
        errors['userName'] = 'Username must be 3-150 characters: letters, digits and @/./+/-/_ only'
    elif User.objects.filter(username__iexact=username).exists():
        errors['userName'] = 'Already Registered'
    if not first_name:
        errors['firstName'] = 'First name is required'
    if not last_name:
        errors['lastName'] = 'Last name is required'
    try:
        validate_email(email)
        if User.objects.filter(email__iexact=email).exists():
            errors['email'] = 'This email is already registered'
    except ValidationError:
        errors['email'] = 'Enter a valid email address'
    try:
        validate_password(password, User(username=username, first_name=first_name, last_name=last_name, email=email))
    except ValidationError as exc:
        errors['password'] = ' '.join(exc.messages)
    if errors:
        message = 'Already Registered' if errors.get('userName') == 'Already Registered' else 'Please correct the errors below'
        return error(400, message, errors=errors, userName=username)

    user = User.objects.create_user(
        username=username, first_name=first_name, last_name=last_name, email=email, password=password
    )
    login(request, user)
    return JsonResponse(
        {'userName': username, 'status': 'Authenticated', 'user': user_payload(user)}, status=201
    )


# ---------- Dealers and reviews (proxied to the Express API) ----------

@require_GET
def get_dealerships(request, state='All'):
    endpoint = '/fetchDealers' if state in ('', 'All') else f'/fetchDealers/{state}'
    dealers, err = backend_call(restapis.get_request, endpoint)
    if err:
        return err
    return JsonResponse({'status': 200, 'count': len(dealers), 'dealers': dealers})


@require_GET
def get_dealer_details(request, dealer_id):
    dealer, err = backend_call(restapis.get_request, f'/fetchDealer/{dealer_id}')
    if err:
        return err
    return JsonResponse({'status': 200, 'dealer': dealer})


@require_GET
def get_dealer_reviews(request, dealer_id):
    reviews, err = backend_call(restapis.get_request, f'/fetchReviews/dealer/{dealer_id}')
    if err:
        return err
    for review in reviews:
        if not review.get('sentiment'):
            review['sentiment'] = restapis.analyze_review_sentiments(review['review']).get('sentiment', 'neutral')
    ratings = [r['rating'] for r in reviews if r.get('rating')]
    average = round(sum(ratings) / len(ratings), 1) if ratings else None
    return JsonResponse({'status': 200, 'count': len(reviews), 'average_rating': average, 'reviews': reviews})


@require_POST
def add_review(request):
    if not request.user.is_authenticated:
        return error(401, 'You must be logged in to post a review')
    data = parse_json(request)
    if data is None:
        return error(400, 'Invalid JSON body')

    errors = {}
    review_text = str(data.get('review', '')).strip()
    if len(review_text) < 5:
        errors['review'] = 'Review must be at least 5 characters'
    try:
        rating = int(data.get('rating'))
        if not 1 <= rating <= 5:
            raise ValueError
    except (TypeError, ValueError):
        errors['rating'] = 'Choose a rating from 1 to 5'
        rating = None
    try:
        dealer_id = int(data.get('dealership'))
    except (TypeError, ValueError):
        errors['dealership'] = 'Dealer is required'
        dealer_id = None
    purchase_date = str(data.get('purchase_date', '')).strip()
    if purchase_date:
        try:
            if date.fromisoformat(purchase_date) > date.today():
                errors['purchase_date'] = 'Purchase date cannot be in the future'
        except ValueError:
            errors['purchase_date'] = 'Use the YYYY-MM-DD format'
    car_make, car_model, car_year = '', '', None
    car_id = data.get('car_id')
    if car_id:
        car = CarModel.objects.select_related('car_make').filter(pk=car_id).first()
        if car is None:
            errors['car'] = 'Unknown car model'
        else:
            car_make, car_model, car_year = car.car_make.name, car.name, car.year
    else:
        car_make = str(data.get('car_make', '')).strip()
        car_model = str(data.get('car_model', '')).strip()
        car_year = data.get('car_year') or None
    if errors:
        return error(400, 'Please correct the errors below', errors=errors)

    user = request.user
    payload = {
        'name': user.get_full_name() or user.username,
        'dealership': dealer_id,
        'review': review_text,
        'purchase': bool(data.get('purchase')),
        'purchase_date': purchase_date,
        'car_make': car_make,
        'car_model': car_model,
        'car_year': car_year,
        'rating': rating,
    }
    saved, err = backend_call(restapis.post_review, payload)
    if err:
        return err
    return JsonResponse({'status': 201, 'message': 'Review posted', 'review': saved}, status=201)


@require_GET
def analyze_sentiment(request, text):
    return JsonResponse(restapis.analyze_review_sentiments(text))


# ---------- Car makes and models ----------

def ensure_cars():
    if not CarMake.objects.exists():
        initiate()


@require_GET
def get_cars(request):
    ensure_cars()
    car_models = CarModel.objects.select_related('car_make')
    return JsonResponse({
        'status': 200,
        'count': car_models.count(),
        'CarModels': [
            {'id': c.id, 'CarModel': c.name, 'CarMake': c.car_make.name, 'type': c.type, 'year': c.year,
             'dealer_id': c.dealer_id}
            for c in car_models
        ],
    }, json_dumps_params={'indent': 2})


@require_GET
def get_car_makes(request):
    ensure_cars()
    makes = CarMake.objects.prefetch_related('models')
    return JsonResponse({
        'status': 200,
        'count': makes.count(),
        'CarMakes': [
            {'id': m.id, 'name': m.name, 'country': m.country, 'founded': m.founded,
             'description': m.description, 'models': sorted({c.name for c in m.models.all()})}
            for m in makes
        ],
    }, json_dumps_params={'indent': 2})


@require_GET
def get_car_models(request):
    ensure_cars()
    car_models = CarModel.objects.select_related('car_make')
    make = request.GET.get('make')
    if make:
        car_models = car_models.filter(car_make__name__iexact=make)
    return JsonResponse({
        'status': 200,
        'count': car_models.count(),
        'CarModels': [
            {'id': c.id, 'name': c.name, 'make': c.car_make.name, 'type': c.get_type_display(),
             'year': c.year, 'dealer_id': c.dealer_id}
            for c in car_models
        ],
    }, json_dumps_params={'indent': 2})
