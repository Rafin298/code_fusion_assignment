
from django.urls import path

from .views import (
    CountryListAPIView, CountryDetailAPIView, CountryByRegionAPIView,
)

urlpatterns = [
    # Standard RESTful endpoints
    path('', CountryListAPIView.as_view(), name='country-list'),
    path('<int:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),
    path('<int:pk>/region/', CountryByRegionAPIView.as_view(), name='country-by-region'),
]