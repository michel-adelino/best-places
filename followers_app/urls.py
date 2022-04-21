from django.urls import path
from .views import FollowerListCreate, FollowerRetrieve

urlpatterns = [
    path('', FollowerListCreate.as_view()),
    path('<int:pk>/', FollowerRetrieve.as_view()),
]
