from src.data_validation import validate_booking_metrics, booking_metric_validation_report
import pandas as pd
import pytest

def test_booking_metric_validation():
    df = pd.DataFrame({
        "lead_time_days": [5, -2, 3, 4],
        "no_of_days_stayed": [2, 3, -1, float("nan")]
    })

    result = validate_booking_metrics(df)

    assert len(result) == 3
    assert 0 not in result.index

    assert 1 in result.index
    assert 2 in result.index
    assert 3 in result.index

@pytest.mark.parametrize(
    "total_records, invalid_metric_records_count, expected",
    [
        (0, 134578, 0),
        (134578, 200, 0.15),
        (100, 100, 100.0),
        
    ]
)
def test_booking_metric_validation_report(total_records, invalid_metric_records_count, expected):

    result = booking_metric_validation_report(total_records, invalid_metric_records_count)

    assert result['invalid_percentage'] == expected


