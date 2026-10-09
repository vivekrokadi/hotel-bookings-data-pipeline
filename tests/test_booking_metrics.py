from src.data_transformation import create_booking_metrics, transform_dates
import pytest
import pandas as pd

@pytest.mark.parametrize(
    "booking_date, check_in_date, checkout_date, lead_time_days, no_of_days_stayed",
    [
        ('2026-july-05', '2026-july-10', '2026-july-14', 5, 4),
        ('2026-july-05', '2026-july-10', float("nan"), 5, float("nan")),
        ('2026-july-16', '2026-july-16', '2026-july-17', 0, 1)
        
    ]
)

def test_booking_metrics(booking_date, check_in_date, checkout_date, lead_time_days, no_of_days_stayed):
    df = pd.DataFrame({
        "booking_date": [booking_date],
        "check_in_date": [check_in_date],
        "checkout_date": [checkout_date],
    })
    df = transform_dates(df)
    df = create_booking_metrics(df)

    assert df['lead_time_days'].iloc[0] == lead_time_days
    if pd.isna(no_of_days_stayed):
        assert pd.isna(df['no_of_days_stayed'].iloc[0])
    else:
        assert df['no_of_days_stayed'].iloc[0] == no_of_days_stayed
  
