from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import status
from .serializer import ReviewSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class ReviewCreate(APIView):

    permission_classes = [IsAuthenticated, ]

    def post(self, request):

        request.data['user'] = request.user.id
        review_serializer = ReviewSerializer(data=request.data)

        if not review_serializer.is_valid():
            return Response(data=review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        review_serializer.save()

        return Response(data=review_serializer.data, status=status.HTTP_201_CREATED)
