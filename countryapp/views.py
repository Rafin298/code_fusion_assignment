from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import (
    Country
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
    
    