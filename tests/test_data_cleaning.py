from src.data_cleaning import clean_bookings
import pandas as pd

def test_clean_bookings():
    df = pd.DataFrame({
        'no_guests': [0, 2],
        'revenue_generated': [100, 100]
    })

    result = clean_bookings(df)

    assert len(result) == 1
    assert result['no_guests'].iloc[0] == 2