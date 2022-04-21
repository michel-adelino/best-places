from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from rest_framework import status

# from jwt_auth_app.serializers import UserSerializer
from .serializers import FollowerSerializer
from .models import Follower

User = get_user_model()


class FollowerListCreate(APIView):

    # permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """ GET `/followers/` endpoint """

        followers = Follower.objects.all()

        serialized_followers = FollowerSerializer(followers, many=True)
        return Response(data=serialized_followers.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ POST `/followers/` endpoint
        """

        follower_serializer = FollowerSerializer(data=request.data)

        if not follower_serializer.is_valid():
            return Response(data=follower_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        follower_serializer.save()

        return Response(data=follower_serializer.data, status=status.HTTP_201_CREATED)


# class Unfollow(APIView):

#     permission_classes = [IsAuthenticated, ]

#     def post(self, request):
#         pass

class FollowerRetrieve(APIView):

    # permission_classes = [IsAuthenticated, ]

    def fetch_connection(self, pk):
        """ Helper function to fetch the following connection by id 
            through a try-catch block (User 1 following user 3 is one connection. User 3 following user 8 is another connection).
        """
        try:
            return Follower.objects.get(pk=pk)
        except Follower.DoesNotExist:
            raise NotFound(detail="Following connection id not found")

    def get(self, request, pk):
        """ GET `/followers/<int:pk>/` endpoint.
            `user` arg is the 'followee'
        """

        user = self.fetch_connection(pk=pk)
        serialized_user = FollowerSerializer(user)

        return Response(data=serialized_user.data, status=status.HTTP_200_OK)
