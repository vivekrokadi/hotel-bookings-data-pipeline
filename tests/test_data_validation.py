import pytest
import pandas as pd
from src.data_validation import validate_bookings, validation_report

@pytest.mark.parametrize(
    "no_guests, revenue_generated, expected",
    [
        (0, 100, 1),
        (-1, 100, 1),
        (float("nan"), 100,1),
        (2, 0, 1),
        (2, -100, 1),
        (2, 500, 0),
    ]
)

def test_validate_bookings(no_guests, revenue_generated, expected):
    df = pd.DataFrame({
        "no_guests": [no_guests],
        "revenue_generated": [revenue_generated]
    })
    
    result = validate_bookings(df)

    assert len(result) == expected


def test_validation_report():
    total_records = 0
    invalid_count = 0
    result = validation_report(total_records, invalid_count)

    assert result['total_records'] == 0
    assert result['invalid_records'] == 0
    assert result['invalid_percentage'] == 0
