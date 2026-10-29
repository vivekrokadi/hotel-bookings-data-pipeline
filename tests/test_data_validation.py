import pytest
import pandas as pd
from src.data_validation import validate_bookings, validation_report, validate_stay_dates
from src.data_transformation import transform_dates

@pytest.mark.parametrize(
    "no_guests, revenue_generated, expected, validation_reason",
    [
        (0, 100, 1, 'negative_no_guests'),
        (-1, 100, 1, 'negative_no_guests'),
        (float("nan"), 100,1, 'missing_no_guests'),
        (2, -100, 1, 'negative_revenue_generated'),
        (2, float('nan'), 1, 'missing_revenue_generated'),
        (-2, float('nan'), 1, 'negative_no_guests; missing_revenue_generated'),
    ]
)

def test_validate_bookings(no_guests, revenue_generated, expected, validation_reason):
    df = pd.DataFrame({
        "no_guests": [no_guests],
        "revenue_generated": [revenue_generated]
    })
    
    result = validate_bookings(df)

    assert len(result) == expected
    assert result['validation_reason'].iloc[0] == validation_reason


def test_validation_report():
    total_records = 0
    invalid_count = 0
    result = validation_report(total_records, invalid_count)

    assert result['total_records'] == 0
    assert result['invalid_records'] == 0
    assert result['invalid_percentage'] == 0


@pytest.mark.parametrize(
    "check_in_date, checkout_date, expected, validation_reason",
    [
        (float('nan'), float('nan'), 1, 'missing_check_in_date; missing_checkout_date'),
        ('2026-oct-12', '2026-oct-10', 1, 'invalid_stay_dates'),
        (float('nan'), '2026-oct-10', 1, 'missing_check_in_date')
    ]
)


def test_validate_stay_dates(check_in_date, checkout_date, expected, validation_reason):
    df = pd.DataFrame({
        "booking_date": ["2026-oct-01"],
        "check_in_date": [check_in_date],
        "checkout_date": [checkout_date],
    })
    df = transform_dates(df)

    result = validate_stay_dates(df)

    assert len(result) == expected
    assert result['validation_reason'].iloc[0] == validation_reason