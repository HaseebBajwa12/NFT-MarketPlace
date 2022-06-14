from django.urls import path, include
from admin_panel.custom_emails.views import EmailTemplateListView, EmailTemplateUpdateView

app_name = "custom_emails"
urlpatterns = [
    path('list/', EmailTemplateListView.as_view(), name='email_list'),
    path('list/update/<int:pk>', EmailTemplateUpdateView.as_view(), name='update-email-template')

]
