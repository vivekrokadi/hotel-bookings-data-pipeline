def clean_bookings(df):
    df = df[(df['no_guests'] > 0) & (df['revenue_generated'] > 0)]

    return df