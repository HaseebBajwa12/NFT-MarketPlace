from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.contrib import messages, auth
from django.views.generic.base import View


class LoginView(View):

    def get(self, request):
        context = {'error': None}
        return render(request, 'login.html', context=context)

    def post(self, request):
        data = request.POST
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            messages.warning(request, "Email or Password is invalid")
            context = {'error': 'Email or password is Invalid'}
            return render(request, 'login.html', context=context)
        elif user.is_superuser:
            login(request, user)
            url = reverse('admin_side:dashboard')
            return HttpResponseRedirect(url)
        else:
            messages.warning(request, "You have not permission to login in admin penal")
            context = {'error': 'Email or password is Invalid'}
            return render(request, 'login.html', context=context)


class LogoutView(View):

    def get(self, request):
        auth.logout(request)
        url = reverse('account:login')
        return HttpResponseRedirect(url)