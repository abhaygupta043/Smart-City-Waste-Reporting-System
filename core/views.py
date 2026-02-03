import random

from django.contrib import messages

from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


from django.contrib.auth import get_user_model
User = get_user_model() # This tells Django "User" refers to your custom core.User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Report , User
from .forms import ReportForm

from django.contrib.auth import login
from .forms import CustomUserCreationForm




from .forms import CustomUserCreationForm  # Import your new form



# 1. The Home Page
def home(request):
    return render(request, 'core/base.html')

# 2. Submit Report (The Dashboard)
@login_required # Only logged-in users can see this
# core/views.py
@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, "Report submitted successfully!")
            return redirect('dashboard')
    else:
        form = ReportForm()

    # Fetch previous reports for the logged-in user, newest first
    user_reports = Report.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'core/dashboard.html', {
        'form': form,
        'user_reports': user_reports
    })

# 3. View My Reports
@login_required
def my_reports(request):
    # Fetch only the reports belonging to the logged-in user
    reports = Report.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_reports.html', {'reports': reports})



from django.core.mail import send_mail

def register(request):
    # Redirect authenticated users away from registration
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')

        # Cleanup inactive users
        User.objects.filter(username=username, is_active=False).delete()
        User.objects.filter(email=email, is_active=False).delete()

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            
            otp_code = str(random.randint(1000, 9999))
            user.otp = otp_code
            user.otp_expires = timezone.now() + timedelta(minutes=10)
            user.save()

            # Email logic (Ensure this is filled in)
            send_mail(
                'Verification Code',
                f'Your OTP is: {otp_code}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect('verify_otp', email=user.email)
    
    
    else:
        form = CustomUserCreationForm()

    # This return MUST be at the very bottom, aligned with the first 'if'
    return render(request, 'registration/register.html', {'form': form})


def verify_otp(request, email):
    # If logged in, no need to verify another account here
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        try:
            user = User.objects.get(email=email, is_active=False)
            
            if user.otp == entered_otp and user.otp_expires > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account verified successfully! You can now login.")
                return redirect('login')
            else:
                messages.error(request, "Invalid or expired OTP.")
                # IMPORTANT: We fall through to the return at the bottom
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('register')

    # This context dictionary ensures 'email' is ALWAYS available to the template
    context = {'email': email}
    return render(request, 'registration/verify.html', context)


# core/views.py (Add this function)

# core/views.py

def verify_otp(request, email):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        try:
            user = User.objects.get(email=email, is_active=False)
            
            if user.otp == entered_otp and user.otp_expires > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account verified successfully! You can now login.")
                return redirect('login')
            else:
                messages.error(request, "Invalid or expired OTP.")
                # IMPORTANT: We fall through to the return at the bottom
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('register')

    # This context dictionary ensures 'email' is ALWAYS available to the template
    context = {'email': email}
    return render(request, 'registration/verify.html', context)



def resend_otp(request, email):
    try:
        # 1. Look for the user who exists but isn't active yet
        user = User.objects.get(email=email, is_active=False)
        
        # 2. Generate a fresh 4-digit code
        new_otp = str(random.randint(1000, 9999))
        
        # 3. Update the database with the fresh code and a new 10-minute window
        user.otp = new_otp
        user.otp_expires = timezone.now() + timedelta(minutes=10)
        user.save()

        # 4. Send the fresh email
        send_mail(
            'Your New Verification Code',
            f'Your fresh OTP is: {new_otp}. It expires in 10 minutes.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        messages.success(request, f"A fresh code has been sent to {email}.")
        
    except User.DoesNotExist:
        # If the user is already active, they shouldn't be here
        messages.error(request, "This account is already verified or does not exist.")
        return redirect('login')
    
    return redirect('verify_otp', email=email)