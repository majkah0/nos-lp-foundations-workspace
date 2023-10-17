import argparse
import pandas as pd
from load_save import load_data, save_data, LoadJson, LoadTsv
from cleaning import clean_data

BASE_DIR = Path().cwd() / 'life_expectancy' / 'data'

def main(region: str, file_type: str)-> pd.DataFrame:
    """Main function.
    
    Args:
        region (str): The region to select.
    """
    file_type_strategy = {'tsv':{'load_file': LoadTsv(), 'clean_data': CleanTsv()},
                          'json':{'load_file': LoadJson, 'clean_data': CleanJson}}
    load_file_strategy = file_type_strategy[file_type]['load_file']
    clean_strategy = file_type_strategy[file_type]['clean_data']
    eu_life_expectancy_data = load_data(load_file_strategy)
    region_life_expectancy_data = clean_data(clean_strategy, eu_life_expectancy_data, 
                                             region = region)
    save_data(region_life_expectancy_data, region)
    return region_life_expectancy_data

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region",
                         default = 'PT', 
                         help = 'Input region argument.',
                         type = str)
    parser.add_argument("-f", "--file_type",
                         default = 'tsv', 
                         help = 'Input file type argument.',
                         type = str)
    args = parser.parse_args()
    main(region = args.region)
