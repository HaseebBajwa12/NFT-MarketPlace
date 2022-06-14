from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apis.Response.json_response import response_json
from .models import *
from .serializers import WalletSerializer
from ..bidding_and_transection.pagination import PaginationHandlerMixin
from ..bidding_and_transection.views import BasicPagination


class WalletAPI(APIView):
    def get(self, request, pk):
        try:
            wall_obj = Wallet.objects.get(pk=pk)
            serializer = WalletSerializer(wall_obj)
            return Response(response_json(data=serializer.data,status=True), status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response(response_json(message=f"Wallet does not exist against this id {pk}",status=False), status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(response_json(message=e.args[0],status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=WalletSerializer,

        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        try:
            wal_obj = Wallet.objects.get(pk=pk)
            serializer = WalletSerializer(wal_obj, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_json(message="wallet updated successfully",data=serializer.data,status=True), status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response(response_json(message=f"Wallet does not exist against this id {pk}",status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message= e.args[0],status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        try:
            wall_obj = Wallet.objects.get(pk=pk)
            wall_obj.delete()
            return Response(response_json(message= "Wallet deleted Successfully",status=True), status=status.HTTP_200_OK)

        except Wallet.DoesNotExist:
            return Response(response_json(message=f"Wallet does not exist against this id {pk}",status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletListView(APIView, PaginationHandlerMixin):
    @swagger_auto_schema(
        request_body=WalletSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        try:
            serializer = WalletSerializer(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_json(message="Wallet Created successfully",data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors,status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    pagination_class = BasicPagination
    serializer_class = WalletSerializer

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request):
        try:
            wallet_obj = Wallet.objects.all()
            page = self.paginate_queryset(wallet_obj)
            serializer = WalletSerializer(wallet_obj, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(wallet_obj, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
