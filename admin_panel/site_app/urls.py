from django.urls import path
from . import views


app_name = 'admin_side'

urlpatterns = [
    path("dashboard/", views.DashboardTemplateView.as_view(), name='dashboard'),
]
