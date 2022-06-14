from rest_framework.serializers import ModelSerializer
from .models import *


class SiteSerializer(ModelSerializer):
    class Meta:
        model = SiteSetting
        # fields = '__all__'
        exclude = ('code', 'id')


class SocialSerializer(ModelSerializer):
    class Meta:
        model = SocialSetting
        # fields = '__all__'
        exclude = ('code', 'id')


class PercentageSerializer(ModelSerializer):
    class Meta:
        model = PercentageSetting
        # fields = '__all__'
        exclude = ('code', 'id')
