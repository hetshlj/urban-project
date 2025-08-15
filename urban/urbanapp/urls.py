from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # Password reset flow
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='urbanapp/forgot-password.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='urbanapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='urbanapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='urbanapp/password_reset_complete.html'), name='password_reset_complete'),
    # OTP-based SMS login
    path('login/otp/request/', views.otp_request, name='login_otp_request'),
    path('login/otp/verify/', views.otp_verify, name='login_otp_verify'),
    # Google OAuth placeholder
    path('login/google/', views.google_login, name='login_google'),
    path('services-list/', views.services, name='services'),
    path('service-details/', views.servicedetails, name='servicesdetails'),
    path('categories/', views.categories, name='categories'),

]
