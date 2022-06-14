from rest_framework.serializers import ModelSerializer

from .models import *


class FAQSerializer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
        read_only_fields = ("created_at", "updated", "is_active")


def to_representation(self, instance):
    response = super().to_representation(instance)
    # response['category'] = f"{instance.category.name}"
    # response['updated_by'] = f"{instance.updated_by.first_name} {instance.updated_by.last_name}"
    return response


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
