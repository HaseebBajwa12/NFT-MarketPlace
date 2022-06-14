from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('site/', views.SiteView.as_view()),
    path('social/', views.SocialView.as_view()),
    path('percentage/', views.PercentageView.as_view())
]
