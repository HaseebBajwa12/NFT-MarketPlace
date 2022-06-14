from rest_framework.serializers import ModelSerializer
from .models import *


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ('is_removed', )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = f"{instance.user.first_name} {instance.user.last_name}"
        return response
