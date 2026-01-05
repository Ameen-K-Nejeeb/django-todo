from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

# Keep your existing CustomUserCreationForm here...

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    # ✅ Name validation (only letters)
    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')

        if not name.isalpha():
            raise ValidationError(
                "Name should contain only letters (no numbers or special characters)."
            )
        return name

    # ✅ Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")

        # strict email pattern
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValidationError("Enter a valid email address.")

        return email

    # ✅ Password match validation
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already used by another user.")

        return email
