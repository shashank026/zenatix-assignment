from email import message
from re import sub
from django.conf import settings
from django.core.mail import send_mail




def send_account_activation_email(email, email_token):
    subject = 'You need to activate your account.'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to activate your account http://localhost:8000/accounts/activate/{email_token}'
    send_mail(subject, message, email_from, [email])