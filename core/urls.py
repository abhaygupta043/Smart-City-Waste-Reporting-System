from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-reports/', views.my_reports, name='my_reports'),
    
    # Auth URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('verify-otp/<str:email>/', views.verify_otp, name='verify_otp'),

    path('resend-otp/<str:email>/', views.resend_otp, name='resend_otp'),
]