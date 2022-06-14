from django.urls import path

from . import views

app_name = 'admin_user'
urlpatterns = [
    path('home/', views.ListUserView.as_view(), name='home'),
    path('profiles_view/<int:id>/', views.ListUserProfileView.as_view(), name='profiles_view'),
    path('delete/<int:id>/', views.DeleteUserView.as_view(), name='deletepost'),
    path('update_profile/<int:id>/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('change-pass/', views.change_pass, name='change-pass')
]
