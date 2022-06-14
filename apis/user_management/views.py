import requests
from accounts.models import *
from apis.Response.json_response import response_json
#from apis.nft_management.paginate import paginate
from django.db.models import F
# from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
# from .pagination import MyPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apis.nft_management.paginate import CustomPagination

from .pagination import PaginationHandlerMixin
from .serializers import PasswordResetSerializer, UserDetailSerializer, CustomUserSerializer, UserProfileSerializer
from .serializers import ProfileSerializer


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 4


class UserActivationView(APIView):
    def get (self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/auth/users/activation/"
        print("post ulr",post_url)
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data = post_data)
        content = result.text
        return Response(content)


@api_view(['GET'])
def activate_user_view(request, uid, token):
    post_url = "https://nft-marketeplace-fkg7q.ondigitalocean.app/api/auth/users/activation/"
    # post_url = 'http://127.0.0.1:8000/api/auth/users/activation/'
    post_data = {"uid": uid, "token": token}
    print(post_url)
    print(post_data)
    result = requests.post(post_url, data=post_data)
    print(result)
    message = "Account activate successfully" if (
            result.status_code == 200 or result.status_code == 204) else "Account activation failed"
    return Response(response_json(message=message, status=True), str(result.status_code))


@api_view(['POST'])
def password_reset_view(request, uid, token):
    data = request.data
    serializer = PasswordResetSerializer(data=data)
    if serializer.is_valid():
        post_url = "https://nft-marketeplace-fkg7q.ondigitalocean.app/api/auth/users/reset_password_confirm/"
        post_data = {"uid": uid, "token": token, 'new_password': data['password']}
        result = requests.post(post_url, data=post_data)
        content = result.text
        return Response(response_json(data={"content": content, "result": result}, status=True), '200')
    else:
        return Response(response_json(data=serializer.errors, status=False), '400')


class LogoutAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: "OK",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(response_json(message="Logout Successfully", status=True), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response_json(message="Something Went wrong", status=False),
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileManagement(APIView):
    """ProfileVManagementView class

      This view performs GET,POST operations for Profile Model

      Parameters
      ----------
      APIView : rest_framework.views

       """

    # permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        """HTTP GET request

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
            prof_obj = User.objects.get(pk=pk)
            serializer = CustomUserSerializer(prof_obj)
            return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(response_json(message=f"Profile does not exist against this id {pk}", status=False),
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=ProfileSerializer,

        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """HTTP PUT request

          A HTTP endpoint that updates a Profile object for provided PK

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
            profile_obj = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile_obj)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Profile updated successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        except Profile.DoesNotExist:
            return Response(response_json(message=f"Profile does not exist against this id {pk}", status=False),
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
        """HTTP DELETE request

         A HTTP endpoint that deletes a Profile for provided PK

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
            nft = Profile.objects.get(pk=pk)
            nft.delete()
            return Response(response_json(message="Profile deleted successfully", status=True),
                            status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(response_json(message=f"Profile does not exist against this id {pk}", status=False),
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateProfile(APIView):
    permission_classes = [IsAuthenticated]
    """CreateProfileView class

      This view performs GET,POST operations for Profile Model

      Parameters
      ----------
      APIView : rest_framework.views

       """

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """HTTP POST request

         A HTTP endpoint that saves a Profile object  in DB


         Parameters
         ----------
         request : django.http.request

         Returns
         -------
         rest_framework.response
             returns success message if data saved successfully,error message otherwise
        """
        try:
            user = request.user
            serializer = CustomUserSerializer(data=request.data, instance=user)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_json(message="Profile Created successfully", data=serializer.data, status=True),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetProfileList(APIView, PaginationHandlerMixin):
    """ProfileView class

     This view performs GET operations

     Parameters
     ----------
     APIView : rest_framework.views
     """

    pagination_class = BasicPagination
    serializer_class = ProfileSerializer

    # permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request, format=None, *args, **kwargs):
        """HTTP GET request

              A HTTP endpoint that returns Profile objects list

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
            profile = Profile.objects.all()
            page = self.paginate_queryset(profile)
            serializer = ProfileSerializer(profile, many=True)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
            else:
                serializer = self.serializer_class(profile, many=True)
                return Response(response_json(data=serializer.data, status=True), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response_json(message=e.args[0], status=False),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailView(ListAPIView):
    """
    API for User Details with NFT,Collection and user profie
    """
    model = User
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        return User.objects.all()


@api_view(['GET'])
def users_profile_list(request, *args, **kargs):
    """

    Parameters
    ----------
    request

    Returns: users object
    -------

    """
    paginator = CustomPagination()
    try:

        user_obj = Profile.objects.filter(is_removed=False).annotate(first_name=F('user__first_name'),
                                                                     users_id=F("user__id"),
                                                                     last_name=F('user__last_name')).values(
            "profile_image", 'user_id', 'banner_image', 'profile_image', "id", 'first_name', 'last_name',
            'about', 'facebook_link', 'twitter_link', 'vine_link', 'google_plus_link')

        context = paginator.paginate_queryset(user_obj, request)
        return paginator.get_paginated_response(context, result_key="user_profile")
        # return Response(response_json(data={"pagination": pagination, "user_profile": user_obj}, status=True),
        #                 status=status.HTTP_200_OK)
    except Exception as e:
        return Response(response_json(message=e.args[0], status=False), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserProfileSerializer,

        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """HTTP PUT request

          A HTTP endpoint that updates a Profile object for provided PK

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
            user = User.objects.get(pk=pk)
            data = request.data
            serializer = UserProfileSerializer(data=data)
            if serializer.is_valid():

                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.username = data['username']
                user.save()
                profile = Profile.objects.filter(user=pk).first()
                if 'profile_image' in data.keys():
                    profile.profile_image = data['profile_image']
                if 'banner_image' in data.keys():
                    profile.banner_image = data['banner_image']
                profile.facebook_link = data['facebook_link']
                profile.twitter_link = data['twitter_link']
                profile.google_plus_link = data['google_plus_link']
                profile.vine_link = data['vine_link']
                profile.about = data['about']

                profile.save()
                return Response(
                    response_json(data=serializer.data, status=True, message="Profile Updated Successfully"),
                    status=status.HTTP_200_OK)
            else:
                return Response(response_json(data=serializer.errors, status=False, message="Something went Wrong"),
                                status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response(response_json(message=f"Profile does not exist against this id {pk}", status=False),
                            status=status.HTTP_400_BAD_REQUEST)
