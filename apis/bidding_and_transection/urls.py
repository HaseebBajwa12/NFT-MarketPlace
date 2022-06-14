from django.urls import path
from . import views


urlpatterns = [
    path('bidding/<int:pk>/', views.BiddingView.as_view(), name='bidding'),
    path('bidding/', views.BiddingListView.as_view(), name='bidding_list'),
    path('nft-transaction/', views.NftTransactionView.as_view(), name='nft-transaction'),
    path('nft-transaction-detail/<int:pk>', views.NftTransactionDetail.as_view(), name='nft-transaction-detail'),
    path('specific_bidding_nft/<int:id>/', views.bidding_nft_data, name='bidding_nft'),
 ]
