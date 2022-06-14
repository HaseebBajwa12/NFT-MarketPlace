from datetime import datetime

from apis.Response.json_response import response_json
# from apis.nft_management.paginate import paginate
from apis.user_management.pagination import PaginationHandlerMixin
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .paginate import CustomPagination
from .serializers import NFTSerializer, CollectionSerializer, CategorySerializer, FavouriteNftSerializer, \
    ReportedNftSerializer, CollectionNftSerializer, LiveAuctionSerializer


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 4


class NFTCreateView(APIView):
    """
    NFTCreateView class

    This view performs POST operation for NFT

    Parameters
    ----------
    APIView : rest_framework.views

    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=NFTSerializer,

        responses={
            201: "CREATED",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """HTTP POST request

        An HTTP endpoint that saves a NFT object in DB

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """

        try:
            data = request.data
            data['owner'] = request.user.id
            serializer = NFTSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(response_json(message="NFT created Successfully", data=serializer.data, status=True),
                                status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NFTManagementView(APIView):
    """
    NFTManagementView class

    This view performs PUT & Delete operation for NFT

    Parameters
    ----------
    APIView : rest_framework.views

    """

    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(
        request_body=NFTSerializer,

        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """
        HTTP PUT request

        An HTTP endpoint that updates a NFT object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        -------
        rest_framework.response
            returns success message if data updated successfully,error message otherwise
        """
        try:
            nft_object = Nft.objects.get(pk=pk)
            serializer = NFTSerializer(nft_object, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(response_json(message="NFT Updated Successfully", data=serializer.data, status=True),
                                status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Nft.DoesNotExist:
            return Response(response_json(message=f"NFT does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        """
        HTTP DELETE request

        An HTTP endpoint that deletes a NFT object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        -------
        rest_framework.response
            returns success message if data deleted successfully,error message otherwise
        """
        try:
            nft = Nft.objects.get(pk=pk)
            nft.is_removed = True
            nft.save()
            return Response(response_json(message="NFT deleted Successfully", status=True), status=status.HTTP_200_OK)

        except Nft.DoesNotExist:
            return Response(response_json(message=f"NFT does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NFTView(APIView):
    """
    NFTView Class

    This view performs GET operation for NFT

    Parameters
    ----------
    APIView : rest_framework.views

    """

    def get(self, request, pk):
        """
        HTTP GET request

        An HTTP endpoint that returns NFT object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        ---------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            nft_object = Nft.objects.get(pk=pk)
            serializer = NFTSerializer(nft_object)
            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Nft.DoesNotExist:
            return Response(response_json(message=f"NFT does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NFTListView(APIView, PaginationHandlerMixin):
    """
    NFTListView Class

    This view performs GET operation for NFT

    Parameters
    ----------
    APIView : rest_framework.views

    """

    pagination_class = BasicPagination
    serializer_class = NFTSerializer

    def get(self, request, *args, **kwargs):
        """
        HTTP GET request

        An HTTP endpoint that returns all NFT objects

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            nft = Nft.objects.filter(is_removed=False)
            page = self.paginate_queryset(nft)
            serializer = NFTSerializer(nft, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(nft, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateCollectionView(APIView):
    """
    CreateCollectionView Class

    This view performs POST operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views

    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CollectionSerializer,
        responses={
            201: "CREATED",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        HTTP POST request

        An HTTP endpoint that saves a collection object in DB

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = CollectionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Collection created Successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionManagementView(APIView):
    """
    CollectionManagementView Class

    This view performs PUT & Delete operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views

    """

    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(
        request_body=CollectionSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """
        HTTP PUT request

        An HTTP endpoint that updates a Collection object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        -------
        rest_framework.response
            returns success message if data updated successfully,error message otherwise
        """
        try:
            collection_obj = Collection.objects.get(pk=pk)
            serializer = CollectionSerializer(collection_obj, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Collection updated successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Collection.DoesNotExist:
            return Response(response_json(message=f"collection does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        """
        HTTP DELETE request

        An HTTP endpoint that deletes a Collection object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        -------
        rest_framework.response
            returns success message if data deleted successfully,error message otherwise
        """
        try:
            coll_obj = Collection.objects.get(pk=pk)
            coll_obj.is_removed = True
            coll_obj.save()
            return Response(response_json(message="collection deleted Successfully", status=True),
                            status=status.HTTP_200_OK)

        except Collection.DoesNotExist:
            return Response(response_json(message=f"collection does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionView(APIView):
    """
    CollectionView Class

    This view performs GET operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views

    """

    def get(self, request, pk):
        """
        HTTP GET request

        An HTTP endpoint that returns collection object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        ---------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            collection = Collection.objects.get(pk=pk)
            serializer = CollectionNftSerializer(collection)
            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            return Response(response_json(message=f"Collection does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionListView(APIView, PaginationHandlerMixin):
    """
    CollectionListView Class

    This view performs GET operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views

    """
    pagination_class = BasicPagination
    serializer_class = CollectionSerializer

    def get(self, request, *args, **kwargs):
        """
        HTTP GET request

        An HTTP endpoint that returns all Collection objects

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            collection = Collection.objects.filter(is_removed=False)
            page = self.paginate_queryset(collection)
            serializer = CollectionSerializer(collection, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(collection, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryCreateView(APIView):
    """
    CategoryCreateView Class

    This view performs POST operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views
    """

    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            201: "CREATED",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        HTTP POST request

        An HTTP endpoint that saves a Category object in DB

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            serializer = CategorySerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Category created successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryManagementView(APIView):
    """
    CategoryManagementView Class

    This view performs PUT & Delete operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views

    """

    # permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """
        HTTP PUT request

        An HTTP endpoint that updates a category object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        -------
        rest_framework.response
            returns success message if data updated successfully,error message otherwise
        """
        try:
            cata_obj = Category.objects.get(pk=pk)
            serializer = CategorySerializer(cata_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Category updated successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response(response_json(message=f"category does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk, format=None):
        """
        HTTP DELETE request

        An HTTP endpoint that deletes a Category object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        -------
        rest_framework.response
            returns success message if data deleted successfully,error message otherwise
        """
        try:
            cata_obj = Category.objects.get(pk=pk)
            cata_obj.is_removed = True
            cata_obj.save()
            return Response(response_json(message="Category deleted Successfully", status=True),
                            status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return Response(response_json(message=f" category does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryView(APIView):
    """
    CategoryView Class

    This view performs GET operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views
    """

    def get(self, request, pk):
        """
        HTTP GET request

        An HTTP endpoint that returns category object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        ---------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            cat_obj = Category.objects.get(pk=pk)
            serializer = CategorySerializer(cat_obj)
            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response(response_json(message=" Category does not exist", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryListView(APIView):
    """
    CategoryListView Class

    This view performs GET operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views
    """

    def get(self, request):
        """
        HTTP GET request

        An HTTP endpoint that returns all Category objects

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """

        try:
            cat_obj = Category.objects.filter(is_removed=False)
            serializer = CategorySerializer(cat_obj, many=True)

            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavouritesNftView(APIView, PaginationHandlerMixin):
    """
    FavouriteNFTList Class

    This view performs POST, GET & Delete operations on Favourite NFT object

    Parameters
    ----------
    APIView : rest_framework.views
    """

    @swagger_auto_schema(
        request_body=FavouriteNftSerializer,

        responses={
            201: "Created",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        HTTP POST request

        An HTTP endpoint that saves a Favourite Item object in DB

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            serializer = FavouriteNftSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Favourite NFT Created Successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    pagination_class = BasicPagination
    serializer_class = FavouriteNftSerializer

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request):
        """
        HTTP GET request

        An HTTP endpoint that returns all Favourite Item objects

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            favourite_nft = Nft.objects.filter(
                id__in=FavouriteNft.objects.filter(
                    user=request.user.id
                ).values_list('id')
            )
            print(favourite_nft)
            page = self.paginate_queryset(favourite_nft)
            serializer = FavouriteNftSerializer(favourite_nft, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(favourite_nft, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except FavouriteNft.DoesNotExist:
            return Response(response_json(message="No Favourite NFTs", status=False),
                            status=status.HTTP_400_BAD_REQUEST)


class FavouritesNFTDeleteView(APIView):
    """
    FavouritesNFTDeleteView Class

    This view performs Delete operation for favourites object

    Parameters
    ----------
    APIView : rest_framework.views
    """

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        """
        HTTP DELETE request

        An HTTP endpoint that deletes a Favourite Item object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        -------
        rest_framework.response
            returns success message if data deleted successfully,error message otherwise
        """
        try:
            fav_obj = FavouriteNft.objects.get(pk=pk)
            fav_obj.is_removed = True
            fav_obj.save()
            return Response(response_json(message="Favorite NFT deleted", status=True), status=status.HTTP_200_OK)
        except FavouriteNft.DoesNotExist:
            return Response(response_json(message=f"Favourite NFT does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportedNFTCreateView(APIView):
    """
    ReportedNFTCreateView Class

    This view performs POST operation for reported NFT object

    Parameters
    ----------
    APIView : rest_framework.views
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ReportedNftSerializer,

        responses={
            201: "CREATED",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        HTTP POST request

        An HTTP endpoint that saves a reported NFT object in DB

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            data = request.data
            data['reporter'] = request.user.id
            serializer = ReportedNftSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Reported NFT created successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportedNFTListView(APIView, PaginationHandlerMixin):
    """
    ReportedNFTListView Class

    This view performs GET operation for reported NFT object

    Parameters
    ----------
    APIView : rest_framework.views
    """

    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
    serializer_class = ReportedNftSerializer

    def get(self, request):
        """
        HTTP GET request

        An HTTP endpoint that returns all Reported NFT objects

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            reported_nft_obj = ReportedNft.objects.filter(is_resolved=False, is_removed=False)
            page = self.paginate_queryset(reported_nft_obj)
            serializer = ReportedNftSerializer(reported_nft_obj, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(reported_nft_obj, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)

        except ReportedNft.DoesNotExist:
            return Response(response_json(message="Reported Nft does not exist", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportedNFTView(APIView):
    """
    ReportedNFTView Class

    This view performs GET operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views
    """

    def get(self, request, pk):
        """
        HTTP GET request

        An HTTP endpoint that returns reported NFT object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        ---------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            reported_nft_obj = ReportedNft.objects.get(pk=pk)
            serializer = ReportedNftSerializer(reported_nft_obj)
            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)

        except ReportedNft.DoesNotExist:
            return Response(response_json(message=f" Category does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportedNFTDeleteView(APIView):
    """
    ReportedNFTDeleteView Class

    This view performs Delete operation for collection object

    Parameters
    ----------
    APIView : rest_framework.views
    """

    @swagger_auto_schema(

        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        """
        HTTP DELETE request

        An HTTP endpoint that deletes a Reported NFT object for provided PK

        Parameters
        ----------
        request : django.http.request

        pk : integer

        Returns
        -------
        rest_framework.response
            returns success message if data deleted successfully,error message otherwise
        """
        try:
            reported_nft = ReportedNft.objects.get(pk=pk)
            reported_nft.is_removed = True
            reported_nft.save()
            return Response(response_json(message="Reported NFT Deleted Successfully", status=True),
                            status=status.HTTP_200_OK)

        except ReportedNft.DoesNotExist:
            return Response(response_json(message=f"Reported NFT does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def top_sellers(request, *args, **kwargs):
    """

    Parameters: request
    ----------
    request: GET

    Returns: top sellers list
    -------

    """
    paginator = CustomPagination()
    try:

        top_selling = Nft.objects.values('owner__id').annotate(Sum('price')).order_by('-price__sum')
        records = []
        for record in top_selling:
            user = User.objects.get(id=record['owner__id'])
            profiles = user.user_profile.profile_image.url
            records.append({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_image": "" if profiles is None else profiles,
                "price": record['price__sum'],
                "id": record['owner__id']
            })

        context = paginator.paginate_queryset(records, request)
        return paginator.get_paginated_response(context, result_key="top_seller")
        # return Response(response_json(data={"top_sellers": records}, status=True),
        #                 status=status.HTTP_200_OK)
    except Exception as e:
        return Response(response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def users_nft_data(request, id, *args, **kargs):
    """

    Parameters: request
    ----------
    request: GET

    Returns: user data object
    -------

    """
    paginator = CustomPagination()
    try:

        user_data = User.objects.filter(
            id=id).annotate(user_id=F(
            "id"),
            user_name=F(
                "first_name"),
            user_email=F('email'),
            nft_name=F('nft_owner__name'),
            nft_description=F(
                'nft_owner__description'),
            nft_image=F(
                'nft_owner__image'), collection_name=F('user_collection__name'),
            collection_description=F('user_collection__description'),
            collection_logo=F('user_collection__logo_image'),
            collection_image=F('user_collection__banner_image'),
            collection_id=F('user_collection__id'), nft_id=F(
                'nft_owner__id'), nft_price=F(
                'nft_owner__price'), nft_size=F(
                'nft_owner__size'), banner_image=F('user_profile__profile_image'),
            profile_image=F('user_profile__profile_image'),
            facebook_link=F('user_profile__facebook_link'),
            twitter_link=F('user_profile__twitter_link'),
            google_plus_link=F('user_profile__google_plus_link'),
            vine_link=F('user_profile__vine_link')).values(
            'user_name',
            'user_id',
            'user_email',
            'nft_name',
            'nft_description',
            'nft_image',
            'banner_image',
            'profile_image', 'facebook_link',
            'twitter_link', 'google_plus_link',
            'vine_link', 'is_active',
            'collection_name',
            'collection_description',
            'collection_logo', 'collection_image', 'collection_id', 'nft_id',
            'nft_price', 'nft_size').distinct()

        context = paginator.paginate_queryset(user_data, request)
        return paginator.get_paginated_response(context, result_key="user_data")
        # return Response(response_json(data={"pagination": pagination, "user_data": user_data}, status=True),
        #                 status=status.HTTP_200_OK)
    except Exception as e:
        return Response(response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LiveAuction(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = LiveAuctionSerializer

    def get(self, request):
        """
        HTTP GET request

        An HTTP endpoint that returns all Reported NFT objects

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            # today = date.today()
            # y = today.year + 20
            # m = today.month
            # d = today.day
            # ff = f"{m}/{d}/{y}"
            # future = datetime.strptime(ff, '%m/%d/%Y').date()
            current_date = datetime.now().strftime("%Y-%m-%d")

            nft_obj = Nft.objects.filter(is_removed=False, sale_type="is_put_on_sale", expiry_date__gt=current_date)
            page = self.paginate_queryset(nft_obj)
            serializer = LiveAuctionSerializer(nft_obj, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(nft_obj, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def category_collection_data(request, id, *args, **kargs):
    print(request, args, kargs)
    print(request.query_params)
    """

    Parameters: request
    ----------
    request: GET

    Returns: category data object
    -------
    """
    paginator = CustomPagination()
    try:

        if id > 0:
            category_data = Category.objects.filter(id=id).annotate(
                collection_name=F(
                    "collection_category__name"),
                logo_image=F('collection_category__logo_image'),
                banner_image=F('collection_category__banner_image'),
                description=F('collection_category__description'),
                collection_id=F('collection_category__id'),

            ).values('id',
                     'name',
                     'collection_name',
                     'logo_image',
                     'banner_image',
                     'description',
                     'is_active', 'collection_id')

            context = paginator.paginate_queryset(category_data, request)
            return paginator.get_paginated_response(context, result_key="category_data")
            # return Response(response_json(data={"pagination": pagination, "category_data": category_data}, status=True),
            #                 status=status.HTTP_200_OK)

        category_data = Collection.objects.filter(is_removed=False).annotate(
            user_name=F(
                "user__first_name"), collection_name=F('name')

        ).values('id',
                 'collection_name',
                 'logo_image',
                 'banner_image',
                 'description',
                 'user_name',
                 )

        context = paginator.paginate_queryset(category_data, request)
        return paginator.get_paginated_response(context, result_key="category_data")
        # return Response(response_json(data={"pagination": pagination, "category_data": category_data}, status=True),
        #                 status=status.HTTP_200_OK)
    except Exception as e:
        return Response(response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def user_collection(request, pk, *args, **kargs):
    """
    Parameters: request
    ----------
    request: GET

    Returns: user data object
    -------

    """
    paginator = CustomPagination()
    try:

        user_data = User.objects.filter(pk=pk).annotate(collection_name=F('user_collection__name'),
                                                        logo_image=F('user_collection__logo_image'),
                                                        banner_image=F('user_collection__banner_image'),
                                                        collection_description=F('user_collection__description'),
                                                        collection_id=F('user_collection__id'),

                                                        category_name=F('user_collection__category__name'),
                                                        user_name=F('user_collection__user__first_name'),
                                                        user_id=F('id')).values('user_id',
                                                                                "collection_name",
                                                                                "logo_image",
                                                                                "banner_image",
                                                                                "collection_description",
                                                                                "category_name",
                                                                                "user_name", 'collection_id')

        context = paginator.paginate_queryset(user_data, request)
        return paginator.get_paginated_response(context, result_key="user_collection")

        # return Response(response_json(data={"pagination": pagination, "user_collection": user_data}, status=True),
        #                 status=status.HTTP_200_OK)
    except Exception as e:
        return Response(response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
