from data_loader import load_csv
from data_validation import validate_bookings, validation_report, validate_booking_metrics, booking_metric_validation_report, validate_stay_dates
from data_cleaning import clean_bookings
from data_profiling import profile_dataframe
from data_transformation import transform_dates, count_invalid_dates, create_booking_metrics
from logger_config import setup_logger
import logging
from data_writer import save_records
import pandas as pd

setup_logger()
logger = logging.getLogger(__name__)

logger.info("Hotel bookings data pipeline started")

df_bookings = load_csv("fact_bookings.csv")
logger.info("Data loaded successfully")

invalid_records = validate_bookings(df_bookings)
logger.info("Booking validation completed. Found %s invalid records out of %s", len(invalid_records), len(df_bookings))
logger.warning("%s Invalid records found", len(invalid_records))
print(invalid_records)

cleaned_bookings = clean_bookings(df_bookings)
logger.info("%s cleaned records remaining", len(cleaned_bookings))

# print("Original records:", len(df_bookings))
# print("Invalid records:", len(invalid_records))
# print("Cleaned records:", len(cleaned_bookings))

report = validation_report(len(df_bookings), len(invalid_records))
print("Booking validation report:", report)

profile = profile_dataframe(df_bookings)
print("row_count: ",profile['row_count'])
print("column_count: ",profile['column_count'])
print("missing_values: ",profile['missing_values'])
print("duplicate_rows: ",profile['duplicate_rows'])



cleaned_bookings = transform_dates(cleaned_bookings)
invalid_dates = count_invalid_dates(cleaned_bookings)

if (invalid_dates['check_in_date'] > 0) & (invalid_dates['check_in_date'] > 0) & (invalid_dates['check_in_date'] > 0):
    logger.warning("%s Invalid or missing dates found after cleaning",count_invalid_dates(cleaned_bookings))
else:
    logger.info("No Invalid or missing dates detected")


# print("Invalid dates count after cleaning: ",count_invalid_dates(cleaned_bookings))

invalid_stay_records = validate_stay_dates(cleaned_bookings)
logger.info(
    "Found %s bookings with invalid stay dates",
    len(invalid_stay_records)
)


invalid_stay_indices = invalid_stay_records.index

cleaned_bookings = cleaned_bookings.drop(
    index=invalid_stay_indices
).copy()

logger.info(
    "%s bookings remain after stay-date validation",
    len(cleaned_bookings)
)

rejected_bookings = pd.concat(
    [invalid_records, invalid_stay_records],
    ignore_index=True,
    sort=False
)
cleaned_bookings = create_booking_metrics(cleaned_bookings)
logger.info("Booking metrics created successfully")

invalid_metric_records = validate_booking_metrics(cleaned_bookings)
print(invalid_metric_records)
if len(invalid_metric_records) > 0:
    logger.warning("%s invalid metric records found", len(invalid_metric_records))
else:
    logger.info("No invalid metric records found")

metric_report  = booking_metric_validation_report(len(cleaned_bookings), len(invalid_metric_records))

print("Booking metric validation report:", metric_report)

save_records(cleaned_bookings, 'processed/cleaned_bookings.csv')
save_records(rejected_bookings, 'rejected/invalid_bookings.csv')

