from django.urls import path
from . import views


urlpatterns = [
    path("faqs/<int:pk>/", views.FAQView.as_view(), name='faq-crud'),
    path('faq_list/', views.FAQListView.as_view(), name='faq-list'),
    path('contacts/<int:pk>/', views.ContactAPIView.as_view(), name='contacts'),
    path('contact_list/', views.ContactListView.as_view(), name='cont_list')
]