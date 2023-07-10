from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification


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

    # access save function
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            orig = Vendor.objects.get(pk=self.pk)  # get status vendor current

            # check status is_approved
            if orig.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                context = {
                    "user": self.user,
                    "is_approved": self.is_approved,
                }

                # if status is_approved change
                if self.is_approved == True:
                    # send notification Congratulation mail
                    mail_subject = "Congratulation! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # send notification mail
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."
                    send_notification(mail_subject, mail_template, context)

        return super(Vendor, self).save(*args, **kwargs)
