from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import (
    Country, Language
)
from .serializers import (
    CountryListSerializer, CountryCreateUpdateSerializer
)

class CountryListAPIView(APIView):
    """List all countries or create a new one"""
    
    def get(self, request):
        """Get all countries with full details"""
        countries = Country.objects.all()
        serializer = CountryListSerializer(countries, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new country"""
        serializer = CountryCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return the newly created country with full details
            country = Country.objects.get(pk=serializer.instance.pk)
            response_serializer = CountryListSerializer(country)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryDetailAPIView(APIView):
    """Retrieve, update or delete a country"""
    
    def get_object(self, pk):
        return get_object_or_404(Country, pk=pk)
    
    def get(self, request, pk):
        """Get details of a specific country"""
        country = self.get_object(pk)
        serializer = CountryListSerializer(country)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Update an existing country"""
        country = self.get_object(pk)
        serializer = CountryCreateUpdateSerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return the updated country with full details
            updated_country = self.get_object(pk)
            response_serializer = CountryListSerializer(updated_country)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Delete an existing country"""
        country = self.get_object(pk)
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CountryByRegionAPIView(APIView):
    """List countries in the same region as a specified country"""
    
    def get(self, request, pk):
        """Get countries in the same region"""
        country = get_object_or_404(Country, pk=pk)
        
        if not country.region:
            return Response(
                {"error": "The specified country does not have a region assigned."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        regional_countries = Country.objects.filter(region=country.region).exclude(pk=pk)
        serializer = CountryListSerializer(regional_countries, many=True)
        return Response(serializer.data)


class CountryByLanguageAPIView(APIView):
    """List countries that speak a specific language"""
    
    def get(self, request, language_code):
        """Get countries speaking the specified language"""
        # Check if language exists
        language = get_object_or_404(Language, code=language_code)
        
        # Get countries that speak this language
        countries = Country.objects.filter(languages__language=language)
        serializer = CountryListSerializer(countries, many=True)
        return Response(serializer.data)


