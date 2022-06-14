from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('site/', views.UpdateSiteView.as_view(), name='site'),
    path('social/', views.UpdateSocialView.as_view(), name='social'),
    path('percentage/', views.UpdatePercentageView.as_view(), name='percentage'),
    ]