from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.template.defaultfilters import slugify

from .forms import VendorForm
from .models import Vendor

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor

from menu.models import Category, FoodItem
from menu.forms import CategoryForm


# get vendor
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


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


# menu builder
@login_required(login_url="login")  # define login and redirect url
@user_passes_test(check_role_vendor)  # check user role
def menu_builder(request):
    vendor = get_vendor(request)  # get vendor
    categories = Category.objects.filter(vendor=vendor).order_by(
        "created_at"
    )  # get categories with vendor
    context = {
        "categories": categories,
    }

    return render(request, "vendor/menu_builder.html", context)


# food items
@login_required(login_url="login")  # define login and redirect url
@user_passes_test(check_role_vendor)  # check user role
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)  # get vendor
    category = get_object_or_404(Category, pk=pk)  # get category
    fooditems = FoodItem.objects.filter(
        vendor=vendor, category=category
    )  # get food items

    context = {
        "fooditems": fooditems,
        "category": category,
    }

    return render(request, "vendor/fooditems_by_category.html", context)


# add category
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)  # get form

        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = form.save(commit=False)  # ready save
            category.vendor = get_vendor(request)  # get vendor
            category.slug = slugify(category_name)  # slug
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect("menu_builder")
        else:
            print(form.errors)
    else:
        form = CategoryForm()  # get form

    context = {
        "form": form,
    }

    return render(request, "vendor/add_category.html", context)


# edit category
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)  # get form

        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = form.save(commit=False)  # ready save
            category.vendor = get_vendor(request)  # get vendor
            category.slug = slugify(category_name)  # slug
            form.save()
            messages.success(request, "Category added successfully!")  # message
            return redirect("menu_builder")
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)  # get form

    context = {
        "form": form,
        "category": category,
    }

    return render(request, "vendor/edit_category.html", context)


# delete category
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)  # get category
    category.delete()  # delete
    messages.success(request, "Category has been deleted successfully!")  # message

    return redirect("menu_builder")
