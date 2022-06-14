# Create your models here.
from django.db import models

email_types = [
    ('forgot-password', 'Forgot Password'),
    ('user-activation', 'User Activation'),
    ('activation-confirmation', 'Activation Confirmation')
]


class EmailTemplate(models.Model):
    type = models.CharField(choices=email_types, max_length=100)
    subject = models.CharField(max_length=250)
    body = models.TextField()
