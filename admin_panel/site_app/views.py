from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from accounts.models import User
from apis.nft_management.models import Collection, Category, Nft



class DashboardTemplateView(View):

    def get(self, request):
        user_list_count = User.objects.all().count()
        nft_list_count = Nft.objects.all().count()
        category_list_count = Category.objects.all().count()
        collection_list_count = Collection.objects.all().count()

        return render(request, 'nft_admin/index.html', {
            'user': request.user,
            'image': 'favicon.svg',
            'user_count' : user_list_count,
            'nft_count': nft_list_count,
            'category_count': category_list_count,
            'collection_count': collection_list_count
        })

