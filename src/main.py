from data_loader import load_csv
from data_validation import validate_bookings, validation_report
from data_cleaning import clean_bookings
from data_profiling import profile_dataframe
from data_transformation import transform_dates, count_invalid_dates, create_booking_metrics
import pandas as pd

df_bookings = load_csv("fact_bookings.csv")
df_agg_bookings = load_csv("fact_aggregated_bookings.csv")
df_hotels = load_csv("dim_hotels.csv")
df_rooms = load_csv("dim_rooms.csv")
df_date = load_csv("dim_date.csv")


invalid_records = validate_bookings(df_bookings)

cleaned_bookings = clean_bookings(df_bookings)


# print("Original records:", len(df_bookings))
# print("Invalid records:", len(invalid_records))
# print("Cleaned records:", len(cleaned_bookings))

# report = validation_report(len(df_bookings), len(invalid_records))

# print(report)

# profile = profile_dataframe(df_bookings)
# print("row_count: ",profile['row_count'])
# print("column_count: ",profile['column_count'])
# print("missing_values: ",profile['missing_values'])
# print("duplicate_rows: ",profile['duplicate_rows'])

cleaned_bookings = transform_dates(cleaned_bookings)

# print(cleaned_bookings['booking_date'].head())

# print(count_invalid_dates(df_bookings))

cleaned_bookings = create_booking_metrics(cleaned_bookings)

print(cleaned_bookings)