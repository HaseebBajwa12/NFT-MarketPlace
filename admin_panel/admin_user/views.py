from accounts.models import User, Profile
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .filters import UserFilter
from .forms import ChangePass, UpdateProfileForm


# Create your views here.

class ListUserView(View):
    """
    **ListUerView class**

    This view used to perform get request on user object to view the list of user object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request):
        """
        Http get request use to Render home2 template,

        **Template:**

        `template:` admin_user/home2.html

        **Returns:**

        `render:` home2 template

        """
        message = request.GET.get('message', None)
        user = User.objects.all().order_by('id')
        user = user.filter(is_active=True)
        user_count = user.count()
        myfilter = UserFilter(request.GET, queryset=user)
        user = myfilter.qs
        p = Paginator(user.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'home2.html',
                      {'users': user, 'myfilter': myfilter, 'obj': obj, 'user_count': user_count, 'message': message

                       })


class DeleteUserView(View):
    """
    **DeleteUserView class**

    This view used to perform get  request on User object to delete the User object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render list User template after delete the user.

        **Template:**

        `template:` admin_user/home2.html

        **Returns:**

        `HttpResponseRedirect:` home2 template

        """
        object = User.objects.get(id=id)
        object.delete()

        #
        # if len(object.user_profile.all()) == 1:
        #     object2 = object.user_profile.all()[0]
        #
        #     object2.delete()
        # object.delete()
        url = reverse('admin_user:home')
        url += "?message=Delete-Successfully/"
        return HttpResponseRedirect(url)


class ListUserProfileView(View):
    """
    **ListCollectionView class**

    This view used to perform get request on profile object to view the list of profile object

    **Parameters**

    `View:`  django.viewsgit

    """

    def get(self, request, id):
        """
        Http get request use to Render profiles template

        **Template:**

        `template:` admin_user/profiles.html

        **Returns:**

        `render:` profile template and user list

        """
        try:
            profile = Profile.objects.get(user_id=id)
            user_obj = User.objects.get(id=id)

            return render(request, 'profile_view.html', {'profile': profile, 'user_obj': user_obj})
        except Exception as e:
            print(e)
            print('in except')
            profile = Profile()
            user_obj = User.objects.get(id=id)
            return render(request, 'profile_view.html', {'profile': profile, 'user_obj': user_obj})


def change_pass(request):
    if request.method == 'POST':
        fm = ChangePass(user=request.user, data=request.POST)
        print(request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(request, ' Password    Changed Successfully..!!')
            return HttpResponseRedirect('/admin_site/login/')

    else:

        fm = ChangePass(user=request.user)
    return render(request, 'change_pass.html', {'form': fm})


class UpdateProfileView(View):

    def get(self, request, id):
        pi = Profile.objects.get(user_id=id)
        profile_form = UpdateProfileForm(instance=pi)
        return render(request, 'update.html', context={'form': profile_form, 'id': id})

    def post(self, request, id):
        instance = Profile.objects.get(user_id=id)
        form_obj = UpdateProfileForm(request.POST, request.FILES, instance=instance)
        if form_obj.is_valid():
            form_obj.save()
            messages.success(request, 'Profile Updated Successfully..!!')

        url = reverse('admin_user:profiles_view', kwargs={'id': id})
        return HttpResponseRedirect(url)
