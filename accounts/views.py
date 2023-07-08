from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# register user view
def registerUser(request):
    # if user already logged in
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")  # message
        return redirect("myAccount")

    elif request.method == "POST":
        # get request data
        form = UserForm(request.POST)

        # form had data
        if form.is_valid():
            """
            Create the user using the form
            """
            # password = form.cleaned_data["password"]  # map data
            # user = form.save(commit=False)  # form ready save
            # user.set_password(password)  # hash password
            # user.role = User.CUSTOMER  # choice role
            # user.save()

            """
                Create the user using create_user method
            """
            # Get data to form and map data on database
            firts_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # create instance user
            user = User.objects.create_user(
                first_name=firts_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.role = User.CUSTOMER  # choice role
            user.save()

            # message
            messages.success(
                request,
                "Your account has been registered successfully!",
            )

            return redirect("registerUser")
        else:
            print(form.errors)
    else:
        form = UserForm()

    context = {
        "form": form,
    }

    return render(request, "accounts/registerUser.html", context)


# register vendor
def registerVendor(request):
    # if user already logged in
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")  # message
        return redirect("myAccount")

    elif request.method == "POST":
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            # Get data to form and map data on database
            firts_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # create instance user
            user = User.objects.create_user(
                first_name=firts_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.role = User.VENDOR  # role
            user.save()  # create user and signals user profile

            vendor = v_form.save(commit=False)  # ready save
            vendor.user = user  # add user
            user_profile = UserProfile.objects.get(user=user)  # get user profile
            vendor.user_profile = user_profile  # add user profile
            vendor.save()  # create vendor

            # message
            messages.success(
                request,
                "Your account has been registered successfully! Please wait for the approval.",
            )

            return redirect("registerVendor")
        else:
            print("Invalid form")
            print(form.errors)  # form errors
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        "form": form,
        "v_form": v_form,
    }

    return render(request, "accounts/registerVendor.html", context)


# login
def login(request):
    # if user already logged in
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")  # message
        return redirect("myAccount")

    # if user login
    elif request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # compare email and password on database
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)  # login
            messages.success(request, "You are now logged in.")  # message
            return redirect("myAccount")
        else:
            messages.error(request, "Invalid login credentials")  # message
            return redirect("login")

    return render(request, "accounts/login.html")


# logout
def logout(request):
    auth.logout(request)  # logout
    messages.info(request, "You are logged out")  # message
    return redirect("login")


# define user role and redirect by detect function
@login_required(login_url="login")  # define login and redirect url
def myAccount(request):
    user = request.user  # get user by request
    redirectUrl = detectUser(user)  # call detectUser function, define user role
    return redirect(redirectUrl)  # redirect


# customer dashboard
@login_required(login_url="login")  # define login and redirect url
@user_passes_test(check_role_customer)  # check user role
def custDashboard(request):
    return render(request, "accounts/custDashboard.html")


# vendor dashboard
@login_required(login_url="login")  # define login and redirect url
@user_passes_test(check_role_vendor)  # check user role
def vendorDashboard(request):
    return render(request, "accounts/vendorDashboard.html")
