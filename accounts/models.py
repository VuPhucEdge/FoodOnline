from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    # create an user
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)  # hash password
        user.save(using=self._db)  # define database using

        return user

    # create a superuser
    def create_superuser(self, first_name, last_name, username, email, password=None):
        # before, u need create an user
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)  # define database using

        return user


# User model
class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2
    ROLE_CHOICE = (
        (RESTAURANT, "Restaurant"),
        (CUSTOMER, "Customer"),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, blank=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICE,
        blank=True,
        null=True,
    )

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # default django using username for login
    # but I want use email for login
    # config login
    USERNAME_FIELD = "email"
    # config fields required
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    # config use UserManage replace default django user manager
    objects = UserManager()

    # config display email in admin
    def __str__(self):
        return self.email

    # check permission
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # check permission
    def has_module_perms(self, app_label):
        return True


# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )  # one user only has one profile
    profile_picture = models.ImageField(
        upload_to="users/profile_picture",
        blank=True,
        null=True,
    )
    cover_photo = models.ImageField(
        upload_to="users/cover_photo",
        blank=True,
        null=True,
    )
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
