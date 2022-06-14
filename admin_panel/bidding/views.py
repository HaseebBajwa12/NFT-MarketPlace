from django.contrib.admin.models import LogEntry
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import DeleteView
from apis.bidding_and_transection.models import Bidding, NftTransaction
from django.views import View
from .filters import BiddingFilter, BiddingTransactionFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


class BiddingdetailView(View):
    """
        *ListUerView class*

        This view used to perform get request on user object to view the list of user object

        *Parameters*

        `View:`  django.views

        """

    def get(self, request):
        """
        Http get request use to Render create_collection template, categories and users.

        *Template:*

        `template:` collection_app/list-collection.html

        *Returns:*

        `render:` list-collection template and collection list

        """
        message = request.GET.get('message', None)

        bidding_list = Bidding.objects.all().order_by('id')
        bidding_list = bidding_list.filter(status=True)
        bidding_count = bidding_list.count()
        myfilter = BiddingFilter(request.GET, queryset=bidding_list)
        bidding = myfilter.qs
        p = Paginator(bidding.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'bidding_index.html',
                      {'biddings': bidding,'message': message, 'myfilter': myfilter, 'obj': obj, 'bidding_count': bidding_count})


class DeleteBiddingView(View):
    def get(self, request, id):
        object = Bidding.objects.get(id=id)
        object.status = False
        object.save()
        url = reverse('bidding:bidding-list')
        url += "?message=Delete-Successfully/"
        return HttpResponseRedirect(url)


class TransactiondetailView(View):
    def get(self, request):
        message = request.GET.get('message', None)
        Transaction = LogEntry.objects.all().order_by('-id')
        Transaction = Transaction.filter()
        Transaction_count = Transaction.count()
        myfilter = BiddingTransactionFilter(request.GET, queryset=Transaction)
        transaction = myfilter.qs
        p = Paginator(transaction.order_by('-id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'nft_transaction_index.html',
                      {'transaction': transaction, 'message': message,'myfilter': myfilter, 'obj': obj, 'Transaction_count': Transaction_count})


class DeleteTransactionView(DeleteView):

    def get(self, request, id):
        object = NftTransaction.objects.get(id=id)
        object.is_removed = True
        object.save()
        url = reverse('bidding:Nft-transaction-list')
        url += "?message=Delete-Successfully/"
        return HttpResponseRedirect(url)


class TransactionView(View):
    def get(self, request,id):
        nft_transaction = NftTransaction.objects.get(id=id)
        return render(request, 'nfttransaction_view.html',
                      {'nft_transaction': nft_transaction})


class BiddingView(View):
    """
        *ListUerView class*

        This view used to perform get request on user object to view the list of user object

        *Parameters*

        `View:`  django.views

        """

    def get(self, request,id):
        """
        Http get request use to Render create_collection template, categories and users.

        *Template:*

        `template:` collection_app/list-collection.html

        *Returns:*

        `render:` list-collection template and collection list

        """
        bidding= Bidding.objects.get(id=id)
        return render(request, 'bidding_view.html',
                      {'bidding': bidding})
