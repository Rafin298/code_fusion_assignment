
from django.urls import path

from .views import (
    CountryListAPIView
)

urlpatterns = [
    # Main endpoints that match the original API structure
    path('', CountryListAPIView.as_view(), name='country-list-all'),
]