from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

import pgeocode
import pycountry


def domicile_validator(client):
    """
    Validates if the country of domicile in client profile corresponds to the country of domicile in account form
    """
    return client['account_form']['country_of_domicile'] == client['client_profile']['country_of_domicile']

def address_validator(client):
    """
    Validates if the address in client profile corresponds to the address in account form
    """
    return client['account_form']['address'] == client['client_profile']['address']

_nomi_cache = {}

def get_country_code(country_name):
    """
    Convert a full country name (e.g., 'Spain') to ISO Alpha-2 code (e.g., 'ES').

    Returns:
        str or None: ISO Alpha-2 code or None if not found.
    """
    try:
        return pycountry.countries.lookup(country_name).alpha_2
    except LookupError:
        return None

def get_nomi_instance(country_code):
    """
    Return a cached pgeocode.Nominatim instance for the given country.
    """
    if country_code not in _nomi_cache:
        _nomi_cache[country_code] = pgeocode.Nominatim(country_code)
    return _nomi_cache[country_code]

def validate_postal_code_for_client(client, check_city=False):
    """
    Validates if the postal code exists in the provided city and country.

    Parameters:
        client_profile (dict): Must include 'address' and 'country_of_domicile'.
        check_city (bool): if true we use this function to find whther city really belongs to the country

    Returns:
        bool: True if postal code matches the city in any listed country, else False.
    """
    client_profile = client['client_profile']
    country_names = [name.strip() for name in client_profile.get('country_of_domicile', '').split(',')]
    address = client_profile.get('address', {})
    city = address.get('city', '').lower()
    postal_code = address.get('postal code', '')

    if check_city:
        for country_name in country_names:
            country_code = get_country_code(country_name)
            if not country_code:
                continue  # Skip invalid countries

            nomi = get_nomi_instance(country_code)
            df = nomi._data

            if df is None or df.empty:
                continue
            
            # Convert to NumPy array and use list comprehension (still fast)
            col_values = df[['place_name', 'postal_code']].values
            mask1 = [val_pair[0].lower() in city or city in val_pair[0].lower() in city for val_pair in col_values]
            df = df[mask1]

            if not df.empty:
                return True
            
        return False

    for country_name in country_names:
        country_code = get_country_code(country_name)
        if not country_code:
            continue  # Skip invalid countries

        nomi = get_nomi_instance(country_code)
        df = nomi._data

        if df is None or df.empty:
            continue
        
        # Convert to NumPy array and use list comprehension (still fast)
        col_values = df[['place_name', 'postal_code']].values
        # mask1 = [val_pair[1] == postal_code and val_pair[0] in city for val_pair in col_values]
        mask1 = [val_pair[1] == postal_code for val_pair in col_values]
        df = df[mask1]

        if not df.empty:
            return True
        
        # postal_info = nomi.query_postal_code(postal_code)['postal_code']

        # if postal_info is None:
        #     continue

        # # matched_cities = [c.strip().lower() for c in postal_info.place_name.split(',')]
        # if postal_info == postal_code:
        #     return True  # Valid match

    return False  # No match found

