from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

def jwt_authentication(get_response):
    def middleware(request):
        user=None
        try:
            user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
            user = user_jwt[0]
            request.user = user
        except Exception as e:
            pass
        return get_response(request)
    return middleware

     



