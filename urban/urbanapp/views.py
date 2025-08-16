from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from .models import UserProfile
from django.utils import timezone
import random
import datetime
import os


def home(request):
    return render(request, 'urbanapp/index.html')


def about(request):
    return render(request, 'urbanapp/about.html')


def services(request):
    return render(request, 'urbanapp/services-list.html')


def servicedetails(request):
    return render(request, 'urbanapp/service-details.html')


def categories(request):
    return render(request, 'urbanapp/categories.html')

def providers(request):
    return render(request, 'urbanapp/providers.html')


def provider_details(request):
    return render(request, 'urbanapp/provider-details.html')

def create_service(request):
    return render(request, 'urbanapp/create-service.html')

def user_dashboard(request):
    return render(request, 'urbanapp/user-dashboard.html')

def user_booking_list(request):
    return render(request, 'urbanapp/user-booking-list.html')

def favourites(request):
    return render(request, 'urbanapp/favourites.html')

def user_wallet(request):
    return render(request, 'urbanapp/customer-wallet.html')

def user_reviews(request):
    return render(request, 'urbanapp/customer-reviews.html')

def user_chat(request):
    return render(request, 'urbanapp/user-chat.html')

def account_settings(request):
    return render(request, 'urbanapp/account-settings.html')

def register(request):
    """Handle GET/POST for user registration.

    POST fields: username, email, phone (optional), password
    Creates a Django User and a UserProfile record.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        # first_name removed from form; keep empty
        first_name = ''
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect('register')

        # Determine username: prefer explicitly provided username, otherwise use email
        chosen_username = username or email

        # Check uniqueness
        if User.objects.filter(username__iexact=chosen_username).exists():
            messages.error(request, 'A user with that username already exists.')
            return redirect('register')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'A user with that email already exists.')
            return redirect('register')

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=chosen_username, email=email, password=password)
                user.first_name = first_name
                user.save()
                UserProfile.objects.create(user=user, phone=phone)

            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')
        except Exception as e:
            # Show exception message during development to help debug why user creation failed
            messages.error(request, 'Unable to create account. Error: %s' % str(e))
            return redirect('register')

    return render(request, 'urbanapp/register.html')


def user_login(request):
    """Handle GET/POST for user login. Template posts 'username' and 'password'."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # First try normal authentication (username)
        user = authenticate(request, username=username, password=password)
        # If that fails and the input looks like an email, try to find the user by email
        if user is None and '@' in username:
            try:
                # lookup case-insensitive email
                from django.contrib.auth.models import User as DjangoUser
                candidate = DjangoUser.objects.filter(email__iexact=username).first()
                if candidate:
                    user = authenticate(request, username=candidate.username, password=password)
            except Exception:
                user = None

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('home')
            else:
                messages.error(request, 'This account is inactive.')
        else:
            messages.error(request, 'Invalid username or password.')

        return redirect('login')

    return render(request, 'urbanapp/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


def otp_request(request):
    """Request an SMS OTP by phone number (stored on UserProfile.phone).

    POST: phone
    Stores the OTP and expiry on the user's UserProfile and saves the user id in session.
    In development the OTP is shown in a success message for convenience. In production
    integrate an SMS provider (Twilio, Vonage, etc.) and remove the OTP from responses.
    """
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        if not phone:
            messages.error(request, 'Please provide a phone number.')
            return redirect('login_otp_request')

        profile = UserProfile.objects.filter(phone__iexact=phone).first()
        if not profile or not profile.user:
            messages.error(request, 'No account found with that phone number.')
            return redirect('login_otp_request')

        code = f"{random.randint(0, 999999):06d}"
        profile.verification_code = code
        profile.verification_expiry = timezone.now() + datetime.timedelta(minutes=5)
        profile.save()

        # Send SMS placeholder: if TWILIO_* env vars are present you can integrate here.
        # For now we surface the code to the developer via messages (remove in production).
        messages.success(request, f'OTP sent to {phone}. (dev code: {code})')

        request.session['otp_user_id'] = profile.user.id
        return redirect('login_otp_verify')

    return render(request, 'urbanapp/otp_request.html')


def otp_verify(request):
    """Verify the SMS OTP and log the user in if valid."""
    uid = request.session.get('otp_user_id')
    if not uid:
        messages.error(request, 'No OTP request in progress. Please request a new code.')
        return redirect('login_otp_request')

    user = User.objects.filter(id=uid).first()
    if not user:
        messages.error(request, 'User not found. Please request a new code.')
        return redirect('login_otp_request')

    profile = getattr(user, 'profile', None)

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        if profile and profile.verification_code == code and profile.verification_expiry and profile.verification_expiry > timezone.now():
            # successful OTP verification
            # clear stored code
            profile.verification_code = None
            profile.verification_expiry = None
            profile.save()
            login(request, user)
            request.session.pop('otp_user_id', None)
            messages.success(request, 'Logged in using OTP.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            return redirect('login_otp_verify')

    return render(request, 'urbanapp/otp_verify.html', {'phone': profile.phone if profile else ''})


def google_login(request):
    """Placeholder page explaining how to enable Google OAuth integration.

    For production, install and configure a library such as `django-allauth` or
    use Google Identity Platform and redirect users through OAuth flows.
    """
    return render(request, 'urbanapp/google_login.html')