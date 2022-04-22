from django.urls import path
from .views import HolidayListCreate, HolidayRetrieveUpdateDelete

urlpatterns = [
    path('', HolidayListCreate.as_view()),
    path('<int:pk>/', HolidayRetrieveUpdateDelete.as_view()),
]
