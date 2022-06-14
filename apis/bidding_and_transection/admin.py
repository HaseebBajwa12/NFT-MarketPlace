from django.contrib import admin

from .models import *


@admin.register(Bidding)
class BiddingAdmin(admin.ModelAdmin):
    list_display = ("offer_by", 'bidding_date', 'price', 'expiry_date', "status", "nft")
    list_filter = ('bidding_date',)


@admin.register(NftTransaction)
class NftTransactionAdmin(admin.ModelAdmin):
    list_display = ("buyer", 'seller', 'nft', 'sold_price', "sold_date", "wallet","service_fee")
    list_filter = ("sold_date",)
    search_fields = ('buyer__first_name','nft__name','service_fee')