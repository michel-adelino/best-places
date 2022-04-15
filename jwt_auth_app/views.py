from ast import If
from datetime import datetime, timedelta
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
