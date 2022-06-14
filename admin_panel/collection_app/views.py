from accounts.models import User
from admin_panel.collection_app.filters import CollectionFilter, CategoryFilter, FavouriteNftFilter, ReportedNftFilter, \
    nphFilter, nftFilter
from admin_panel.collection_app.forms import CategoryForm
from apis.nft_management.models import Collection, Category, FavouriteNft, ReportedNft, Nft, NftPriceHistory
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView, ListView


# Create your views here.
class ListCollectionView(View):
    """
    **ListCollectionView class**

    This view used to perform get request on Collection object to view the list of collection object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request):
        """
        Http get request use to Render create_collection template, categories and users.

        **Template:**

        `template:` admin_site/list-collection.html

        **Returns:**

        `render:` list-collection template and collection list

        """
        message = request.GET.get('message', None)
        collection_list = Collection.objects.all()
        filter_collection = CollectionFilter(request.GET, collection_list)
        collection_list = filter_collection.qs
        p = Paginator(collection_list.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'list_collection.html', {
            'collection_list': collection_list,
            "filter": filter_collection,
            'obj': obj,
            'message': message
        })


class SpecificDeleteCollection(View):

    def get(self, request, id, col_id):
        nft_obj = Nft.objects.get(id=id)
        nft_obj.delete()
        url = reverse(f'nft_management:detail-collection', kwargs={'id': col_id})
        url += "?message=Delete-Successfully/"
        return HttpResponseRedirect(url)


class DetailCollectionView(View):

    def get(self, request, id):
        collection_obj = Collection.objects.filter(id=id).first()
        message = request.GET.get('message', None)
        nft_obj = Nft.objects.filter(collection=id)
        myfilter = nftFilter(request.GET, queryset=nft_obj)
        nft_obj = myfilter.qs
        p = Paginator(nft_obj.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'view_collection.html', context={
            'collection_obj': collection_obj,
            'nft': nft_obj,
            'myfilter': myfilter,
            'obj': obj,
            'message': message
        })


class DeleteCollectionView(View):
    """
    **DeleteCollectionView class**

    This view used to perform get  request on Collection object to delete the Collection object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render list collection template after soft delete the collection.

        **Template:**

        `template:` admin_site/list-collection.html

        **Returns:**

        `HttpResponseRedirect:` collection list template

        """
        collection_object = Collection.objects.get(id=id)
        nft_objects = Nft.objects.filter(collection=id)
        for nft in nft_objects:
            nft.delete()
        collection_object.delete()
        url = reverse('nft_management:list-collection')
        url += "?message=Delete-Successfully/"
        return HttpResponseRedirect(url)


class CreateCategoryView(View):
    """
    **CreateCategoryView class**

    This view used to perform get and post request on Category object to create the Category object

    **Parameters**

    `View` : django.views

    """

    def post(self, request):
        """
        Http get request use to Render create_category template and categories list

        **Template:**

        `success-template:` admin_site/create-category.html

        **Returns:**

        ``render`` : `create category template, category list`

        """
        try:
            name = request.POST.get('name')
            category_obj = Category(name=name, is_active=True)
            category_obj.save()
            url = reverse('nft_management:list-category')
            url += "?message=Created-Successfully/"
            return HttpResponseRedirect(url)
        except Exception as e:
            url = reverse('nft_management:list-category')
            url += "?message=Already-Exist/"
            return HttpResponseRedirect(url)


class ListCategoryView(View):
    """
    **ListCategoryView class**

    This view used to perform get request on category object to view the list of categories object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request):
        """
        Http get request use to Render create_category template and category list

        **Template:**

        `template:` admin_site/list-collection.html

        **Returns:**

        `render:` list-category template and category list

        """
        message = request.GET.get('message', None)
        print(message)
        category_list = Category.objects.filter(is_removed=False)
        filter_category = CategoryFilter(request.GET, category_list)
        category_list = filter_category.qs
        p = Paginator(category_list.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'list_category.html', {
            'category_list': category_list,
            "filter": filter_category,
            'obj': obj,
            'message': message
        })


class DeleteCategoryView(View):
    """
    **DeleteCategoryView class**

    This view used to perform get request on Category object to delete the Category object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render list category template after soft delete the category.

        **Template:**

        `template:` admin_site/list-category.html

        **Returns:**

        `HttpResponseRedirect:` category list template

        """
        category_object = Category.objects.get(id=id)
        category_object.delete()
        url = reverse('nft_management:list-category')
        url += "?message=Delete-Successfully/"
        return HttpResponseRedirect(url)


class UpdateCategoryView(View):
    """
    *UpdateCategoryView class*

    This view used to perform get and post request on Category object to update the Collection object

    *Parameters*

    `View:`  django.views

    """

    def post(self, request, id):
        """
        Http post request use to Update an individual Collection object.

        *Template:*

        `success-template:` collection_app/list-collection.html

        `un-success-template:` collection_app/update-collection.html

        *Returns:*

        `HttpResponseRedirect` : 'if form is valid'

        `else` : render 'update collection template and objects used in collection creation'
        """
        try:
            category_object = Category.objects.get(pk=id)
            category_object.name = request.POST.get('name')
            is_active = False
            if request.POST.get('is_active_2'):
                is_active = True
            category_object.is_active = is_active
            category_object.save()
            url = reverse('nft_management:list-category')
            url += "?message=Updated-Successfully/"
            return HttpResponseRedirect(url)
        except Exception as e:
            url = reverse('nft_management:list-category')
            url += "?message=Already-Exist/"
            return HttpResponseRedirect(url)


class ListFavoritesNFTView(View):
    """
        **ListCollectionView class**

        This view used to perform get request on Collection object
        to view the list of collection object

        **Parameters**

        `View:`  django.views

        """

    def get(self, request):
        """
        Http get request use to Render create_collection template, categories and users.

        **Template:**

        `template:` admin_site/list-collection.html

        **Returns:**

        `render:` list-collection template and collection list

        """
        favorites_nft_list = FavouriteNft.objects.all()
        filter_favorites_nft = FavouriteNftFilter(request.GET, favorites_nft_list)
        favorites_nft_list = filter_favorites_nft.qs
        p = Paginator(favorites_nft_list.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'list_favorites_nft.html', {
            'favorites_nft_list': favorites_nft_list,
            "filter": filter_favorites_nft,
            'obj': obj
        })


class DeleteFavoritesNFTView(View):
    """
    **DeleteCategoryView class**

    This view used to perform get request on Category object to delete the Category object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render list category template after soft delete the category.

        **Template:**

        `template:` admin_site/list-category.html

        **Returns:**

        `HttpResponseRedirect:` category list template

        """
        favorites_nft_object = FavouriteNft.objects.get(id=id)
        favorites_nft_object.is_removed = True
        favorites_nft_object.save()
        url = reverse('nft_management:list-favorites-nft')
        return HttpResponseRedirect(url)


class ListReportedNFTView(View):
    """
    **ListCollectionView class**

    This view used to perform get request on Collection object
    to view the list of collection object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request):
        """
        Http get request use to Render create_collection template, categories and users.

        **Template:**

        `template:` admin_site/list-collection.html

        **Returns:**

        `render:` list-collection template and collection list

        """
        reported_nft_list = ReportedNft.objects.all()
        filter_reported_nft = ReportedNftFilter(request.GET, reported_nft_list)
        reported_nft_list = filter_reported_nft.qs
        p = Paginator(reported_nft_list.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)

        return render(request, 'list_reported_nft.html', {
            'reported_nft_list': reported_nft_list,
            "filter": filter_reported_nft,
            'obj': obj,
        })


class ResolveReportedNFTView(View):
    """
    **DeleteCategoryView class**

    This view used to perform get request on Category object to delete the Category object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render list category template after soft delete the category.

        **Template:**

        `template:` admin_site/list-category.html

        **Returns:**

        `HttpResponseRedirect:` category list template

        """
        reported_nft_object = ReportedNft.objects.get(id=id)
        reported_nft_object.delete()
        messages.success(request,'Reported Nft : Resolved Successfully')
        url = reverse('nft_management:list-reported-nft')

        return HttpResponseRedirect(url)


class NftListDisplay(View):
    model = Nft
    template_name = "nft-list.html"

    # template_name += "?message=Delete-Successfully/"

    def get(self, request):
        """
        Http get request use to Render create_collection template, categories and users.

        *Template:*


        `template:` collection_app/list-collection.html

        *Returns:*


        `render:` list-collection template and collection list

        """
        message = request.GET.get('message', None)

        nfts = Nft.objects.all().order_by('id')
        myfilter = nftFilter(request.GET, queryset=nfts)
        nftis = myfilter.qs
        p = Paginator(nftis.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'nft-list.html', {'nftis': nftis, 'myfilter': myfilter, 'obj': obj, 'message': message})


class NftUpdate(UpdateView):
    model = Nft
    fields = "__all__"
    template_name = "update_nft.html"

    def get_context_data(self, **kwargs):
        collection_obj = Collection.objects.all()
        user_obj = User.objects.all()
        context = super().get_context_data(**kwargs)
        context["collection_obj"] = collection_obj
        context["user_obj"] = user_obj

        return context


class NftCreate(View):
    model = Nft
    fields = "__all__"
    template_name = "create_nft.html"

    def get(self, request):
        collection_obj = Collection.objects.all()
        user_obj = User.objects.all()
        nft_obj = Nft.objects.all()
        context = {
            "collection_obj": collection_obj,
            "user_obj": user_obj,
            "nft_obj": nft_obj,
        }
        return render(request, "create_nft.html", context)

    def post(self, request):
        data = request.POST
        name = data["name"]
        description = data["description"]
        image = data["image"]
        royalty = data["royalty"]
        size = data["size"]
        no_of_copies = data["no_of_copies"]
        total_views = data["total_views"]
        sale_type = data["sale_type"]
        price = data["price"]
        collection = Collection.objects.get(id=int(data["collection"]))
        owner = User.objects.get(id=int(data["owner"]))

        nft = Nft(
            name=name,
            description=description,
            image=image,
            royalty=royalty,
            size=size,
            no_of_copies=no_of_copies,
            is_hidden=True,
            collection=collection,
            owner=owner,
            sale_type=sale_type,
            price=price,
        )
        nft.save()
        return redirect("nft_management:nfts_list")


class NftDelete(View):
    """
    *DeleteCategoryView class*

    This view used to perform get request on Category object to delete the Category object

    *Parameters*

    `View:`  django.views

    """

    def get(self, request, pk):
        """
        Http get request use to Render list category template after soft delete the category.

        *Template:*

        `template:` admin_site/list-category.html

        *Returns:*

        `HttpResponseRedirect:` category list template

        """
        nft_object = Nft.objects.get(pk=pk)
        # nft_object.is_removed = True
        # nft_object.save()
        nft_object.delete()
        url = reverse('nft_management:nfts_list')
        url += "?message=Delete-Successfully/"

        return HttpResponseRedirect(url)


class AddNftPriceHistory(View):
    model = NftPriceHistory
    templated_name = "nftprice_add.html"
    fields = "__all__"

    def get(self, request):
        nft_obj = Nft.objects.all()
        context = {"nft_obj": nft_obj}
        return render(request, "nftprice_add.html", context)

    def post(self, request):
        data = request.POST
        price = data["price"]
        is_active = request.POST.get("is_active", False)
        date = data["date"]
        nft = Nft.objects.get(id=int(data["nft"]))
        nft = Nft(is_active=is_active, nft=nft, date=date, price=price)
        nft.save()
        return HttpResponseRedirect("nft_management:price-history-list")


class DeletePriceHistory(DeleteView):
    model = NftPriceHistory
    template_name = "nftprice_delete.html"
    fields = "__all__"
    success_url = reverse_lazy("nft_management:price-history-list")


class PriceHistoryList(ListView):
    def get(self, request):
        """
        Http get request use to Render create_collection template, categories and users.

        *Template:*


        `template:` collection_app/list-collection.html

        *Returns:*


        `render:` list-collection template and collection list

        """
        nfts = NftPriceHistory.objects.all().order_by('id')
        myfilter = nphFilter(request.GET, queryset=nfts)
        npriceh = myfilter.qs
        p = Paginator(npriceh.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'nftprice_list.html', {'npricehs': npriceh, 'myfilter': myfilter, 'obj': obj})


class UpdateHistoryList(UpdateView):
    model = NftPriceHistory
    templated_name = "nftprice_list.html"
    fields = "__all__"
    success_url = reverse_lazy("nft_management:nfts_list")


class NftDetailView(View):
    """
    *Nft Detail class*

    This view used to perform get request on profile object to view the list of Nft

    *Parameters*

    `View:`  django.viewsgit

    """

    def get(self, request, id):
        """
        Http get request use to Render profiles template

        *Template:*

        `template:` admin_user/profiles.html

        *Returns:*

        `render:` profile template and user list

        """
        try:
            nft = Nft.objects.get(id=id)
            bids = nft.bidding_nft.all().order_by('id')
            p = Paginator(bids.order_by('id'), 5)
            page = request.GET.get('page',)
            obj = p.get_page(page)

            return render(request, 'nft_detail.html', {'nft': nft, 'bids': bids,'obj':obj})
        except Exception as e:
            return "Nft Doesn not Exist"


class LiveAuctionView(ListView):
    model = Nft
    fields = "__all__"
    template_name = 'live_auction.html'

    def get(self, request):
        """
        Http get request use to Render create_collection template, categories and users.

        *Template:*


        `template:` collection_app/list-collection.html

        *Returns:*


        `render:` list-collection template and collection list

        """
        nft = Nft.objects.all().order_by('id')
        myfilter = nftFilter(request.GET, queryset=nft)
        nftis = myfilter.qs
        p = Paginator(nftis.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'live_auction.html', {'nftis': nftis, 'myfilter': myfilter, 'obj': obj})


class ReportedNFTView(View):
    """
    *ListCollectionView class*

    This view used to perform get request on Collection object
    to view the list of collection object

    *Parameters*

    `View:`  django.views

    """

    def get(self, request):
        """
        Http get request use to Render create_collection template, categories and users.

        *Template:*

        `template:` admin_site/list-collection.html

        *Returns:*

        `render:` list-collection template and collection list

        """
        reported_nft_list = ReportedNft.objects.get(id=id)
        return render(request, 'reported_nft_view.html', {
            'reported_nft_list': reported_nft_list
        })