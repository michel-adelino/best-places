from django.urls import path
from .views import CityList, CityDetail

urlpatterns = [
    path('cities/', CityList.as_view()),
    path('cities/detail/<int:pk>/', CityDetail.as_view()),
]
