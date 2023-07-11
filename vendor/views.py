from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)

from .forms import VendorForm
from .models import Vendor

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor


# vendor profile
@login_required(login_url="login")  # define login and redirect url
@user_passes_test(check_role_vendor)  # check user role
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)  # get profile or 404
    vendor = get_object_or_404(Vendor, user=request.user)  # get vendor or 404

    # check request
    if request.method == "POST":
        profile_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )
        vendor_form = VendorForm(
            request.POST,
            request.FILES,
            instance=vendor,
        )

        # check valid
        if profile_form.is_valid() and vendor_form.is_valid():
            # save if true
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Settings Update")  # message
            return redirect("vprofile")
        else:
            # error
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(
            instance=profile
        )  # get profile form and load data
        vendor_form = VendorForm(instance=vendor)  # get vendor form and load data

    context = {
        "profile_form": profile_form,
        "vendor_form": vendor_form,
        "profile": profile,
        "vendor": vendor,
    }

    return render(request, "vendor/vprofile.html", context)
