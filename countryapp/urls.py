
from django.urls import path

from .views import (
    CountryListAPIView, CountryDetailAPIView
)

urlpatterns = [
    # Standard RESTful endpoints
    path('', CountryListAPIView.as_view(), name='country-list'),
    path('<int:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),
]