from rest_framework.request import Request
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin


def auth_middleware(request):
    
    user = None
    try:
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        user = user_jwt[0]
        request.user = user
    except Exception as e:
        pass
    return user


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """ Middleware for authenticating JSON web token in Authorize Header """
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: auth_middleware(request))
