from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import (
    Country, Language
)
from .serializers import (
    CountryDetailSerializer, CountryListRegionSerializer, CountryListSerializer, CountryCreateUpdateSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for API results"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CountryListAPIView(APIView):
    """List all countries or create a new one"""
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        """Get all countries with pagination"""
        countries = Country.objects.all().order_by('common_name')
        
        # Implement pagination
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(countries, request)
        serializer = CountryListSerializer(result_page, many=True)
        
        # Create response with pagination metadata
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        """Create a new country"""
        serializer = CountryCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return the newly created country with full details
            country = Country.objects.get(pk=serializer.instance.pk)
            response_serializer = CountryCreateUpdateSerializer(country)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryDetailAPIView(APIView):
    """Retrieve, update or delete a country"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(Country, pk=pk)
    
    def get(self, request, pk):
        """Get details of a specific country"""
        country = self.get_object(pk)
        serializer = CountryDetailSerializer(country)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Update an existing country"""
        country = self.get_object(pk)
        serializer = CountryCreateUpdateSerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return the updated country with full details
            updated_country = self.get_object(pk)
            response_serializer = CountryCreateUpdateSerializer(updated_country)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Delete an existing country"""
        country = self.get_object(pk)
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CountryByRegionAPIView(APIView):
    """List countries in the same region as a specified country"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Get countries in the same region"""
        country = get_object_or_404(Country, pk=pk)
        
        if not country.region:
            return Response(
                {"error": "The specified country does not have a region assigned."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        regional_countries = Country.objects.filter(region=country.region).exclude(pk=pk)
        serializer = CountryListRegionSerializer(regional_countries, many=True)
        return Response(serializer.data)


class CountryByLanguageAPIView(APIView):
    """List countries that speak a specific language"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, language_code):
        """Get countries speaking the specified language"""
        # Check if language exists
        language = get_object_or_404(Language, code=language_code)
        
        # Get countries that speak this language
        countries = Country.objects.filter(languages__language=language)
        serializer = CountryListSerializer(countries, many=True)
        return Response(serializer.data)


class CountrySearchAPIView(APIView):
    """Search countries by name (supports partial search)"""
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, name=None):
        """Search countries by name"""
        search_term = name or request.query_params.get('q', '')
        
        if not search_term:
            return Response(
                {"error": "Please provide a search term with 'q' parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Search in common name, official name, alternative spellings and translations
        countries = Country.objects.filter(
            Q(common_name__icontains=search_term) |
            Q(official_name__icontains=search_term) |
            Q(alt_spellings__spelling__icontains=search_term) |
            Q(translations__common_name__icontains=search_term) |
            Q(translations__official_name__icontains=search_term)
        ).distinct().order_by('common_name')
        
        # Implement pagination
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(countries, request)
        serializer = CountryListSerializer(result_page, many=True)
        
        # Create response with pagination metadata
        return paginator.get_paginated_response(serializer.data)

class RegisterView(CreateView):
    """View for user registration"""
    template_name = 'countryapp/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, "Registration successful. You can now login.")
        return super().form_valid(form)


class HomeView(LoginRequiredMixin, TemplateView):
    """Home page view showing the list of countries"""
    template_name = 'countryapp/country_list.html'
    login_url = 'login'  # Redirect to login page if user is not authenticated

class AboutView(LoginRequiredMixin, TemplateView):
    """About page view"""
    template_name = 'countryapp/about.html'
    login_url = 'login'