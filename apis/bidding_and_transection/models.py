from accounts.models import User
from django.db import models
from apis.nft_management.models import Nft
from apis.wallet_management.models import Wallet


class Bidding(models.Model):
    offer_by = models.ForeignKey(User, related_name="user_biding", on_delete=models.CASCADE)
    bidding_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    price = models.FloatField(verbose_name='bidding_price',null=False, blank=False)
    expiry_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)  # Accepted or Rejected
    nft = models.ForeignKey(Nft, related_name="bidding_nft", on_delete=models.CASCADE)


class NftTransaction(models.Model):
    buyer = models.ForeignKey(User, related_name="nft_buyer", on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name="nft_seller", on_delete=models.CASCADE)
    nft = models.ForeignKey(Nft, related_name="nft_transaction", on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, related_name="user_wallet", on_delete=models.CASCADE)
    sold_price = models.FloatField(null=False, blank=False)
    sold_date = models.DateTimeField(auto_now_add=True)
    service_fee = models.FloatField(default=0.0)
    is_removed = models.BooleanField(default=False)

    class Meta:
        unique_together=['buyer','seller']

