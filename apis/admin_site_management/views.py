from apis.Response.json_response import response_json
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
# Create your views here.
from ..bidding_and_transection.pagination import PaginationHandlerMixin


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 4


class FAQView(APIView):
    """FAQView class

    This view performs GET,PUT, DELETE operations for FAQ Model

    Parameters
    ----------
    APIView : rest_framework.views

    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]

    def get(self, request, pk):
        """HTTP GET request

        A HTTP endpoint that returns FAQ object for provided PK

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
            faq_obj = FAQ.objects.get(pk=pk)
            serializer = FAQSerializer(faq_obj)
            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except FAQ.DoesNotExist:
            return Response(
                response_json(message=f"FAQ does not exist against this id {pk}", status=False),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=FAQSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """HTTP PUT request

        A HTTP endpoint that updates a FAQ object for provided PK

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
            faqs = FAQ.objects.get(pk=pk)
            serializer = FAQSerializer(instance=faqs, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(response_json(message="FAQ updated successfully", data=serializer.data, status=True),
                                status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        """HTTP DELETE request

        A HTTP endpoint that deletes a FAQ for provided PK

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
            faqs = FAQ.objects.get(pk=pk)
            faqs.is_active = False
            faqs.save()
            return Response(
                response_json(message="FAQ deleted Successfully", status=True), status=status.HTTP_200_OK
            )
        except FAQ.DoesNotExist:
            return Response(
                response_json(message=f"FAQ does not exist this id {pk}", status=False),
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FAQListView(APIView, PaginationHandlerMixin):
    """FAQListView class

    This view performs POST and GET operations

    Parameters
    ----------
    APIView : rest_framework.views

    """

    #     def get_permissions(self):
    #         if self.request.method == "POST":
    #             return [permissions.AllowAny()]
    #         else:
    #             return [permissions.IsAdminUser()]

    @swagger_auto_schema(
        request_body=FAQSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """HTTP POST request

        A HTTP endpoint that saves a FAQ object  in DB

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
            data["updated_by"] = request.user.id
            serializer = FAQSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(response_json(message="FAQ inserted Successfully", data=serializer.data, status=True),
                                status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    pagination_class = BasicPagination
    serializer_class = FAQSerializer

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request):
        """HTTP GET request

        A HTTP endpoint that returns FAQ object list

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            faqs = FAQ.objects.filter(is_active=True)
            page = self.paginate_queryset(faqs)
            serializer = FAQSerializer(faqs, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(faqs, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContactAPIView(APIView):
    """ContactView class

    This view performs POST and GET operations

    Parameters
    ----------
    APIView : rest_framework.views
    """

    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        """HTTP GET request

        A HTTP endpoint that returns Contacts object for provided PK

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
            con_obj = Contact.objects.get(pk=pk)
            serializer = FAQSerializer(con_obj)
            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except FAQ.DoesNotExist:
            return Response(
                response_json(message=f"contact does not exist against this id {pk}", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=ContactSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """HTTP PUT request

        A HTTP endpoint that updates a Contacts object for provided PK

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
            contact = Contact.objects.get(pk=pk)
            serializer = ContactSerializer(contact, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Contacts updated successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Contact.DoesNotExist:
            return Response(
                response_json(message=f"Contact does not exist against this id {pk}", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        """HTTP DELETE request

        A HTTP endpoint that deletes a Contacts for provided PK

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
            contact = Contact.objects.get(pk=pk)
            contact.is_removed = True
            contact.save()
            return Response(
                response_json(message="Contact deleted Successfully", status=True), status=status.HTTP_200_OK
            )
        except Contact.DoesNotExist:
            return Response(
                response_json(message=f"Contact does not exist against this id {pk}", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContactListView(APIView, PaginationHandlerMixin):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAdminUser()]
        else:
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        request_body=ContactSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """HTTP POST request

        A HTTP endpoint that saves a Contacts object  in DB


        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            # data = request.data
            # data['resolved_by'] = request.user.id
            # print(request.user.id)
            serializer = ContactSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Contacts Inserted Successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    pagination_class = BasicPagination
    serializer_class = ContactSerializer

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request):
        """HTTP GET request

        A HTTP endpoint that returns Contacts objects list

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
            contact = Contact.objects.filter(is_removed=False)
            page = self.paginate_queryset(contact)
            serializer = ContactSerializer(contact, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(contact, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)

        except Contact.DoesNotExist:
            return Response(
                response_json(message="Contact does not exist", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
