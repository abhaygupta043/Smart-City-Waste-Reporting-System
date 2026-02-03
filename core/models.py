from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Updated User Model with OTP fields
class User(AbstractUser):
    # This forces the database to check for duplicates
    email = models.EmailField(unique=True) 
    reward_points = models.IntegerField(default=0)
    mobile = models.CharField(max_length=15, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expires = models.DateTimeField(blank=True, null=True)

    gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
        blank=True
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    
    # Add these two fields for the OTP logic
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expires = models.DateTimeField(blank=True, null=True)

# 2. Waste Report (remains the same)
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='reports/')
    
    
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], 
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)