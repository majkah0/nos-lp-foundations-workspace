from enum import Enum, unique, auto
import argparse
from pathlib import Path

BASE_DIR = Path().cwd() / 'life_expectancy' / 'data'

EUROSTAT_COUNTRY_DICT = {'BE' : 'Belgium', 'EL' : 'Greece', 'LT' :'Lithuania', 'PT' : 'Portugal',
'BG' : 'Bulgaria', 'ES' : 'Spain', 'LU' : 'Luxembourg', 'RO' : 'Romania',
'CZ' : 'Czechia', 'FR' : 'France', 'HU' : 'Hungary', 'SI' : 'Slovenia',
'DK' : 'Denmark', 'HR' : 'Croatia', 'MT' : 'Malta', 'SK' : 'Slovakia',
'DE' : 'Germany', 'IT' : 'Italy', 'NL' : 'Netherlands', 'FI' : 'Finland',
'EE' : 'Estonia', 'CY' : 'Cyprus', 'AT' : 'Austria', 'SE' : 'Sweden',
'IE' : 'Ireland', 'LV' : 'Latvia', 'PL' : 'Poland',
'IS' : 'Iceland', 'NO' : 'Norway', 'LI' : 'Liechtenstein', 'CH' : 'Switzerland',
'UK' : 'United Kingdom', 'BA' : 'Bosnia and Herzegovina', 'ME' : 'Montenegro',
'MD' : 'Moldova', 'MK' : 'North Macedonia', 'AL' : 'Albania', 'RS' : 'Serbia',
'TR' : 'Türkiye', 'UA' : 'Ukraine', 'XK' : 'Kosovo', 'GE' : 'Georgia',
'RU' : 'Russia', 'DZ' : 'Algeria', 'LB' : 'Lebanon', 'SY' : 'Syria',
'EG' : 'Egypt', 'LY' : 'Libya', 'TN' : 'Tunisia',
'IL' : 'Israel', 'MA' : 'Morocco', 'JO' : 'Jordan', 'PS' : 'Palestine',
'AR' : 'Argentina', 'CN_X_HK' : 'China (except Hong Kong)', 'MX' : 'Mexico', 'ZA' : 'South Africa',
'AU' : 'Australia', 'HK' : 'Hong Kong', 'NG' : 'Nigeria', 'KR' : 'South Korea',
'BR' : 'Brazil', 'IN' : 'India', 'NZ' : 'New Zealand', 'TW' : 'Taiwan',
'CA' : 'Canada','JP' : 'Japan', 'SG' : 'Singapore', 'US' : 'United States',
'DE_TOT' : 'Germany after 3 October 1990'}

EUROSTAT_OTHER_DICT = {'EA18' : 'Euro area 18', 'EA19' : 'Euro area 19',
'EEA30_2007' : 'European economic area 30', 'EEA31' :'European economic area 31' ,
'EFTA' : 'European free trade association' , 'EU27_2007' : 'European union 27 countries',
'EU27_2020' : 'European union 27 countries without UK', 'EU28' : 'European union 28 countries' ,}
    
def _country_names():
       return EUROSTAT_COUNTRY_DICT.values()

def _country_codes():
        return EUROSTAT_COUNTRY_DICT.keys()

""" Enum for country names to control input arguments """
Country = Enum('Country', EUROSTAT_COUNTRY_DICT | EUROSTAT_OTHER_DICT)
Country.country_names = _country_names
Country.country_codes = _country_codes

class InputFileType(Enum):
        """ Enum for file types to control input arguments """
        tsv = 'tsv'
        json = 'json'

class EnumAction(argparse.Action):
    """ Argparse action for handling Enums """
    def __init__(self, **kwargs):
        enum_type = kwargs.pop("type", None)
        if enum_type is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(enum_type, Enum):
            raise TypeError("type must be an Enum when using EnumAction")

        # Generate choices from the Enum
        kwargs.setdefault("choices", tuple(e.value for e in enum_type))

        super(EnumAction, self).__init__(**kwargs)
        self._enum = enum_type

    def __call__(self, parser, namespace, values, option_string=None):
        value = self._enum(values)
        setattr(namespace, self.dest, value)

