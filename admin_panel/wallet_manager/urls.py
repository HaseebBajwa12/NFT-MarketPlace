from django.urls import path
from . import views

app_name = 'wallet_manager'

urlpatterns = [
    path('wallet_transaction/', views.WalletTransactiondetailView.as_view(), name='wallet-transaction'),
    path('wallet/', views.WalletDisplay.as_view(), name='wallet'),
    path('wallet/<int:id>', views.DeleteWalletView.as_view(), name='wallet-delete'),
    path('wallet_view/<int:id>', views.WalletDisplayView.as_view(), name='wallet_view'),
    path('wallet_transaction_view/<int:id>', views.WalletTransactionView.as_view(), name='wallet_transaction_view'),
]
