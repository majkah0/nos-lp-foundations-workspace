from enum import Enum, unique, auto

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

Country = Enum('Country', EUROSTAT_COUNTRY_DICT | EUROSTAT_OTHER_DICT)
Country.country_names = _country_names
Country.country_codes = _country_codes


class InputFileType(Enum):
        tsv = auto()
        json = auto()

