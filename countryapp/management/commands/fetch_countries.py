from django.core.management.base import BaseCommand
import requests
from django.db import transaction


from countryapp.models import (
    Country, CapitalCity, CountryName, AlternativeSpelling, 
    BorderCountry, Currency, CountryCurrency, Language, 
    CountryLanguage, Demonym, CountryTranslation, InternationalDialingCode
)

class Command(BaseCommand):
    help = 'Fetch country data from restcountries.com API and populate the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-url',
            default='https://restcountries.com/v3.1/all',
            help='API URL to fetch country data from'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing country data before importing'
        )

    def fetch_countries_data(self, url):
        """Fetch country data from REST Countries API"""
        self.stdout.write(self.style.NOTICE(f"Fetching country data from {url}"))
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses
            countries_data = response.json()
            self.stdout.write(self.style.SUCCESS(f"Successfully fetched data for {len(countries_data)} countries"))
            return countries_data
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data: {e}"))
            return None

    @transaction.atomic
    def import_countries_data(self, countries_data):
        """Import country data to the database"""
        self.stdout.write(self.style.NOTICE("Starting country data import..."))
        
        # Track countries by code for border relationships
        country_objects = {}
        
        # Create or update languages and currencies first
        languages = {}
        currencies = {}
        
        # Process languages and currencies
        self.stdout.write(self.style.NOTICE("Processing languages and currencies..."))
        for country_data in countries_data:
            # Process languages
            for lang_code, lang_name in country_data.get('languages', {}).items():
                if lang_code not in languages:
                    language, created = Language.objects.update_or_create(
                        code=lang_code,
                        defaults={'name': lang_name}
                    )
                    languages[lang_code] = language
                    if created:
                        self.stdout.write(f"Created language: {lang_code} - {lang_name}")

            # Process currencies
            for currency_code, currency_info in country_data.get('currencies', {}).items():
                if currency_code not in currencies:
                    currency, created = Currency.objects.update_or_create(
                        code=currency_code,
                        defaults={
                            'name': currency_info.get('name', ''),
                            'symbol': currency_info.get('symbol', '')
                        }
                    )
                    currencies[currency_code] = currency
                    if created:
                        self.stdout.write(f"Created currency: {currency_code}")
        
        # Process countries
        self.stdout.write(self.style.NOTICE("Processing countries..."))
        counter = 0
        total = len(countries_data)
        
        # Now process each country
        for country_data in countries_data:
            try:
                # Ensure we have a cca3 code which is our primary identifier
                cca3 = country_data.get('cca3')
                if not cca3:
                    self.stdout.write(self.style.WARNING(
                        f"Skipping country without cca3 code: {country_data.get('name', {}).get('common', 'Unknown')}"
                    ))
                    continue
                    
                counter += 1
                if counter % 10 == 0 or counter == total:
                    self.stdout.write(f"Processing country {counter}/{total}: {country_data.get('name', {}).get('common', cca3)}")
                
                # Create or update the main country record
                country, created = Country.objects.update_or_create(
                    cca3=cca3,
                    defaults={
                        'common_name': country_data.get('name', {}).get('common', ''),
                        'official_name': country_data.get('name', {}).get('official', ''),
                        'cca2': country_data.get('cca2', ''),
                        'ccn3': country_data.get('ccn3', ''),
                        'cioc': country_data.get('cioc', ''),
                        'independent': country_data.get('independent', True),
                        'status': country_data.get('status', ''),
                        'un_member': country_data.get('unMember', False),
                        'region': country_data.get('region', ''),
                        'subregion': country_data.get('subregion', ''),
                        'latitude': country_data.get('latlng', [None, None])[0] if len(country_data.get('latlng', [])) > 0 else None,
                        'longitude': country_data.get('latlng', [None, None])[1] if len(country_data.get('latlng', [])) > 1 else None,
                        'landlocked': country_data.get('landlocked', False),
                        'area': country_data.get('area', None),
                        'population': country_data.get('population', None),
                        'tlds': country_data.get('tld', []),
                        'start_of_week': country_data.get('startOfWeek', 'monday'),
                        'gini': country_data.get('gini', {}),
                        'fifa': country_data.get('fifa', ''),
                        'car_signs': country_data.get('car', {}).get('signs', []),
                        'car_side': country_data.get('car', {}).get('side', ''),
                        'timezones': country_data.get('timezones', []),
                        'continents': country_data.get('continents', []),
                        'google_maps_url': country_data.get('maps', {}).get('googleMaps', ''),
                        'openstreetmap_url': country_data.get('maps', {}).get('openStreetMaps', ''),
                        'flag_png_url': country_data.get('flags', {}).get('png', ''),
                        'flag_svg_url': country_data.get('flags', {}).get('svg', ''),
                        'flag_alt': country_data.get('flags', {}).get('alt', ''),
                        'coat_of_arms_png_url': country_data.get('coatOfArms', {}).get('png', ''),
                        'coat_of_arms_svg_url': country_data.get('coatOfArms', {}).get('svg', ''),
                        'postal_code_format': country_data.get('postalCode', {}).get('format', ''),
                        'postal_code_regex': country_data.get('postalCode', {}).get('regex', ''),
                    }
                )
                
                # Store for border relationships
                country_objects[country.cca3] = country
                
                # Add capital cities
                CapitalCity.objects.filter(country=country).delete()
                capitals = country_data.get('capital', [])
                capital_info = country_data.get('capitalInfo', {}).get('latlng', [None, None])
                
                for i, capital_name in enumerate(capitals):
                    lat = capital_info[0] if i == 0 and len(capital_info) > 0 else None
                    lng = capital_info[1] if i == 0 and len(capital_info) > 1 else None
                    
                    CapitalCity.objects.create(
                        country=country,
                        name=capital_name,
                        latitude=lat,
                        longitude=lng
                    )
                
                # Add native names
                CountryName.objects.filter(country=country).delete()
                for lang_code, name_data in country_data.get('name', {}).get('nativeName', {}).items():
                    CountryName.objects.create(
                        country=country,
                        language_code=lang_code,
                        official_name=name_data.get('official', ''),
                        common_name=name_data.get('common', '')
                    )
                
                # Add alternative spellings
                AlternativeSpelling.objects.filter(country=country).delete()
                for spelling in country_data.get('altSpellings', []):
                    AlternativeSpelling.objects.create(
                        country=country,
                        spelling=spelling
                    )
                
                # Add languages
                CountryLanguage.objects.filter(country=country).delete()
                for lang_code in country_data.get('languages', {}):
                    if lang_code in languages:
                        CountryLanguage.objects.create(
                            country=country,
                            language=languages[lang_code]
                        )
                
                # Add currencies
                CountryCurrency.objects.filter(country=country).delete()
                for currency_code in country_data.get('currencies', {}):
                    if currency_code in currencies:
                        CountryCurrency.objects.create(
                            country=country,
                            currency=currencies[currency_code]
                        )
                
                # Add demonyms
                Demonym.objects.filter(country=country).delete()
                for lang_code, demonym_data in country_data.get('demonyms', {}).items():
                    Demonym.objects.create(
                        country=country,
                        language=lang_code,
                        male=demonym_data.get('m', ''),
                        female=demonym_data.get('f', '')
                    )
                
                # Add translations
                CountryTranslation.objects.filter(country=country).delete()
                for lang_code, translation_data in country_data.get('translations', {}).items():
                    CountryTranslation.objects.create(
                        country=country,
                        language_code=lang_code,
                        official_name=translation_data.get('official', ''),
                        common_name=translation_data.get('common', '')
                    )
                
                # Add IDD (International Dialing)
                InternationalDialingCode.objects.filter(country=country).delete()
                idd_data = country_data.get('idd', {})
                if idd_data:
                    InternationalDialingCode.objects.create(
                        country=country,
                        root=idd_data.get('root', ''),
                        suffixes=idd_data.get('suffixes', [])
                    )
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error processing country {country_data.get('name', {}).get('common', 'Unknown')}: {e}"
                ))
        
        # Now handle border relationships after all countries are created
        self.stdout.write(self.style.NOTICE("Setting up border relationships..."))
        for country_data in countries_data:
            from_country = country_objects.get(country_data.get('cca3'))
            if not from_country:
                continue
                
            # Remove existing borders first
            BorderCountry.objects.filter(from_country=from_country).delete()
            
            # Add new borders
            for border_code in country_data.get('borders', []):
                to_country = country_objects.get(border_code)
                if to_country:
                    BorderCountry.objects.create(
                        from_country=from_country,
                        to_country=to_country
                    )
        
        self.stdout.write(self.style.SUCCESS(f"Successfully imported data for {len(country_objects)} countries"))

    def handle(self, *args, **options):
        """Execute the command"""
        self.stdout.write(self.style.NOTICE("Starting country data fetch and import process"))
        
        # Reset existing data if requested
        if options['reset']:
            self.stdout.write(self.style.WARNING("Deleting all existing country data..."))
            # Delete in order to avoid foreign key conflicts
            InternationalDialingCode.objects.all().delete()
            CountryTranslation.objects.all().delete()
            Demonym.objects.all().delete()
            CountryCurrency.objects.all().delete()
            CountryLanguage.objects.all().delete()
            AlternativeSpelling.objects.all().delete()
            CountryName.objects.all().delete()
            CapitalCity.objects.all().delete()
            BorderCountry.objects.all().delete()
            Country.objects.all().delete()
            Currency.objects.all().delete()
            Language.objects.all().delete()
            
        # Fetch data from API
        countries_data = self.fetch_countries_data(options['api_url'])
        if not countries_data:
            self.stdout.write(self.style.ERROR("Failed to fetch country data. Exiting."))
            return
        
        # Import data to database
        try:
            self.import_countries_data(countries_data)
            self.stdout.write(self.style.SUCCESS("Country data import completed successfully"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during import process: {e}"))