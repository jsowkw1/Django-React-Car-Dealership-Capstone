import json
from io import StringIO
from unittest import mock

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client, TestCase

from djangoapp import restapis
from djangoapp.models import CarMake, CarModel

DEALER = {'id': 1, 'full_name': 'Sunflower State Motors', 'city': 'Wichita', 'state': 'Kansas', 'st': 'KS'}
REVIEWS = [
    {'id': 2, 'dealership': 1, 'review': 'Great staff', 'rating': 5, 'sentiment': 'positive'},
    {'id': 1, 'dealership': 1, 'review': 'Okay', 'rating': 3},
]


def post_json(client, url, data):
    return client.post(url, json.dumps(data), content_type='application/json')


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user('alice', email='alice@example.com', password='Str0ng-Passw0rd!')

    def test_register_creates_user_and_logs_in(self):
        res = post_json(self.client, '/djangoapp/register', {
            'userName': 'bob99', 'firstName': 'Bob', 'lastName': 'Stone',
            'email': 'bob@example.com', 'password': 'Secur3-Pa55word',
        })
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()['status'], 'Authenticated')
        user = User.objects.get(username='bob99')
        self.assertTrue(user.check_password('Secur3-Pa55word'))
        self.assertNotEqual(user.password, 'Secur3-Pa55word')  # stored hashed
        self.assertTrue(self.client.get('/djangoapp/me').json()['isAuthenticated'])

    def test_register_validation_errors(self):
        res = post_json(self.client, '/djangoapp/register', {
            'userName': 'alice', 'firstName': '', 'lastName': '', 'email': 'nope', 'password': '123',
        })
        self.assertEqual(res.status_code, 400)
        errors = res.json()['errors']
        self.assertEqual(set(errors), {'userName', 'firstName', 'lastName', 'email', 'password'})
        self.assertEqual(res.json()['error'], 'Already Registered')

    def test_login_success_and_failure(self):
        bad = post_json(self.client, '/djangoapp/login', {'userName': 'alice', 'password': 'wrong'})
        self.assertEqual(bad.status_code, 401)
        ok = post_json(self.client, '/djangoapp/login', {'userName': 'alice', 'password': 'Str0ng-Passw0rd!'})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ok.json()['userName'], 'alice')
        self.assertEqual(self.client.get('/djangoapp/me').json()['userName'], 'alice')

    def test_login_rejects_bad_json(self):
        res = self.client.post('/djangoapp/login', 'not json', content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_logout(self):
        self.client.login(username='alice', password='Str0ng-Passw0rd!')
        res = self.client.post('/djangoapp/logout')
        self.assertEqual(res.json()['loggedOut'], 'alice')
        self.assertFalse(self.client.get('/djangoapp/me').json()['isAuthenticated'])

    def test_csrf_is_enforced(self):
        client = Client(enforce_csrf_checks=True)
        res = post_json(client, '/djangoapp/login', {'userName': 'alice', 'password': 'Str0ng-Passw0rd!'})
        self.assertEqual(res.status_code, 403)
        client.get('/djangoapp/me')
        token = client.cookies['csrftoken'].value
        res = client.post('/djangoapp/login', json.dumps({'userName': 'alice', 'password': 'Str0ng-Passw0rd!'}),
                          content_type='application/json', HTTP_X_CSRFTOKEN=token)
        self.assertEqual(res.status_code, 200)


class DealerProxyTests(TestCase):
    @mock.patch('djangoapp.restapis.get_request', return_value=[DEALER])
    def test_get_dealers(self, get):
        res = self.client.get('/djangoapp/get_dealers')
        self.assertEqual(res.json()['count'], 1)
        get.assert_called_with('/fetchDealers')

    @mock.patch('djangoapp.restapis.get_request', return_value=[DEALER])
    def test_get_dealers_by_state(self, get):
        res = self.client.get('/djangoapp/get_dealers/Kansas')
        self.assertEqual(res.status_code, 200)
        get.assert_called_with('/fetchDealers/Kansas')

    @mock.patch('djangoapp.restapis.get_request', return_value=DEALER)
    def test_dealer_details(self, get):
        res = self.client.get('/djangoapp/dealer/1')
        self.assertEqual(res.json()['dealer']['full_name'], 'Sunflower State Motors')

    @mock.patch('djangoapp.restapis.get_request', side_effect=restapis.BackendError(404, 'Dealer 99 not found'))
    def test_dealer_not_found(self, get):
        res = self.client.get('/djangoapp/dealer/99')
        self.assertEqual(res.status_code, 404)

    @mock.patch('djangoapp.restapis.get_request', side_effect=restapis.BackendError(503, 'Dealer service is unavailable'))
    def test_backend_unavailable(self, get):
        self.assertEqual(self.client.get('/djangoapp/get_dealers').status_code, 503)

    @mock.patch('djangoapp.restapis.analyze_review_sentiments', return_value={'sentiment': 'neutral'})
    @mock.patch('djangoapp.restapis.get_request', return_value=[dict(r) for r in REVIEWS])
    def test_reviews_get_sentiment_and_average(self, get, analyze):
        body = self.client.get('/djangoapp/reviews/dealer/1').json()
        self.assertEqual(body['count'], 2)
        self.assertEqual(body['average_rating'], 4.0)
        self.assertEqual([r['sentiment'] for r in body['reviews']], ['positive', 'neutral'])
        analyze.assert_called_once_with('Okay')


class AddReviewTests(TestCase):
    def setUp(self):
        call_command('seed_demo', stdout=StringIO())
        self.user = User.objects.create_user('carol', first_name='Carol', last_name='King',
                                             password='Str0ng-Passw0rd!')
        self.car = CarModel.objects.get(car_make__name='Toyota', name='Camry')
        self.review = {'dealership': 1, 'review': 'Fantastic services', 'rating': 5, 'purchase': True,
                       'purchase_date': '2026-01-15', 'car_id': self.car.id}

    def test_requires_login(self):
        res = post_json(self.client, '/djangoapp/add_review', self.review)
        self.assertEqual(res.status_code, 401)

    @mock.patch('djangoapp.restapis.post_review')
    def test_posts_review_to_express(self, post):
        post.return_value = {'id': 15, 'name': 'Carol King', 'sentiment': 'positive'}
        self.client.force_login(self.user)
        res = post_json(self.client, '/djangoapp/add_review', self.review)
        self.assertEqual(res.status_code, 201)
        sent = post.call_args.args[0]
        self.assertEqual(sent['name'], 'Carol King')
        self.assertEqual((sent['car_make'], sent['car_model'], sent['car_year']), ('Toyota', 'Camry', 2025))
        self.assertEqual(sent['rating'], 5)

    def test_validation(self):
        self.client.force_login(self.user)
        res = post_json(self.client, '/djangoapp/add_review',
                        {'dealership': 1, 'review': '', 'rating': 7, 'purchase_date': '2999-01-01'})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(set(res.json()['errors']), {'review', 'rating', 'purchase_date'})


class CarTests(TestCase):
    def test_get_cars_populates_and_lists(self):
        body = self.client.get('/djangoapp/get_cars').json()
        self.assertGreaterEqual(body['count'], 20)
        self.assertIn({'CarModel': 'Camry', 'CarMake': 'Toyota'},
                      [{'CarModel': c['CarModel'], 'CarMake': c['CarMake']} for c in body['CarModels']])

    def test_car_makes_and_filtered_models(self):
        makes = self.client.get('/djangoapp/get_car_makes').json()
        names = {m['name'] for m in makes['CarMakes']}
        self.assertTrue({'Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes-Benz', 'Nissan'} <= names)
        models = self.client.get('/djangoapp/get_car_models?make=bmw').json()
        self.assertTrue(models['count'] >= 3 and all(m['make'] == 'BMW' for m in models['CarModels']))

    def test_seed_is_idempotent(self):
        call_command('seed_demo', stdout=StringIO())
        count = CarModel.objects.count()
        call_command('seed_demo', stdout=StringIO())
        self.assertEqual(CarModel.objects.count(), count)
        self.assertTrue(User.objects.get(username='root').is_superuser)
        self.assertEqual(CarMake.objects.count(), 8)


class SentimentClientTests(TestCase):
    @mock.patch('djangoapp.restapis.requests.get')
    def test_analyze_url_encodes_text(self, get):
        get.return_value.status_code = 200
        get.return_value.json.return_value = {'sentiment': 'positive'}
        res = self.client.get('/djangoapp/analyze/Fantastic services')
        self.assertEqual(res.json()['sentiment'], 'positive')
        self.assertTrue(get.call_args.args[0].endswith('/analyze/Fantastic%20services'))

    @mock.patch('djangoapp.restapis.requests.get', side_effect=restapis.requests.ConnectionError)
    def test_analyzer_down_falls_back_to_neutral(self, get):
        with self.assertLogs('djangoapp.restapis', level='WARNING'):
            self.assertEqual(restapis.analyze_review_sentiments('hi'), {'sentiment': 'neutral'})


class FrontendTests(TestCase):
    def test_spa_routes_resolve(self):
        for url in ['/', '/about', '/contact', '/login', '/register', '/dealers', '/dealers/Kansas',
                    '/dealer/1', '/postreview/1']:
            self.assertIn(self.client.get(url).status_code, (200, 503), url)

    def test_admin_login_page(self):
        self.assertEqual(self.client.get('/admin/login/').status_code, 200)
