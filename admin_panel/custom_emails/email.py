from django.core import mail
from django.views.generic.base import ContextMixin


class ConfirmationEmail(mail.EmailMultiAlternatives, ContextMixin):

    template_name = "email/confirmation.html"
