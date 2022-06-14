from django.urls import path
from . import views

app_name = 'bidding'

urlpatterns = [
    path('bidding/', views.BiddingdetailView.as_view(), name='bidding-list'),
    path('bidding/<int:id>', views.BiddingView.as_view(), name='bidding-View'),
    path('bidding/delete/<int:id>', views.DeleteBiddingView.as_view(), name='bidding-delete'),
    path('nft_transaction/', views.TransactiondetailView.as_view(), name='Nft-transaction-list'),
    path('nft_transaction/<int:id>', views.TransactionView.as_view(), name='Nft-transaction-view'),
    path('nft_transaction/delete/<int:id>', views.DeleteTransactionView.as_view(), name='transaction-delete'),
]
