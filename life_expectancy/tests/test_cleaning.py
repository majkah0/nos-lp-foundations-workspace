"""Tests for all modules"""

from unittest.mock import Mock, patch
import pandas as pd
from ..load_save import load_data, save_data
from ..cleaning import clean_data, CleanJson, CleanTsv
from ..main import main
from ..my_constants import BASE_DIR, Country, InputFileType
from . import OUTPUT_DIR, FIXTURES_DIR


def _correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Set correct data types.
    
    Args:
        df (pd.DataFrame): The data.

    Returns:
        df (pd.DataFrame): The modified data.
    """
    for col in ['unit', 'sex', 'age', 'region']:
        df[col] = df[col].astype('string')
    df['year'] = df['year'].astype('int')
    df['value'] = pd.to_numeric(
        df['value'])
    return df

def test_clean_data_tsv(pt_life_expectancy_tsv_input: pd.DataFrame,
                     pt_life_expectancy_cleaned_expected_tsv_input: pd.DataFrame):
    """Test for the clean_data function with the 'tsv' strategy
    
    Args:
        pt_life_expectancy_input (pd.DataFrame): Fixture for function input.
        pt_life_expectancy_cleaned_expected_tsv_input (pd.DataFrame): Fixture for function output.

    """
    pt_life_expectancy_cleaned_actual = clean_data(CleanTsv(), pt_life_expectancy_tsv_input, Country.PT)
    pd.testing.assert_frame_equal(pt_life_expectancy_cleaned_actual,
                                  _correct_data_types(pt_life_expectancy_cleaned_expected_tsv_input))

def test_clean_data_json(pt_life_expectancy_json_input: pd.DataFrame,
                     pt_life_expectancy_cleaned_expected_json_input: pd.DataFrame):
    """Test for the clean_data function with the 'json' strategy
    
    Args:
        pt_life_expectancy_json_input (pd.DataFrame): Fixture for function input.
        pt_life_expectancy_cleaned_expected_json_input (pd.DataFrame): Fixture for function output.

    """
    pt_life_expectancy_cleaned_actual = clean_data(CleanJson(), pt_life_expectancy_json_input, Country.PT)
    pd.testing.assert_frame_equal(pt_life_expectancy_cleaned_actual,
                                  _correct_data_types(pt_life_expectancy_cleaned_expected_json_input))

@patch("pandas.DataFrame.to_csv")
def test_save_data(to_csv_mock: Mock, pt_life_expectancy_cleaned_expected: pd.DataFrame):
    """Test for the save_data function
    
    Args:
        pt_life_expectancy_cleaned_expected (pd.DataFrame): Fixture for function output.

    """
    def _print_message(*args, **kwargs):
        print('Saved file')
    to_csv_mock.side_effect= _print_message
    save_data(pt_life_expectancy_cleaned_expected, Country.PT)
    expected_path = BASE_DIR / 'pt_life_expectancy.csv'
    to_csv_mock.assert_called_once_with(expected_path, index=False)

def test_main_tsv():
    """Test for the main function
       Read data from a json file
       Integration 
    """
    region = Country.PT
    file_type = InputFileType.tsv
    df_actual = main(region = region, file_type = file_type)
    df_expected = pd.read_csv(
        FIXTURES_DIR / 'pt_life_expectancy_total_expected_tsv.csv',index_col=[0])
    df_expected = _correct_data_types(df_expected)
    pd.testing.assert_frame_equal(
        df_actual, df_expected)

def test_main_json():
    """Test for the main function
       Read data from a json file
       Integration 
    """
    region = Country.PT
    file_type = InputFileType.json
    df_actual = main(region = region, file_type = file_type)
    df_expected = pd.read_csv(
        FIXTURES_DIR / 'pt_life_expectancy_total_expected_json.csv',index_col=[0])
    df_expected = _correct_data_types(df_expected)
    pd.testing.assert_frame_equal(
        df_actual, df_expected)
