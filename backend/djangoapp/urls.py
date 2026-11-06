from django.urls import path

from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.registration, name='register'),
    path('me', views.current_user, name='me'),
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review', views.add_review, name='add_review'),
    path('analyze/<path:text>', views.analyze_sentiment, name='analyze'),
    path('get_cars', views.get_cars, name='get_cars'),
    path('get_car_makes', views.get_car_makes, name='get_car_makes'),
    path('get_car_models', views.get_car_models, name='get_car_models'),
]
