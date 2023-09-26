"""Tests for all modules"""

import pandas as pd
from ..load_save import load_data, save_data
from ..cleaning import clean_data
from ..main import main
from unittest.mock import Mock, patch
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

def test_clean_data(pt_life_expectancy_input -> pd.DataFrame,
                     pt_life_expectancy_cleaned_expected -> pd.DataFrame):
    """Test for the clean_data function
    
    Args:
        pt_life_expectancy_input (pd.DataFrame): Fixture for function input.
        pt_life_expectancy_cleaned_expected (pd.DataFrame): Fixture for function output.

    """

    pt_life_expectancy_cleaned_actual = clean_data(pt_life_expectancy_input, 'PT')
    pd.testing.assert_frame_equal(pt_life_expectancy_cleaned_actual,
                                  _correct_data_types(pt_life_expectancy_cleaned_expected))

def test_save_data(pt_life_expectancy_cleaned_expected -> pd.DataFrame):
    """Test for the save_data function
    
    Args:
        pt_life_expectancy_cleaned_expected (pd.DataFrame): Fixture for function output.

    """
    def print_message(*args, **kwargs):
        print(f'Saved file')
    to_csv_mock = Mock(side_effect=print_message())
    with patch("./load_save.save_data.pd.DataFrame.to_csv", to_csv_mock):
         to_csv_mock()
         save_data(pt_life_expectancy_cleaned_expected, 'PT')
         to_csv_mock.assert_called_once_with('pt_life_expectancy.csv', sep=',', index=False)

def test_main():
    """Test for the main function
       Integration test
    """
    region = 'PT'
    df_actual = main(region = region)
    df_expected = pd.read_csv(
        FIXTURES_DIR / 'pt_life_expectancy_total_expected.csv',index_col=[0])
    df_expected = _correct_data_types(df_expected)
    pd.testing.assert_frame_equal(
        df_actual, df_expected)
