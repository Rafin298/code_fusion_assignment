
from django.urls import path

from .views import (
    # API views
    CountryListAPIView, CountryDetailAPIView, CountryByRegionAPIView,
    CountryByLanguageAPIView, CountrySearchAPIView,
    # Template views
    HomeView, AboutView
)



urlpatterns = [
    path('api/countries/', CountryListAPIView.as_view(), name='country-list'),
    path('api/countries/<int:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),
    path('api/countries/<int:pk>/region/', CountryByRegionAPIView.as_view(), name='country-by-region'),
    path('api/countries/language/<str:language_code>/', CountryByLanguageAPIView.as_view(), name='country-by-language'),
    path('api/countries/search/', CountrySearchAPIView.as_view(), name='country-search'),
    
    # Template URL patterns
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
]