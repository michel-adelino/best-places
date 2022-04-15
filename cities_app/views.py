from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import City
from .serializers import CitySerializer
from scrape_searches import search_lonely_planet
from scrape_cities import scrape_cities
import sys
sys.path.append("..")


class ScrapeSearch(APIView):
    def post(self, request):
        """ 
            The POST request parameters will be used to 
            search Lonely Planet and return the results matching the search country and city. 

            Handles the POST `cities/scrape/` request.
        """

        search_fields = request.data

        if not all(x in search_fields.keys() for x in ('city', 'country')):
            return Response(data="Request body needs to have 'city' and 'country' fields.", status=status.HTTP_400_BAD_REQUEST)

        city_urls = search_lonely_planet(
            city_name=search_fields['city'], country_name=search_fields['country']
        )

        if not city_urls:
            return Response(data="No results", status=status.HTTP_400_BAD_REQUEST)

        return Response(data=city_urls, status=status.HTTP_200_OK)


class CityListCreate(APIView):
    """ View that handles GET and POST `cities/` requests. """

    def get(self, request):
        """ Get all cities. """
        cities = City.objects.all()
        serialized_cities = CitySerializer(cities, many=True)
        return Response(data=serialized_cities.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Create a city that doesn't yet exist in our database.
            This is the city that the user selected, which is the
            request parameter = the VALID url string (that was returned from ScrapeSearch).

            This method will:
            1) first scrape the valid city url provided
            2) then add the scraped results to the DB
        """

        if not (request.data or 'url' in request.data):
            return Response(data="", status=status.HTTP_400_BAD_REQUEST)

        city_url = request.data['url']
        city_object = scrape_cities(urls=[city_url])[0]

        city_serializer = CitySerializer(data=city_object)

        if not city_serializer.is_valid():
            return Response(data=city_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            city_serializer.save()
            return Response(data=city_serializer.data, status=status.HTTP_200_OK)


class CityDetail(APIView):
    """ Get city by id (pk). """

    def get(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
            serialized_city = CitySerializer(city)
            return Response(data=serialized_city.data, status=status.HTTP_200_OK)
        except City.DoesNotExist:
            raise NotFound(detail="City id not found")
