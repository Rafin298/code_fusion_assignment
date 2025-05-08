from rest_framework import serializers
from .models import (
    Country, InternationalDialingCode
)
class CountryListSerializer(serializers.ModelSerializer):
    """Serializer for list of countries with full details matching the RestCountries API format"""
    name = serializers.SerializerMethodField()
    capital = serializers.SerializerMethodField()
    timezones = serializers.ListField()
    flags = serializers.SerializerMethodField()
    
    class Meta:
        model = Country
        fields = [
            'id', 'name', 'cca2', 'capital', 'population', 'timezones', 'flags'
        ]
    
    def get_name(self, obj):
        result = {
            'common': obj.common_name,
            'official': obj.official_name,
            'nativeName': {}
        }
        
        # Add native names
        native_names = obj.names.all()
        for name in native_names:
            result['nativeName'][name.language_code] = {
                'official': name.official_name,
                'common': name.common_name
            }
        
        return result
    
    def get_capital(self, obj):
        return [capital.name for capital in obj.capitals.all()]
    
    def get_flags(self, obj):
        return {
            'png': obj.flag_png_url,
            'svg': obj.flag_svg_url,
            'alt': obj.flag_alt
        }
    
class CountryDetailSerializer(serializers.ModelSerializer):
    """Serializer for list of countries with full details matching the RestCountries API format"""
    name = serializers.SerializerMethodField()
    tld = serializers.SerializerMethodField()
    currencies = serializers.SerializerMethodField()
    idd = serializers.SerializerMethodField()
    capital = serializers.SerializerMethodField()
    altSpellings = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    latlng = serializers.SerializerMethodField()
    landlocked = serializers.BooleanField()
    borders = serializers.SerializerMethodField()
    area = serializers.FloatField()
    demonyms = serializers.SerializerMethodField()
    translations = serializers.SerializerMethodField()
    maps = serializers.SerializerMethodField()
    population = serializers.IntegerField()
    gini = serializers.JSONField()
    fifa = serializers.CharField()
    car = serializers.SerializerMethodField()
    timezones = serializers.ListField()
    continents = serializers.ListField()
    flags = serializers.SerializerMethodField()
    coatOfArms = serializers.SerializerMethodField()
    startOfWeek = serializers.CharField(source='start_of_week')
    capitalInfo = serializers.SerializerMethodField()
    postalCode = serializers.SerializerMethodField()
    unMember = serializers.BooleanField(source='un_member')
    flag = serializers.SerializerMethodField()
    
    class Meta:
        model = Country
        fields = [
            'id', 'name', 'tld', 'cca2', 'ccn3', 'cioc', 'independent', 'status', 
            'unMember', 'currencies', 'idd', 'capital', 'altSpellings', 
            'region', 'subregion', 'languages', 'latlng', 'landlocked', 
            'borders', 'area', 'demonyms', 'cca3', 'translations', 'flag', 
            'maps', 'population', 'gini', 'fifa', 'car', 'timezones', 
            'continents', 'flags', 'coatOfArms', 'startOfWeek', 'capitalInfo',
            'postalCode'
        ]
    
    def get_name(self, obj):
        result = {
            'common': obj.common_name,
            'official': obj.official_name,
            'nativeName': {}
        }
        
        # Add native names
        native_names = obj.names.all()
        for name in native_names:
            result['nativeName'][name.language_code] = {
                'official': name.official_name,
                'common': name.common_name
            }
        
        return result
    
    def get_tld(self, obj):
        return obj.tlds if obj.tlds else []
    
    def get_currencies(self, obj):
        result = {}
        currency_relationships = obj.currencies.all()
        
        for rel in currency_relationships:
            result[rel.currency.code] = {
                'name': rel.currency.name,
                'symbol': rel.currency.symbol
            }
        
        return result
    
    def get_idd(self, obj):
        try:
            idd = obj.idd
            return {
                'root': idd.root,
                'suffixes': idd.suffixes if idd.suffixes else []
            }
        except InternationalDialingCode.DoesNotExist:
            return {'root': '', 'suffixes': []}
    
    def get_capital(self, obj):
        return [capital.name for capital in obj.capitals.all()]
    
    def get_altSpellings(self, obj):
        return [spelling.spelling for spelling in obj.alt_spellings.all()]
    
    def get_languages(self, obj):
        result = {}
        language_relationships = obj.languages.all()
        
        for rel in language_relationships:
            result[rel.language.code] = rel.language.name
        
        return result
    
    def get_latlng(self, obj):
        return [obj.latitude, obj.longitude] if obj.latitude and obj.longitude else []
    
    def get_borders(self, obj):
        return [border.to_country.cca3 for border in obj.borders_from.all()]
    
    def get_demonyms(self, obj):
        result = {}
        for demonym in obj.demonyms.all():
            result[demonym.language] = {
                'f': demonym.female,
                'm': demonym.male
            }
        return result
    
    def get_translations(self, obj):
        result = {}
        for translation in obj.translations.all():
            result[translation.language_code] = {
                'official': translation.official_name,
                'common': translation.common_name
            }
        return result
    
    def get_maps(self, obj):
        return {
            'googleMaps': obj.google_maps_url,
            'openStreetMaps': obj.openstreetmap_url
        }
    
    def get_car(self, obj):
        return {
            'signs': obj.car_signs if obj.car_signs else [],
            'side': obj.car_side
        }
    
    def get_flags(self, obj):
        return {
            'png': obj.flag_png_url,
            'svg': obj.flag_svg_url,
            'alt': obj.flag_alt
        }
    
    def get_coatOfArms(self, obj):
        return {
            'png': obj.coat_of_arms_png_url,
            'svg': obj.coat_of_arms_svg_url
        }
    
    def get_capitalInfo(self, obj):
        capitals = obj.capitals.all()
        if capitals.exists() and capitals.first().latitude and capitals.first().longitude:
            return {
                'latlng': [capitals.first().latitude, capitals.first().longitude]
            }
        return {'latlng': []}
    
    def get_postalCode(self, obj):
        return {
            'format': obj.postal_code_format,
            'regex': obj.postal_code_regex
        }
        
    def get_flag(self, obj):
        # Return flag emoji for the country
        return "🇺🇳"


class CountryCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating countries"""
    class Meta:
        model = Country
        fields = [
            'common_name', 'official_name', 'cca2', 'cca3', 'ccn3', 'cioc',
            'independent', 'status', 'un_member', 'region', 'subregion',
            'latitude', 'longitude', 'landlocked', 'area', 'population',
            'tlds', 'start_of_week', 'gini', 'fifa', 'car_signs', 'car_side',
            'timezones', 'continents', 'google_maps_url', 'openstreetmap_url',
            'flag_png_url', 'flag_svg_url', 'flag_alt', 'coat_of_arms_png_url',
            'coat_of_arms_svg_url', 'postal_code_format', 'postal_code_regex'
        ]