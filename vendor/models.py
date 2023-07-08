from django.db import models
from accounts.models import User, UserProfile


# Create your models here.
class Vendor(models.Model):
    # one user, one vendor
    user = models.OneToOneField(
        User,
        related_name="user",  # define name
        on_delete=models.CASCADE,
    )
    # one profile, one vendor
    user_profile = models.OneToOneField(
        UserProfile,
        related_name="userprofile",  # define name
        on_delete=models.CASCADE,
    )
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to="vendor/license")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # define vendor name display admin
    def __str__(self):
        return self.vendor_name
