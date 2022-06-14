from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("title", 'description', 'category', 'created_at',"updated","is_active")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'subject', 'message', 'is_responded', 'resolved_by', 'resolved_date', 'created_at',
        'updated_at')


