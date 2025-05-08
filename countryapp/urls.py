
from django.urls import path

from .views import (
    CountryListAPIView, CountryDetailAPIView, CountryByRegionAPIView,
    CountryByLanguageAPIView
)

urlpatterns = [
    # Standard RESTful endpoints
    path('', CountryListAPIView.as_view(), name='country-list'),
    path('<int:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),
    path('<int:pk>/region/', CountryByRegionAPIView.as_view(), name='country-by-region'),
    path('language/<str:language_code>/', CountryByLanguageAPIView.as_view(), name='country-by-language'),
]