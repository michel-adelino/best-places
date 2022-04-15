from django.urls import path
from .views import CityListCreate, CityRetrieveUpdateDelete, ScrapeSearch

urlpatterns = [
    path('cities/', CityListCreate.as_view()),
    path('cities/<int:pk>/', CityRetrieveUpdateDelete.as_view()),
    path('scrape/search/', ScrapeSearch.as_view()),
]
