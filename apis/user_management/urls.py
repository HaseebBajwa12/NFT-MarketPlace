
from django.urls import path, include, re_path
from . import views
from .views import activate_user_view, password_reset_view, LogoutAPIView, UserActivationView

urlpatterns = [
    path('profile/create/', views.CreateProfile.as_view(), name='profile-create'),
    path('profile/get-list/', views.GetProfileList.as_view(), name='profile_list'),
    path('profile/crud/<int:pk>/', views.ProfileManagement.as_view(), name='profile-crud'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('account/activate/<str:uid>/<str:token>/', activate_user_view),
    path('account/password/reset/confirm/<str:uid>/<str:token>/', password_reset_view),
    path('logout/', LogoutAPIView.as_view()),
    path('user-list-nft/', views.UserDetailView.as_view()),
    path('user_list-profile/',views.users_profile_list),
    path('update_profile/<int:pk>/',views.UpdateProfile.as_view()),
    re_path(r'^auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),
 ]


