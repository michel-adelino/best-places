from django.urls import path
from .views import CityListCreate, CityDetail, ScrapeSearch

urlpatterns = [
    path('cities/', CityListCreate.as_view()),
    path('cities/detail/<int:pk>/', CityDetail.as_view()),
    path('scrape/search/', ScrapeSearch.as_view()),
]
