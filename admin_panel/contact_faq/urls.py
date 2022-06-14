from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = "faq_contact"

urlpatterns = [
    path("list_contact/", views.ListContactView.as_view(), name='list-contact'),
    path("delete_contact/<int:id>", views.DeleteContactView.as_view(), name='delete-contact'),
    path("create_faq/", views.CreateFAQView.as_view(), name='create-faq'),
    path("list_faq/", views.ListFAQView.as_view(), name='list-faq'),
    path("update_faq/<int:id>", views.UpdateFAQView.as_view(), name='update-faq'),
    path("delete_faq/<int:id>", views.DeleteFAQView.as_view(), name='delete-faq'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
