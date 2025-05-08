from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField

class Country(models.Model):
    """Main model to represent a country"""
    
    # Basic information
    common_name = models.CharField(max_length=100)
    official_name = models.CharField(max_length=200)
    cca2 = models.CharField(max_length=2, unique=True)
    cca3 = models.CharField(max_length=3, unique=True)
    ccn3 = models.CharField(max_length=3, null=True, blank=True)
    cioc = models.CharField(max_length=3, null=True, blank=True)
    
    # Status and membership
    independent = models.BooleanField(default=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    un_member = models.BooleanField(default=False)
    
    # Geographical information
    region = models.CharField(max_length=100, null=True, blank=True)
    subregion = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    landlocked = models.BooleanField(default=False)
    area = models.FloatField(null=True, blank=True)
    population = models.IntegerField(null=True, blank=True)
    
    # Additional fields
    tlds = ArrayField(models.CharField(max_length=10), blank=True, null=True)
    start_of_week = models.CharField(max_length=10, default="monday")
    gini = JSONField(null=True, blank=True)
    fifa = models.CharField(max_length=3, null=True, blank=True)
    car_signs = ArrayField(models.CharField(max_length=3), blank=True, null=True)
    car_side = models.CharField(max_length=5, null=True, blank=True)
    timezones = ArrayField(models.CharField(max_length=15), blank=True, null=True)
    continents = ArrayField(models.CharField(max_length=20), blank=True, null=True)
    
    # URLs for maps and flags
    google_maps_url = models.URLField(max_length=255, null=True, blank=True)
    openstreetmap_url = models.URLField(max_length=255, null=True, blank=True)
    flag_png_url = models.URLField(max_length=255, null=True, blank=True)
    flag_svg_url = models.URLField(max_length=255, null=True, blank=True)
    flag_alt = models.TextField(null=True, blank=True)
    coat_of_arms_png_url = models.URLField(max_length=255, null=True, blank=True)
    coat_of_arms_svg_url = models.URLField(max_length=255, null=True, blank=True)
    
    # Postal code information
    postal_code_format = models.CharField(max_length=50, null=True, blank=True)
    postal_code_regex = models.CharField(max_length=100, null=True, blank=True)
    
    # Meta and timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Countries"
    
    def __str__(self):
        return self.common_name


class CapitalCity(models.Model):
    """Model for capital cities of countries"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='capitals')
    name = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Capital Cities"
    
    def __str__(self):
        return f"{self.name} (Capital of {self.country.common_name})"


class CountryName(models.Model):
    """Model for native and alternative names of countries"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='names')
    language_code = models.CharField(max_length=3)
    official_name = models.CharField(max_length=200)
    common_name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('country', 'language_code')
    
    def __str__(self):
        return f"{self.common_name} ({self.language_code})"


class AlternativeSpelling(models.Model):
    """Model for alternative spellings of country names"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='alt_spellings')
    spelling = models.CharField(max_length=200)
    
    def __str__(self):
        return self.spelling


class BorderCountry(models.Model):
    """Model for representing borders between countries"""
    from_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='borders_from')
    to_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='borders_to')
    
    class Meta:
        unique_together = ('from_country', 'to_country')
        verbose_name_plural = "Border Countries"
    
    def __str__(self):
        return f"{self.from_country.common_name} -> {self.to_country.common_name}"


class Currency(models.Model):
    """Model for currencies used by countries"""
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    
    class Meta:
        verbose_name_plural = "Currencies"
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class CountryCurrency(models.Model):
    """Many-to-many relationship between countries and currencies"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='currencies')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='countries')
    
    class Meta:
        unique_together = ('country', 'currency')
    
    def __str__(self):
        return f"{self.country.common_name} - {self.currency.code}"


class Language(models.Model):
    """Model for languages spoken in countries"""
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class CountryLanguage(models.Model):
    """Many-to-many relationship between countries and languages"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='languages')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='countries')
    
    class Meta:
        unique_together = ('country', 'language')
    
    def __str__(self):
        return f"{self.country.common_name} - {self.language.name}"


class Demonym(models.Model):
    """Model for demonyms (names for residents of a country)"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='demonyms')
    language = models.CharField(max_length=3) 
    male = models.CharField(max_length=100)
    female = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('country', 'language')
    
    def __str__(self):
        return f"{self.male}/{self.female} ({self.language})"


class CountryTranslation(models.Model):
    """Model for translations of country names in different languages"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='translations')
    language_code = models.CharField(max_length=3) 
    official_name = models.CharField(max_length=200)
    common_name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('country', 'language_code')
    
    def __str__(self):
        return f"{self.common_name} ({self.language_code})"


class InternationalDialingCode(models.Model):
    """Model for international dialing codes"""
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='idd')
    root = models.CharField(max_length=10)
    suffixes = ArrayField(models.CharField(max_length=10), blank=True, null=True)
    
    def __str__(self):
        return f"{self.root} ({self.country.common_name})"