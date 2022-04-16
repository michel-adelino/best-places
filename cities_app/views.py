from itertools import chain
from django.shortcuts import render
from django.db import connection
from unidecode import unidecode
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

            Handles the POST `scrape/search/` request.
        """

        search_fields = request.data

        if not all(x in search_fields.keys() for x in ('city', 'country')):
            return Response(data="Request body needs to have 'city' and 'country' fields.",
                            status=status.HTTP_400_BAD_REQUEST)

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

        # NO ELSE NEEDED IF YOU RETURN IN THE IF CLAUSE ABOVE...
        else:
            city_serializer.save()
            return Response(data=city_serializer.data, status=status.HTTP_200_OK)


class CityRetrieveUpdateDelete(APIView):
    """ View that handles GET, PUT and DEL `cities/<int:pk>/` request.
            ONLY ADMINs can run the PUT and DEL requests!
    """

    def fetch_city(self, pk):
        """ Helper function to fetch city by id through a try-catch 
            block. 
        """
        try:
            return City.objects.get(pk=pk)
        except City.DoesNotExist:
            raise NotFound(detail="City id not found")

    def get(self, request, pk):
        """ Get city by id (pk). """
        city = self.fetch_city(pk=pk)
        serialized_city = CitySerializer(city)
        return Response(data=serialized_city.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """ Update city by id. 
            ADMIN ONLY. 
        """
        city_to_update = self.fetch_city(pk=pk)
        updated_city = CitySerializer(city_to_update, data=request.data)
        if not updated_city.is_valid():
            return Response(data=updated_city.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            updated_city.save()
            return Response(updated_city.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        """ Delete city by id. 
            ADMIN ONLY. 
        """
        city_to_delete = self.fetch_city(pk=pk)
        city_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchCity(APIView):
    """ Searches through all cities by endpoint parameter:
        - city
        - country
        - state
        - continent
        - top 3 attractions
    """

    def get(self, request, search_term):
        """ GET 'cities/<str:search_term>/' request. """

        # search_term = unidecode(search_term)
        # cities = City.objects.get(city__icontains=search_term)  # `get` returns JUST ONE (error if more). so use `filter`` instead
        cities = City.objects.filter(city__unaccent__icontains=search_term)
        countries = City.objects.filter(
            country__unaccent__icontains=search_term)
        state = City.objects.filter(state__unaccent__icontains=search_term)
        continent = City.objects.filter(
            continent__unaccent__icontains=search_term)
        description = City.objects.filter(
            description__unaccent__icontains=search_term)
        top_3_attractions = City.objects.filter(
            top_3_attractions__icontains=search_term)

        results = set(list(chain(
            cities, countries, state, continent, description, top_3_attractions
        )))

        serialized_results = CitySerializer(results, many=True)
        return Response(data=serialized_results.data, status=status.HTTP_202_ACCEPTED)
