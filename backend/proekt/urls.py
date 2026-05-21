from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home , name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('bookings/', views.bookings_view, name='bookings'),
    path('create-booking/', views.create_booking_view, name='create_booking'),
    path('admin/', views.admin_panel_view, name='admin_panel'),
]
