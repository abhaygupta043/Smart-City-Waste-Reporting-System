import re

from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Report  # Import your Report model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email", "mobile", "gender", "age")
        # 1. Constraint for First Name (No numbers or special chars)
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name should only contain alphabets.")
        return first_name

    # 2. Constraint for Last Name (No numbers or special chars)
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Last name should only contain alphabets.")
        return last_name

    # 3. Constraint for Mobile Number (Exactly 10 digits, no alphabets)
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit():
            raise ValidationError("Mobile number must contain only digits.")
        if len(mobile) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits.")
        return mobile

    # 4. Constraint for Age (Reasonable range)
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 12 or age > 100):
            raise ValidationError("Please enter a valid age between 12 and 100.")
        return age


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        # These fields must match the names in your Report model
        fields = ['location', 'description', 'video']
        
        # Optional: Add styling to make it look better
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'Enter location'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the waste...'}),
        }