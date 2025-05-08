
from django.urls import path

from django.contrib.auth import views as auth_views

from .views import (
    # API views
    CountryListAPIView, CountryDetailAPIView, CountryByRegionAPIView,
    CountryByLanguageAPIView, CountrySearchAPIView,
    # Template views
    HomeView, AboutView,
    # Authentication views
    RegisterView
)



urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='countryapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    
    path('api/countries/', CountryListAPIView.as_view(), name='country-list'),
    path('api/countries/<int:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),
    path('api/countries/<int:pk>/region/', CountryByRegionAPIView.as_view(), name='country-by-region'),
    path('api/countries/language/<str:language_code>/', CountryByLanguageAPIView.as_view(), name='country-by-language'),
    path('api/countries/search/', CountrySearchAPIView.as_view(), name='country-search'),
    
    # Template URL patterns
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
]