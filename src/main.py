from data_loader import load_csv
from data_validation import validate_bookings, validation_report, validate_booking_metrics, booking_metric_validation_report
from data_cleaning import clean_bookings
from data_profiling import profile_dataframe
from data_transformation import transform_dates, count_invalid_dates, create_booking_metrics
from logger_config import setup_logger

setup_logger()
   
df_bookings = load_csv("fact_bookings.csv")

invalid_records = validate_bookings(df_bookings)

cleaned_bookings = clean_bookings(df_bookings)

print("Original records:", len(df_bookings))
print("Invalid records:", len(invalid_records))
print("Cleaned records:", len(cleaned_bookings))

report = validation_report(len(df_bookings), len(invalid_records))
print("Booking validation report:", report)

profile = profile_dataframe(df_bookings)
print("row_count: ",profile['row_count'])
print("column_count: ",profile['column_count'])
print("missing_values: ",profile['missing_values'])
print("duplicate_rows: ",profile['duplicate_rows'])

cleaned_bookings = transform_dates(cleaned_bookings)

raw_date_check = transform_dates(df_bookings.copy())
print("Invalid or missing dates in raw data:", count_invalid_dates(raw_date_check))
print("Invalid dates count after cleaning: ",count_invalid_dates(cleaned_bookings))

cleaned_bookings = create_booking_metrics(cleaned_bookings)

invalid_metric_records = validate_booking_metrics(cleaned_bookings)

metric_report  = booking_metric_validation_report(len(cleaned_bookings), len(invalid_metric_records))

print("Booking metric validation report:", metric_report)

