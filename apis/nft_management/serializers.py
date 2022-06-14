from apis.user_management.serializers import ProfileSerializer
from apis.user_management.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer

from .models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ("is_removed", "is_active")


class NFTSerializer(ModelSerializer):
    class Meta:
        model = Nft
        fields = '__all__'
        read_only_fields = (
            "is_hidden", "updated_at", "is_removed", "created_at", 'total_views')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['collection_id'] = f"{instance.collection.id}"
        response['collection'] = f"{instance.collection.name}"
        response['logo_image'] = f"{instance.collection.logo_image}"
        response['banner_image'] = f"{instance.collection.banner_image}"
        response['owner'] = f"{instance.owner.first_name} {instance.owner.last_name}"
        response['user_id'] = f"{instance.owner.id}"
        image_url = instance.owner.user_profile.profile_image
        response['profile_image'] = image_url.url if image_url is not None else None
        return response


class CollectionUserSerializer(ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Collection
        fields = "__all__"
        depth = 2


class FavouriteNftSerializer(ModelSerializer):
    class Meta:
        model = FavouriteNft
        fields = "__all__"
        read_only_fields = ("is_removed", "date")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["nft"] = f"{instance.nft.name}"
        response["user"] = f"{instance.user.first_name} {instance.user.last_name}"
        return response


class ReportedNftSerializer(ModelSerializer):
    class Meta:
        model = ReportedNft
        fields = "__all__"
        read_only_fields = ("is_resolved",)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["nft"] = f"{instance.nft.name}"
        response[
            "reporter"
        ] = f"{instance.reporter.first_name} {instance.reporter.last_name}"
        return response


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ("is_removed", "created_at", "updated_at")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["category_id"] = f"{instance.category.id}"
        response["category"] = f"{instance.category.name}"
        response["user"] = f"{instance.user.first_name} {instance.user.last_name}"
        response["user_id"] = f"{instance.user.id}"

        return response


class CollectionNftSerializer(ModelSerializer):
    nft_collection = NFTSerializer(read_only=True, many=True)

    class Meta:
        model = Collection
        fields = ("name", 'logo_image', 'banner_image', 'description', 'category', 'user', "nft_collection")
        read_only_fields = ("is_removed", "created_at", "updated_at")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["category"] = f"{instance.category.name}"
        response["category_id"] = f"{instance.category.id}"

        response["user"] = f"{instance.user.first_name} {instance.user.last_name}"
        response["user_id"] = f"{instance.user.id}"

        return response


class LiveAuctionSerializer(ModelSerializer):
    user_profile = ProfileSerializer(read_only=True, many=False)

    class Meta:
        model = Nft
        exclude = (
            'size', 'no_of_copies', 'is_hidden', 'is_removed', 'collection', 'total_views', 'royalty', 'updated_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["owner"] = f"{instance.owner.first_name} {instance.owner.last_name}"
        response["user_id"] = f"{instance.owner.id}"
        image_url = instance.owner.user_profile.profile_image
        response['profile_image'] = image_url.url if image_url is not None else None
        return response
