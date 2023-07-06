from django import forms
from .models import User


# User form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # password form
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )  # confirm password form

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")  # get password
        confirm_password = cleaned_data.get("confirm_password")  # get confirm password

        # Compare password
        if password != confirm_password:
            raise forms.ValidationError("Password dose not match!")
