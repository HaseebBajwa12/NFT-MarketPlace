from accounts.models import User, Profile
from django.db import IntegrityError
from djoser.serializers import UserSerializer, UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['vine_link', 'profile_image', 'banner_image', 'about', 'vine_link',
                  'facebook_link', 'twitter_link', 'google_plus_link']


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)


class UserDetailSerializer(UserSerializer):
    user_profile = ProfileSerializer(read_only=True, many=False)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('user_profile', 'user_collection', 'email', 'first_name', 'last_name')


class CustomUserSerializer(UserSerializer):
    user_profile = ProfileSerializer(required=True, many=False)

    class Meta(UserSerializer.Meta):
        Model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'user_profile')
        read_only_fields = ('email',)

    def update(self, instance: User, validated_data):
        profile = validated_data('user_profile')
        if len(profile) > 0:
            profile = profile[0]
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']
        instance.save()
        if Profile.objects.filter(user=instance).count() == 0:
            Profile.objects.create(**profile, user=instance)
        else:
            Profile.objects.filter(user=instance).update(**profile)
        return instance


class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    profile_image = serializers.ImageField()
    facebook_link = serializers.URLField(required=False)
    twitter_link = serializers.URLField(required=False)
    google_plus_link = serializers.URLField(required=False)
    vine_link = serializers.URLField(required=False)
    banner_image = serializers.ImageField()
    about = serializers.CharField(max_length=200)

    # def update(self, instance, validated_data):
    #     if 'profile_image' in validated_data.keys():
    #         instance.profile_image = validated_data['profile_image']
    #     if 'banner_image' in validated_data.keys():
    #         instance.profile_image = validated_data['banner_image']
    #         instance.save()
    #         return instance


class CreateUserSerializer(UserCreatePasswordRetypeSerializer):

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
            Profile.objects.create(user=user, about='about')
        except IntegrityError:
            self.fail("cannot_create_user")

        return user
