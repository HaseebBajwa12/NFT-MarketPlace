from apis.Response.json_response import response_json
from django.db.models import Value as V
from django.db.models.expressions import F
from django.db.models.functions import Concat
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .pagination import PaginationHandlerMixin
from .serializers import BiddingSerializer, NftTranactionSerializer


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 4


class BiddingView(APIView):
    """BiddingView class

   This view performs GET operation for specific bid

   Parameters
   ----------
   APIView : rest_framework.views

    """

    # permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        """HTTP GET request

         A HTTP endpoint that returns Bid object for provided PK

         Parameters
         ----------
         request : django.http.request

         pk : integer

         Returns
         -------
         rest_framework.response
             returns HTTP 200 status if data returned successfully,error message otherwise
         """
        try:
            bid_obj = Bidding.objects.get(pk=pk)
            serializer = BiddingSerializer(bid_obj)
            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Bidding.DoesNotExist:
            return Response(response_json(message=f"Bidding does not exist against this id {pk}", status=False),
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BiddingListView(APIView, PaginationHandlerMixin):
    """BiddingList class

    This view performs GET ,POST operation for Bidding Model

    Parameters
    ----------
    APIView : rest_framework.views

   """

    # permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        request_body=BiddingSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """HTTP POST request

         A HTTP endpoint that saves a Bidding object  in DB


         Parameters
         ----------
         request : django.http.request

         Returns
         -------
         rest_framework.response
             returns success message if data saved successfully,error message otherwise
        """
        try:
            serializer = BiddingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_json(message="Bidding added successfully", data=serializer.data, status=True),
                                status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    pagination_class = BasicPagination
    serializer_class = BiddingSerializer

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request, format=None):
        """HTTP GET request

             A HTTP endpoint that returns Bid object list

             Parameters
             ----------
             request : django.http.request

             Returns
             -------
             rest_framework.response
                 returns HTTP 200 status if data returned successfully,error message otherwise
             """
        try:
            bid = Bidding.objects.all()
            page = self.paginate_queryset(bid)
            serializer = BiddingSerializer(bid, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(bid, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NftTransactionView(APIView, PaginationHandlerMixin):
    """NftTransactionView class

      This view performs GET,POST operations for NftTransaction Model

      Parameters
      ----------
      APIView : rest_framework.views

       """

    @swagger_auto_schema(
        request_body=NftTranactionSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """HTTP POST request

       A HTTP endpoint that saves a NftTransaction object  in DB
       Parameters
       ----------
       request : django.http.request

       Returns
       -------
       rest_framework.response
           returns success message if data saved successfully,error message otherwise
      """
        try:
            serializer = NftTranactionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="NFT Transection is successfull", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    pagination_class = BasicPagination
    serializer_class = NftTranactionSerializer

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request):
        """HTTP GET request

        A HTTP endpoint that returns NftTransaction object list

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            trans_obj = NftTransaction.objects.all()
            page = self.paginate_queryset(trans_obj)
            serializer = NftTranactionSerializer(trans_obj, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(trans_obj, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)

            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NftTransactionDetail(APIView):

    def get(self, request, pk):
        """HTTP GET request

         A HTTP endpoint that returns NftTransaction object for provided PK

         Parameters
         ----------
         request : django.http.request

         pk : integer


         Returns
         -------
         rest_framework.response
             returns HTTP 200 status if data returned successfully,error message otherwise
         """
        try:
            trans_obj = NftTransaction.objects.get(pk=pk)
            serializer = NftTranactionSerializer(trans_obj)
            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except NftTransaction.DoesNotExist:
            return Response(
                response_json(message=f"Nft transaction detail doesn't exist against this id{pk}", status=False),
                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def bidding_nft_data(request, id):
    """
    Parameters: request
    ----------
    request: GET

    Returns: bidding  data object
    -------
    """
    try:
        bidding_data = Nft.objects.filter(id=id).annotate(bidding_price=F('bidding_nft__price'),
                                                          offer_by=Concat("bidding_nft__offer_by__first_name", V(' '),
                                                                          "bidding_nft__offer_by__last_name"),
                                                          bidding_date=F('bidding_nft__bidding_date'),
                                                          status=F('bidding_nft__status'),
                                                          bid_expiry_date=F("bidding_nft__expiry_date"),
                                                          profile_image=F('owner__user_profile__profile_image'),
                                                          user_id=F('bidding_nft__offer_by__id'),
                                                          nft_id=F('id')).values('nft_id',
            'name',
            'description',
            'image',
            'collection',
            'owner',
            'offer_by',
            'bidding_date',
            'bidding_price',
            'status',
            'profile_image',
            'user_id'
        )
        return Response({"bidding_data": bidding_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
