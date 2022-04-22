from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from holidays_app.serializers import HolidaySerializer
from .models import Holiday


class HolidayListCreate(APIView):

    # permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request):
        """ Lists all holidays """
        holidays = Holiday.objects.all()
        serialized_holidays = HolidaySerializer(holidays, many=True)
        return Response(data=serialized_holidays.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Create a holiday. Logged in user must be the 
            owner of the profile to create a holiday entry
        """
        holiday = request.data
        holiday_serializer = HolidaySerializer(data=holiday)

        if not holiday_serializer.is_valid():
            return Response(data=holiday_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        holiday_serializer.save()
        return Response(data=holiday_serializer.data, status=status.HTTP_200_OK)


class HolidayRetrieveUpdateDelete(APIView):

    # permission_classes = [IsAuthenticatedOrReadOnly, ]

    def fetch_holiday(self, pk):
        """ Helper function to fetch holiday by id through a try-catch 
            block. 
        """
        try:
            return Holiday.objects.get(pk=pk)
        except Holiday.DoesNotExist:
            raise NotFound(detail="Holiday id not found")

    def get(self, request, pk):
        """ Get holiday by id (pk). """
        holiday = self.fetch_holiday(pk=pk)
        serialized_holiday = HolidaySerializer(holiday)
        return Response(data=serialized_holiday.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """ Edit a holiday. Logged in user MUST BE the 
            owner of the profile to update a holiday entry
        """
        holiday_to_update = self.fetch_holiday(pk=pk)
        updated_holiday = HolidaySerializer(
            holiday_to_update, data=request.data)
        if not updated_holiday.is_valid():
            return Response(data=updated_holiday.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            updated_holiday.save()
            return Response(updated_holiday.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        """ Delete a holiday. Logged in user MUST BE the 
            owner of the profile to delete a holiday entry
        """
        holiday_to_delete = self.fetch_holiday(pk=pk)
        holiday_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
