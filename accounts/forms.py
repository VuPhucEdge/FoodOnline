from django import forms

from .models import User, UserProfile
from .validators import allow_only_images_validator


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


class UserProfileForm(forms.ModelForm):
    """
    Set from with class css
    """

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Start Typing...",
                "required": "required",
            }
        )
    )
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_images_validator],
    )
    cover_photo = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_images_validator],
    )

    # read only fields
    # latitude = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))

    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "cover_photo",
            "address",
            "country",
            "state",
            "city",
            "pin_code",
            "latitude",
            "longitude",
        ]

    # read only fields using __init__
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == "latitude" or field == "longitude":
                self.fields[field].widget.attrs["readonly"] = "readonly"
