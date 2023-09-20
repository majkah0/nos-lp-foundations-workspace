import argparse
import pandas as pd
from load_save import load_data, save_data
from cleaning import clean_data

def main(region: str)-> pd.DataFrame:
    """Main function.
    
    Args:
        region (str): The region to select.
    """
    eu_life_expectancy_data = load_data()
    region_life_expectancy_data = clean_data(eu_life_expectancy_data, region = region)
    save_data(region_life_expectancy_data, region)
    return region_life_expectancy_data

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region",
                         default = 'PT', 
                         help = 'Input region argument.',
                         type = str)
    args = parser.parse_args()
    main(region = args.region)
