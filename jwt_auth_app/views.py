from ast import If
from datetime import datetime, timedelta
import email
import jwt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings

from .serializers import UserSerializer

User = get_user_model()

# Create your views here.


class RegisterView(APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response({'message': 'Registration successful'})


class LoginView(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied({'message': 'Invalid credentials'})

        if not user.check_password(password):
            raise PermissionDenied({'message': 'Invalid credentials'})

        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode(
            {
                'sub': user.id,
                'exp': int(dt.strftime('%s'))
            },
            settings.SECRET_KEY,
            algorithm='HS256',
        )

        return Response({'token': token, 'message': f'So you\'re back {user.username}...'})
