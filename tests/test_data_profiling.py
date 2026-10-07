from src.data_profiling import profile_dataframe
import pandas as pd


def test_data_profiling():
    df = pd.DataFrame({
        'no_guests': [2, 0, float('nan')],
        'revenue_generated': [500, 200, 100],
        'hotel': ['A', 'B', 'B']
    })

    result = profile_dataframe(df)
    print(result)
    assert result['row_count'] == 3
    assert result['column_count'] == 3
    assert result['missing_values'].sum() == 1
    assert result['duplicate_rows'] == 0


