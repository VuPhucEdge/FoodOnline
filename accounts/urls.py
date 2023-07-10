from django.urls import path, include

from . import views

urlpatterns = [
    # default url
    path("", views.myAccount, name="accounts"),
    # actions
    path(
        "registerUser/",
        views.registerUser,
        name="registerUser",
    ),
    path(
        "registerVendor/",
        views.registerVendor,
        name="registerVendor",
    ),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # dashboards
    path("myAccount/", views.myAccount, name="myAccount"),
    path("custDashboard/", views.custDashboard, name="custDashboard"),
    path("vendorDashboard/", views.vendorDashboard, name="vendorDashboard"),
    # activate
    path("avtivate/<uidb64>/<token>", views.activate, name="activate"),
    # forgot and reset password
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path(
        "reset_password_validate/<uidb64>/<token>",
        views.reset_password_validate,
        name="reset_password_validate",
    ),
    path("reset_password/", views.reset_password, name="reset_password"),
    # vendor url
    path("vendor/", include("vendor.urls")),
]
