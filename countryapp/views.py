from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Country
)
from .serializers import (
    CountryListSerializer
)

class CountryListAPIView(APIView):
    """List all countries or create a new one"""
    
    def get(self, request):
        """Get all countries with full details"""
        countries = Country.objects.all()
        serializer = CountryListSerializer(countries, many=True)
        return Response(serializer.data)
    
    