from django.contrib import messages
from django.core.paginator import Paginator
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

# Create your views here.
from admin_panel.custom_emails.forms import EmailTemplateForm
from admin_panel.custom_emails.models import EmailTemplate
from django.contrib.messages.views import SuccessMessageMixin


class EmailTemplateListView(ListView):
    template_name = 'email_template_list.html'
    model = EmailTemplate
    paginate_by = 5

    def get(self, request):
        obj = EmailTemplate.objects.all()
        p = Paginator(obj.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'email_template_list.html',
                      {'obj': obj,

                       })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EmailTemplateUpdateView(UpdateView, SuccessMessageMixin):
    template_name = 'email_template_update.html'
    model = EmailTemplate
    # fields = ['subject', 'body']
    # template_name = 'email_update'
    form_class = EmailTemplateForm
    success_url = reverse_lazy('custom_emails:email_list')

    def form_valid(self, form):
        messages.success(self.request, 'Email template Updated Successfully')
        return super().form_valid(form)
