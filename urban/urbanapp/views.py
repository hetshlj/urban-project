from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from urllib3 import request
from .models import UserProfile
from django.utils import timezone
import random
import datetime
import os
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'urbanapp/index.html')

def about(request):
    return render(request, 'urbanapp/about.html')

def blog_grid(request):
    return render(request, 'urbanapp/blog-grid.html')

def blog_list(request):
    return render(request, 'urbanapp/blogs.html')

def blog_details(request):
    return render(request, 'urbanapp/blog-details.html')

def contact(request):
    return render(request, 'urbanapp/contact-us.html')

def how_it_works(request):
    return render(request, 'urbanapp/how-it-works.html')

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

def provider_dashboard(request):
    return render(request, 'provider/provider-dashboard.html')

def provider_services(request):
    return render(request, 'provider/provider-services.html')

def provider_booking(request):
    return render(request, 'provider/provider-booking.html')

def provider_staff(request):
    return render(request, 'provider/staff-list.html')

def provider_customers(request):
    return render(request, 'provider/customer-list.html')

def provider_payout(request):
    return render(request, 'provider/provider-payout.html')

def provider_holiday(request):
    return render(request, 'provider/provider-holiday.html')

def provider_coupons(request):
    return render(request, 'provider/provider-coupons.html')

def provider_offers(request):
    return render(request, 'provider/provider-offers.html')

def provider_reviews(request):
    return render(request, 'provider/provider-reviews.html')

def provider_enquiry(request):
    return render(request, 'provider/provider-enquiry.html')

def provider_earnings(request):
    return render(request, 'provider/provider-earnings.html')

def provider_chat(request):
    return render(request, 'provider/provider-chat.html')

def provider_appointment_settings(request):
    return render(request, 'provider/provider-appointment-settings.html')

def provider_accounts_settings(request):
    return render(request, 'provider/provider-accounts-settings.html')

def provider_social_profile(request):
    return render(request, 'provider/provider-social-profile.html')

def provider_security_settings(request):
    return render(request, 'provider/provider-security-settings.html')

def provider_plan(request):
    return render(request, 'provider/provider-plan.html')

def provider_payment_settings(request):
    return render(request, 'provider/payment-settings.html')

def provider_notifications(request):
    return render(request, 'provider/provider-notifcations.html')

def provider_connected_apps(request):
    return render(request, 'provider/provider-connected-apps.html')

def provider_verification(request):
    return render(request, 'provider/provider-verification.html')

def provider_delete_account(request):
    return render(request, 'provider/provider-delete-account.html')

def admin_users(request):
    # List users for admin interface
    # Select related profile to avoid extra queries
    users = User.objects.all().select_related('profile').order_by('-date_joined')
    return render(request, 'admin/users.html', {'users': users})

def admin_customers(request):
    return render(request, 'admin/customers.html')

def admin_providers(request):
    return render(request, 'admin/providers.html')


def provider_login(request):
    """Handle provider login (GET shows form, POST authenticates providers only).

    Accepts 'username' (or email) and 'password'. Only allows users who have an
    associated UserProfile with a truthy phone or explicit provider flag in DB.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is None and '@' in username:
            from django.contrib.auth.models import User as DjangoUser
            candidate = DjangoUser.objects.filter(email__iexact=username).first()
            if candidate:
                user = authenticate(request, username=candidate.username, password=password)

        if user is not None:
            # ensure this user is a provider via profile or DB flag
            profile = getattr(user, 'profile', None)
            is_provider = False
            if profile:
                # the SQL schema uses provider_profile linked to auth_user; we treat
                # presence of UserProfile and non-empty phone as a provider marker here.
                is_provider = bool(getattr(profile, 'phone', None))

            if not is_provider:
                messages.error(request, 'You are not registered as a provider.')
                return redirect('provider_login')

            if not user.is_active:
                messages.error(request, 'This account is inactive.')
                return redirect('provider_login')

            login(request, user)
            messages.success(request, 'Provider logged in successfully.')
            return redirect('provider_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('provider_login')

    return render(request, 'provider/provider-login.html')

def provider_register(request):
    """Handle GET/POST for provider registration."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect('provider_register')

        chosen_username = email
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        if UserModel.objects.filter(username__iexact=chosen_username).exists() or UserModel.objects.filter(email__iexact=email).exists():
            messages.error(request, 'A user with that email already exists.')
            return redirect('provider_register')

        try:
            with transaction.atomic():
                user = UserModel.objects.create_user(username=chosen_username, email=email, password=password)
                user.first_name = first_name
                user.save()
                # Create or update profile and mark as provider by setting phone
                UserProfile.objects.create(user=user, phone=phone)

            messages.success(request, 'Provider account created. Please sign in.')
            return redirect('provider_login')
        except Exception as e:
            messages.error(request, 'Unable to create provider account. Error: %s' % str(e))
            return redirect('provider_register')

    return render(request, 'provider/provider-register.html')


class ProviderPasswordResetView(auth_views.PasswordResetView):
    """Password reset only for provider accounts (User has a UserProfile with phone)."""
    template_name = 'provider/forgot-password.html'
    email_template_name = 'provider/password_reset_email.html'
    subject_template_name = 'provider/password_reset_subject.txt'
    success_url = reverse_lazy('provider_password_reset_done')

    def get_users(self, email):
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        # find users with matching email and who have a profile (provider)
        candidates = UserModel._default_manager.filter(email__iexact=email, is_active=True)
        for u in candidates:
            profile = getattr(u, 'profile', None)
            if profile and getattr(profile, 'phone', None):
                yield u


class ProviderPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'provider/password_reset_done.html'


class ProviderPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'provider/password_reset_confirm.html'
    success_url = reverse_lazy('provider_password_reset_complete')


class ProviderPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'provider/password_reset_complete.html'

def reset_password(request):
    return render(request, 'urbanapp/reset-password.html')

def admindash(request):
    return render(request,'admin/index.html')

def add_service(request):
    return render(request,'admin/add-service.html')

def admin_service(request):
    return render(request,'admin/services.html')

def admin_service_settings(request):
    return render(request,'admin/service-settings.html')

def admin_sub_categories(request):
    return render(request,'admin/sub-categories.html')

def admin_categories(request):
    return render(request,'admin/categories.html')

def admin_signin(request):
    # Handle admin signin (staff users only).
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is None and '@' in username:
            # allow email login for admin as well
            try:
                from django.contrib.auth.models import User as DjangoUser
                candidate = DjangoUser.objects.filter(email__iexact=username).first()
                if candidate:
                    user = authenticate(request, username=candidate.username, password=password)
            except Exception:
                user = None

        if user is not None:
            if not user.is_active:
                messages.error(request, 'This account is inactive.')
            elif not user.is_staff:
                messages.error(request, 'You do not have permission to access the admin.')
            else:
                login(request, user)
                messages.success(request, 'Admin logged in successfully.')
                return redirect('admindash')
        else:
            messages.error(request, 'Invalid username or password.')

        return redirect('admin_signin')

    return render(request,'admin/signin.html')


def admin_register(request):
    """Register a new admin/staff user. Creates a User with is_staff=True and an associated UserProfile.

    This view mirrors the public `register` behaviour but marks the created user as staff.
    In a real project you should protect admin creation (invite-only or require higher privileges).
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect('admin_register')

        chosen_username = username or email

        if User.objects.filter(username__iexact=chosen_username).exists():
            messages.error(request, 'A user with that username already exists.')
            return redirect('admin_register')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'A user with that email already exists.')
            return redirect('admin_register')

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=chosen_username, email=email, password=password)
                user.is_staff = True
                user.save()
                UserProfile.objects.create(user=user, phone=phone)

            messages.success(request, 'Admin account created. Please sign in.')
            return redirect('admin_signin')
        except Exception as e:
            messages.error(request, 'Unable to create admin account. Error: %s' % str(e))
            return redirect('admin_register')

    return render(request, 'admin/signup.html')


class AdminPasswordResetView(auth_views.PasswordResetView):
    """Send password reset emails only to staff users (is_staff=True)."""
    template_name = 'admin/forgot-password.html'
    email_template_name = 'admin/password_reset_email.html'
    subject_template_name = 'admin/password_reset_subject.txt'
    success_url = reverse_lazy('admin_password_reset_done')

    def get_users(self, email):
        """Return only active staff users with given email."""
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        active_users = UserModel._default_manager.filter(email__iexact=email, is_active=True, is_staff=True)
        return (u for u in active_users)


class AdminPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'admin/password_reset_done.html'


class AdminPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'admin/password_reset_confirm.html'
    success_url = reverse_lazy('admin_password_reset_complete')


class AdminPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'admin/password_reset_complete.html'

def register(request):
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