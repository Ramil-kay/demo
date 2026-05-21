from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index_view , name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('bookings/', views.bookings_view, name='bookings'),
    path('profile/', views.profile_view, name='profile'),
    path('create-booking/', views.create_booking_view, name='create_booking'),
]
