from django.urls import path
from .views import CityListCreate, CityRetrieveUpdateDelete, ScrapeSearch, SearchCity, ScrapeCityUrls

urlpatterns = [
    path('cities/', CityListCreate.as_view()),
    path('cities/<int:pk>/', CityRetrieveUpdateDelete.as_view()),
    path('scrape/search/', ScrapeSearch.as_view()),
    path('scrape/cities/', ScrapeCityUrls.as_view()),
    path('cities/<str:search_term>/', SearchCity.as_view()),
]
