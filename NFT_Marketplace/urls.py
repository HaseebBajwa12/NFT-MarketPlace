"""NFT_Marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apis.nft_management.urls')),
    path('api/', include('apis.admin_site_management.urls')),
    path('api/', include('apis.bidding_and_transection.urls')),
    path('api/', include('apis.wallet_management.urls')),
    path('api/', include('apis.user_management.urls')),
    path('admin_site/', include('admin_panel.bidding.urls')),
    path('admin_site/', include('admin_panel.collection_app.urls')),
    path('admin_site/', include('admin_panel.site_app.urls')),
    path('admin_site/', include('admin_panel.wallet_manager.urls')),
    path('admin_site/', include('admin_panel.admin_user.urls')),
    path('admin_site/', include('admin_panel.contact_faq.urls')),
    path('admin_site/', include('accounts.urls')),
    path('setting/', include('settings.urls')),
    path('api/settings/', include('settings.api_urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('summernote/', include('django_summernote.urls')),
    path('setting/', include('settings.urls')),
    path('api/settings/', include('settings.api_urls')),
    path('email/', include('admin_panel.custom_emails.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
