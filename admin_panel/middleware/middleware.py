from django.http import HttpResponseRedirect
import re


class UserRestrictionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        regex = "/admin_site/"
        paths = re.search(regex, request.path)
        except_path = [
            '/admin_site/login/'
        ]
        if str(user) != 'AnonymousUser' or not (paths) or request.path.strip() in except_path:
            response = self.get_response(request)
            return response
        else:
            return HttpResponseRedirect('/admin_site/login')