from accounts.models import User
from apis.nft_management.models import Category
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(null=False, blank=False, max_length=200)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_responded = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, related_name="resolved_user", on_delete=models.CASCADE, null=True, blank=True)
    resolved_date = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    title = models.CharField(null=False,max_length=200)
    description = models.TextField(null=False,max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True,blank=True)
    category = models.ForeignKey(Category, related_name="faq_category",on_delete=models.CASCADE,null=True,blank=True)
    updated_by = models.ForeignKey(User, related_name="FAQ_user", on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.title
