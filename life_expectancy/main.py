import argparse
import pandas as pd
from life_expectancy import Country, InputFileType, EnumAction, country_name_from_code
from .load_save import load_data, save_data, LoadJson, LoadTsv
from .cleaning import clean_data, CleanJson, CleanTsv

def main(region: Country, file_type: InputFileType)-> pd.DataFrame:
    """Main function.
    
    Args:
        region (Country): The region to select.
        file_type (InputFileType): Input file type.
    """

    file_type_strategy = {'tsv':{'load_file': LoadTsv(), 'clean_data': CleanTsv()},
                          'json':{'load_file': LoadJson(), 'clean_data': CleanJson()}}
    print(f'Loading data from {file_type.name} file. '\
          f'Saving data for {region.value} ({country_name_from_code(region)}) region.')
    load_file_strategy = file_type_strategy[file_type.name]['load_file']
    clean_strategy = file_type_strategy[file_type.name]['clean_data']
    eu_life_expectancy_data = load_data(load_file_strategy)
    region_life_expectancy_data = clean_data(clean_strategy, eu_life_expectancy_data, 
                                             region = region)
    save_data(region_life_expectancy_data, region)
    return region_life_expectancy_data

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--region', type = Country, action = EnumAction,
                            default = Country.PT, help = 'Input region argument.' )
    parser.add_argument("-f", "--file_type", type = InputFileType, action = EnumAction,
                         default = InputFileType.tsv, 
                         help = 'Input file type argument.')
    args = parser.parse_args()
    main(region = args.region, file_type = args.file_type)
