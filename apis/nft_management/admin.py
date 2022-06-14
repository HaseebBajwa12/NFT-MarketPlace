from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Nft)
admin.site.register(NftPriceHistory)
admin.site.register(FavouriteNft)
admin.site.register(ReportedNft)