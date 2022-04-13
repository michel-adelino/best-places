from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings  # for the secret key
import jwt
User = get_user_model()


class JWTAuthentication(BasicAuthentication):

    # Function is called automatically by Django as part of request pipeline
    def authenticate(self, request):

        # Get the authorization header (Bearer <token>)
        header = request.headers.get('Authorization')

        # If no header is present, return None which defaults to unauthenticated
        if not header:
            return None

        # If there is no bearer header present then raise a permission denied exception which will return a HTTP 403 status code
        if not header.startswith('Bearer'):
            raise PermissionDenied({'message': 'Invalid authorization header'})

        # Get the provided bearer token from the headers
        token = header.replace('Bearer ', '')

        # Try and decode the bearer token to extract the `sub` which is the user ID
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(pk=payload.get('sub'))  # sub = user ID

        # If the token cannot be decoded then we raise a permission denied exception which will return a HTTP 403 status code
        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied({'message': 'Invalid Token'})

        # If the user cannot be found then their account may have been deleted between last obtaining a token and now, raise permission denied exception and raise a HTTP 403 status code
        except User.DoesNotExist:
            raise PermissionDenied({'message': 'User not found'})

        # User has successfully authenticated return the user object and token as a tuple
        # They can now be accessed in views with `request.user` and `request.auth` respectively
        return (user, token)
