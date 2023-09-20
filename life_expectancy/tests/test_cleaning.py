"""Tests for all modules"""

import pandas as pd
from ../load_save import load_data, save_data
from ../cleaning import clean_data
from ../main import main
from unittest.mock import Mock, patch
from . import OUTPUT_DIR

def test_clean_data() -> pd.DataFrame:
    pd.testing.assert_frame_equal(clean_data(pt_life_expectancy_input, 'PT'),
                                  pt_life_expectancy_expected)
    
@patch("load_save.pd.DataFrame.to_csv")
def test_save_data(to_csv_mock: Mock):
    to_csv_mock(side_effect=print('Saved data'))
    save_data(pt_life_expectancy_expected, 'PT')
    to_csv_mock.assert_called_once()

def test_main(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    region = 'PT'
    #how to put the fixture?
    pt_life_expectancy_actual = main(region = region)
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
