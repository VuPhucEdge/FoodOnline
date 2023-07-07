from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm


# register user view
def registerUser(request):
    if request.method == "POST":
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


def registerVendor(request):
    if request.method == "POST":
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
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        "form": form,
        "v_form": v_form,
    }
    return render(request, "accounts/registerVendor.html", context)
