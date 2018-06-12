from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

def generate_jwt_token(user):
    """ Generate jwt token upon creation and login of a user """
    user_object = User.objects.get(pk=user['id'])
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user_object)
    token = jwt_encode_handler(payload)
    return token
