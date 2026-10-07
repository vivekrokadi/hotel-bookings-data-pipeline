
def profile_dataframe(df):
    return {
        'row_count': df.shape[0],
        'column_count': df.shape[1],
        'missing_values': df.isna().sum(),
        'duplicate_rows': df.duplicated().sum()
    } 