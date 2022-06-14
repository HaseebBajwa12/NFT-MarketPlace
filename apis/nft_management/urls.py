from django.urls import path

from . import views

urlpatterns = [
    # NFT URLs
    path('specific_nft/<int:pk>/', views.NFTView.as_view(), name="nft"),
    path('update_delete_nft/<int:pk>/', views.NFTManagementView.as_view(), name='auth-nft-crud'),
    path('create_nft/', views.NFTCreateView.as_view(), name="nft-create"),
    path('nft_list/', views.NFTListView.as_view(), name='nft-list'),
    # Category URLs
    path('update_delete_category/<int:pk>/', views.CategoryManagementView.as_view(), name='category-crud'),
    path("create_category/", views.CategoryCreateView.as_view(), name='create-category'),
    path('specific_category/<int:pk>/', views.CategoryView.as_view(), name='specific-category'),
    path('category_list/', views.CategoryListView.as_view(), name='category-list'),
    # Collection URLs
    path("create_collection/", views.CreateCollectionView.as_view(), name='create-collection'),
    path("specific_collection/<int:pk>/", views.CollectionView.as_view(), name='specific-collection'),
    path("update_delete_collection/<int:pk>/", views.CollectionManagementView.as_view(), name='collection-crud'),
    path('collection_list/', views.CollectionListView.as_view(), name='collection-list'),
    # Favourite URLs
    path('favourite-nft/', views.FavouritesNftView.as_view(), name='favourites-nft'),
    path('delete_favourite_nft/<int:pk>/', views.FavouritesNFTDeleteView.as_view(), name='delete-favourites-nft'),

    # Reported NFT URLs
    path('create_reported_nft/', views.ReportedNFTCreateView.as_view(), name='create-reported-nft'),
    path('reported_nft_list/', views.ReportedNFTListView.as_view(), name="reported-nft-list"),
    path('reported_nft/<int:pk>/', views.ReportedNFTView.as_view(), name='reported-nft'),
    path('reported_nft_delete/<int:pk>', views.ReportedNFTDeleteView.as_view(), name='delete-reported-nft'),
    path('top_sellers/', views.top_sellers, name='top-sellers'),
    path('specific_user_nft_data/<int:id>/', views.users_nft_data, name="users_nft_data_list"),
    path('live-auction-nfts/', views.LiveAuction.as_view(), name="live-auction-nfts"),
    path('specific_catgory_collection-data/<int:id>/', views.category_collection_data, name='specific_cat'),
    path('specific-user-collection/<int:pk>/', views.user_collection, name='user-collection'),

]
