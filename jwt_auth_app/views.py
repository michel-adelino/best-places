from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from .serializers import UserSerializer, UserWithCitiesSelializer

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


class CredentialsView(APIView):

    permission_classes = [IsAuthenticated, ]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)


# END OF AUTH VIEWS


class UserList(APIView):

    # Restricts the view to Admins only
    # permission_classes = [IsAdminUser, ]

    # List users
    def get(self, request):

        # Load all users from the db
        users = User.objects.all()

        # Serialize all users (many=True) to JSON
        serialized_users = UserSerializer(users, many=True)
        return Response(data=serialized_users.data, status=status.HTTP_200_OK)


class UserRetrieve(APIView):
    def get(self, request, pk):

        user = User.objects.get(pk=pk)
        serialized_user = UserWithCitiesSelializer(user)

        return Response(data=serialized_user.data, status=status.HTTP_200_OK)


class UserUpdateDelete(APIView):

    def put(self, request, pk):

        user_to_update = User.objects.get(pk=pk)

        updated_user = UserSerializer(user_to_update, data=request.data)

        if not updated_user.is_valid():
            return Response(data=updated_user.errors, status=status.HTTP_400_BAD_REQUEST)

        updated_user.save()

        return Response(updated_user.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):

        user_to_delete = self.get_user(pk=pk)
        user_to_delete.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # Helper method to get user by id
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist():
            raise NotFound(detail='User does not exists')
