from django.contrib import messages
from django.contrib.messages import get_messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from settings.forms import SiteForm, SocialForm, PercentageForm
from settings.models import SiteSetting, SocialSetting, PercentageSetting
from settings.serializers import SiteSerializer, PercentageSerializer, SocialSerializer


# def site_setting(request, code='151'):
#     site_setting = SiteSetting.objects.get(code='151')
#     form = SiteForm(request.POST or None, instance=site_setting)
#     if form.is_valid():
#         form.save()
#         messages.success(request, ' Site-Setting updated successfully.')
#         messages.set_level(request, messages.INFO)
#         return redirect("settings:site")
#     return render(request, 'site.html', {'form': form})


# if form.is_update ():
#     form.save()
class UpdateSocialView(View):

    def get(self, request, code='151'):
        ss = SocialSetting.objects.get(code='151')
        social_form = SocialForm(instance=ss)
        return render(request, 'social.html', context={'form': social_form})

    def post(self, request, code='151'):
        instance = SocialSetting.objects.get(code='151')
        form_obj = SocialForm(request.POST, request.FILES, instance=instance)
        if form_obj.is_valid():
            form_obj.save()
            messages.success(request, 'social setting Updated Successfully..!!')

        url = reverse('settings:social')
        return HttpResponseRedirect(url)


# def social_setting(request, code='151'):
#     ss = SocialSetting.objects.get(code='151')
#     form = SocialForm(request.POST or None, instance=ss)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Social-Setting updated successfully.')
#         messages.set_level(request, messages.INFO)
#         return redirect("settings:social")
#     return render(request, 'social.html', {'form': form})


class UpdateSiteView(View):

    def get(self, request, code='151'):
        ss = SiteSetting.objects.get(code='151')
        site_form = SiteForm(instance=ss)
        return render(request, 'site.html', context={'form': site_form})

    def post(self, request, code='151'):
        instance = SiteSetting.objects.get(code='151')
        form_obj = SiteForm(request.POST, request.FILES, instance=instance)
        if form_obj.is_valid():
            form_obj.save()
            messages.success(request, 'site setting Updated Successfully..!!')

        url = reverse('settings:site')
        return HttpResponseRedirect(url)


# def percentage_setting(request, code='151'):
#     ps = PercentageSetting.objects.get(code='151')
#     form = PercentageForm(request.POST or None, instance=ps)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Percentage-Setting updated successfully.')
#         messages.set_level(request, messages.INFO)
#         return redirect("settings:percentage")
#     return render(request, 'percentage.html', {'form': form})


class UpdatePercentageView(View):

    def get(self, request, code='151'):
        ss = PercentageSetting.objects.get(code='151')
        site_form = PercentageForm(instance=ss)
        return render(request, 'percentage.html', context={'form': site_form})

    def post(self, request, code='151'):
        instance = PercentageSetting.objects.get(code='151')
        form_obj = PercentageForm(request.POST, request.FILES, instance=instance)
        if form_obj.is_valid():
            form_obj.save()
            messages.success(request, 'percentage setting Updated Successfully..!!')

        url = reverse('settings:percentage')
        return HttpResponseRedirect(url)


class SiteView(APIView):
    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request, code='151'):
        _object = SiteSetting.objects.get(code=code)
        serializer = SiteSerializer(_object)
        return Response(serializer.data, '200')


class SocialView(APIView):

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request, code='151'):
        _object = SocialSetting.objects.get(code=code)
        serializer = SocialSerializer(_object)
        return Response(serializer.data, '200')


class PercentageView(APIView):
    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request, code='151'):
        _object = PercentageSetting.objects.get(code=code)
        serializer = PercentageSerializer(_object)
        return Response(serializer.data, '200')
