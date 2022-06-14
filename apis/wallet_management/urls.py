from django.urls import path
from . import views


urlpatterns = [
    path('wallet/<int:pk>/', views.WalletAPI.as_view(), name='wallet'),
    path('wallet_list/', views.WalletListView.as_view(), name='wallet_list')
]
