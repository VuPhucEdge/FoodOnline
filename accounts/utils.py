"""
    Utils
"""
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


# Detect user and redirect
def detectUser(user):
    if user.role == 1:
        redirectUrl = "vendorDashboard"
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "custDashboard"
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = "/admin"
        return redirectUrl


# # send mail
# def send_verification_email(request, user):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     current_site = get_current_site(request)  # get current site
#     mail_subject = "Please activate your account"  # subject
#     # message
#     message = render_to_string(
#         "accounts/emails/account_verification_email.html",
#         {
#             "user": user,
#             "domain": current_site,
#             "uid": urlsafe_base64_encode(
#                 force_bytes(user.pk)
#             ),  # get user pk and encode
#             "token": default_token_generator.make_token(user),
#         },
#     )
#     to_email = user.email  # send to
#     mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
#     mail.send()  # send mail


# # reset password email
# def send_password_reset_email(request, user):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     current_site = get_current_site(request)  # get current site
#     mail_subject = "Reset Your Password"  # subject
#     # message
#     message = render_to_string(
#         "accounts/emails/reset_password_email.html",
#         {
#             "user": user,
#             "domain": current_site,
#             "uid": urlsafe_base64_encode(
#                 force_bytes(user.pk)
#             ),  # get user pk and encode
#             "token": default_token_generator.make_token(user),
#         },
#     )
#     to_email = user.email  # send to
#     mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
#     mail.send()  # send mail


# send mail
def send_mail(request, user, mail_subject, mail_tempalte):
    from_email = settings.DEFAULT_FROM_EMAIL  # from email default
    current_site = get_current_site(request)  # get current site
    # message
    message = render_to_string(
        mail_tempalte,
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(
                force_bytes(user.pk)
            ),  # get user pk and encode
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email  # send to
    mail = EmailMessage(
        mail_subject,
        message,
        from_email,
        to=[to_email],
    )
    mail.send()  # send mail


# send notification
def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL  # from email default
    message = render_to_string(mail_template, context)  # message
    to_email = context["user"].email  # user email address
    mail = EmailMessage(
        mail_subject,
        message,
        from_email,
        to=[to_email],
    )
    mail.send()
