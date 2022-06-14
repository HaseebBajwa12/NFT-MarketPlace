from rest_framework.serializers import ModelSerializer

from .models import *


class BiddingSerializer(ModelSerializer):
    class Meta:
        model = Bidding
        fields = '__all__'
        read_only_fields = ('bidding_date',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['offer_by'] = f"{instance.offer_by.first_name} {instance.offer_by.last_name}"
        response['user_id'] = f"{instance.offer_by.id}"

        response['nft'] = f"{instance.nft.name}"
        response['nft_id'] = f"{instance.nft.id}"

        response['nft_image'] = f"{instance.nft.image}"
        return response


class NftTranactionSerializer(ModelSerializer):
    class Meta:
        model = NftTransaction
        fields = '__all__'
        read_only_fields = ('sold_date', 'is_removed')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['buyer'] = f"{instance.buyer.first_name} {instance.buyer.last_name}"
        response['seller'] = f"{instance.seller.first_name} {instance.seller.last_name}"
        response['nft'] = f"{instance.nft.name}"
        response['wallet'] = f"{instance.wallet.wallet_address}"
        return response
