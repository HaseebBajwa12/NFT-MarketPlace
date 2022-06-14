from django.views import View
from django.urls import reverse
from apis.admin_site_management.models import Contact
from accounts.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from admin_panel.contact_faq.forms import FAQForm
from apis.admin_site_management.models import FAQ
from .filters import ContactFilter, FAQFilter
from django.core.paginator import Paginator
from apis.nft_management.models import Category
from django.contrib import messages


# Create your views here.


class ListContactView(View):
    """
    **ListContactView class**

    This view used to perform get request on Contact object to view the list of contact object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request):
        """
        Http get request use to Render create_contact template, categories and users.

        **Template:**

        `template:` faq_contact/list-collection.html

        **Returns:**

        `render:` list-contact template and contact list

        """
        contact_list = Contact.objects.all()
        cfilter = ContactFilter(request.GET, queryset=contact_list)
        contact_list = cfilter.qs
        p = Paginator(contact_list.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)

        return render(request, 'list_contact.html', {'contact_list': contact_list, 'obj': obj, 'cfilter': cfilter})


class DeleteContactView(View):
    """
    **DeleteContactView class**

    This view used to perform get  request on Contact object to delete the Contact object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render list contact template after delete the contact.

        **Template:**

        `template:` faq_contact/list-contact.html

        **Returns:**

        `HttpResponseRedirect:` contact list template

        """
        object = Contact.objects.get(id=id)
        object.delete()
        messages.success(request, 'delete successfully.')
        messages.set_level(request, messages.INFO)
        url = reverse('faq_contact:list-contact')
        return HttpResponseRedirect(url)


class CreateFAQView(View):
    """
    **CreateFAQView class**

    This view used to perform get and post request on FAQ object to create the faq object

    **Parameters**

    `View` : django.views

    """

    def get(self, request):
        """
        Http get request use to Render create_faq template, categories and users.

        **Template:**

        `success-template:` faq_contact/create-faq.html

        **Returns:**

        ``render`` : `create faq template, categories list, users list`

        """

        category_list = Category.objects.all()
        user_list = User.objects.all().filter(is_staff=True)
        form = FAQForm()
        return render(request, 'create_faq.html', {
            'category_list': category_list,
            'user_list': user_list,
            'errors': None,
            'form': form
        })

    def post(self, request):
        """
        Http post request use to Create an individual FAQ object.

        **Template:**

        `success-template:` adminsite2/list-faq.html

        `un-success-template:` adminsite2/create-faq.html

        **Returns:**

        `HttpResponseRedirect` : 'if form is valid'

        `else` : render 'create faq template and objects used in  faq creation'
        """
        print("data : ", request.POST)
        if request.method == "POST":
            form = FAQForm(request.POST, request.FILES)
            messages.success(request, 'Created Successfully.')
            messages.set_level(request, messages.INFO)
            print(form.errors)
            if form.is_valid():
                form.save()
                url = reverse('faq_contact:list-faq')
                return HttpResponseRedirect(url)

            else:
                # category_list = Category.objects.all()
                # user_list = User.objects.all().filter(is_staff=True)
                faq = FAQ.objects.all()
                form = FAQForm()
                return render(request, 'create_faq.html', {
                    "form": form,
                    "faq": faq
                })


class ListFAQView(View):
    """
    **ListFAQView class**

    This view used to perform get request on Collection object to view the list of collection object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request):
        """
        Http get request use to Render create_faq template, categories and users.

        **Template:**

        `template:` adminsite2/list-faq.html

        **Returns:**

        `render:` list-faq template and faq list

        """
        faq_list = FAQ.objects.all()
        faqfilter = FAQFilter(request.GET, queryset=faq_list)
        faq_list = faqfilter.qs
        p = Paginator(faq_list.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'list_faq.html', {'faq_list': faq_list, 'obj': obj, 'faqfilter': faqfilter})


class UpdateFAQView(View):
    """
    **UpdateFAQView class**

    This view used to perform get and post request on FAQ object to update the FAQ object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render update_faq template, specific ID faq ,categories, form errors and users.

        **Template:**

        `template:` adminsite2/update-faq.html

        **Returns:**

        `render:` specific faq, user object, category object and forms errors

        """
        # object = FAQ.objects.get(id=id)
        #
        # print(object.created_at, object.updated)
        # form = FAQForm()
        instance = FAQ.objects.get(id=id)
        form = FAQForm(request.POST or None, instance=instance)

        return render(request, 'update_faq.html', {
            'form': form,

        })

    def post(self, request, id):
        """
        Http post request use to Update an individual FAQ object.

        **Template:**

        `success-template:` adminsite2/list-collection.html

        `un-success-template:` adminsite2/update-collection.html

        **Returns:**

        `HttpResponseRedirect` : 'if form is valid'

        `else` : render 'update faq template and objects used in faq creation'
        """
        messages.success(request, 'Updated Successfully.')
        messages.set_level(request, messages.INFO)
        faq_object = FAQ.objects.get(id=id)
        form = FAQForm(request.POST, request.FILES, instance=faq_object)
        if form.is_valid():
            form.save()
            url = reverse('faq_contact:list-faq')
            # messages.success(self.request, 'update successfully')
            return HttpResponseRedirect(url)
        else:
            faq = FAQ.objects.all()
            form = FAQForm()
        return render(request, 'update_faq.html', {
            "form": form,
            # "faq":faq
        })


class DeleteFAQView(View):
    """
    **DeleteFAQView class**

    This view used to perform get  request on FAQ object to delete the FAQ object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render list faq template after delete the faq.

        **Template:**

        `template:` adminsite2/list-faq.html

        **Returns:**

        `HttpResponseRedirect:` faq list template

        """
        object = FAQ.objects.get(id=id)
        object.delete()
        messages.success(request, 'Deleted Successfully.')
        messages.set_level(request, messages.INFO)
        url = reverse('faq_contact:list-faq')
        return HttpResponseRedirect(url)


