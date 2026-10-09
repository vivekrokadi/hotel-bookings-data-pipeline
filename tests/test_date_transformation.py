from src.data_transformation import transform_dates, count_invalid_dates
import pytest
import pandas as pd

@pytest.mark.parametrize(
    "booking_date, check_in_date, checkout_date",
    [
        ('18-6-22', '9/7/2022', '15/07/2022') 
    ]
)

def test_transform_dates(booking_date, check_in_date, checkout_date):
    df = pd.DataFrame({
        "booking_date": [booking_date],
        "check_in_date": [check_in_date],
        "checkout_date": [checkout_date]
    })
        
    result = transform_dates(df)
    assert pd.api.types.is_datetime64_any_dtype(result['booking_date'])
    assert pd.api.types.is_datetime64_any_dtype(result['check_in_date'])
    assert pd.api.types.is_datetime64_any_dtype(result['checkout_date'])
    
    assert result["booking_date"].iloc[0] == pd.Timestamp("2022-06-18")
    assert result["check_in_date"].iloc[0] == pd.Timestamp("2022-07-09")
    assert result["checkout_date"].iloc[0] == pd.Timestamp("2022-07-15")


def test_valid_dates():
    df = pd.DataFrame({
        'booking_date': ['18-08-2026'],
        'check_in_date': ['23-08-26'],
        'checkout_date': ['30/08/2022']
    })
    result = transform_dates(df)
    invalid_count = count_invalid_dates(result)
    assert invalid_count['booking_date'] == 0
    assert invalid_count['check_in_date'] == 0
    assert invalid_count['checkout_date'] == 0

def test_invalid_dates():
    df = pd.DataFrame({
        'booking_date': ['Invalid_date'],
        'check_in_date': ["20date"],
        'checkout_date': ['35/07/2022']
    })

    result = transform_dates(df)

    assert pd.isna(result["booking_date"].iloc[0])
    assert pd.isna(result["check_in_date"].iloc[0])
    assert pd.isna(result["checkout_date"].iloc[0])