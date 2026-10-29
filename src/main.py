
import logging

from data_cleaning import clean_bookings
from data_loader import load_csv
from data_profiling import profile_dataframe
from data_transformation import (
    count_invalid_dates,
    create_booking_metrics,
    transform_dates,
)
from data_validation import (
    aggregate_rejections,
    booking_metric_validation_report,
    validate_booking_metrics,
    validate_bookings,
    validate_stay_dates,
    validation_report,
)
from data_writer import save_records
from logger_config import setup_logger


def main():
    setup_logger()
    logger = logging.getLogger(__name__)

    logger.info("Hotel bookings data pipeline started")

    # 1. Load and preserve the original input.
    df_bookings = load_csv("fact_bookings.csv")
    logger.info("Loaded %s input bookings", len(df_bookings))

    # Validate the key used to track bookings across stages.
    if "booking_id" not in df_bookings.columns:
        raise ValueError("Input data must contain a booking_id column")

    if df_bookings["booking_id"].isna().any():
        raise ValueError(
            "booking_id contains missing values; cannot reliably track rejections"
        )

    if df_bookings["booking_id"].duplicated().any():
        raise ValueError(
            "booking_id contains duplicates; cannot reliably aggregate rejections"
        )

    # 2. Profile the original data.
    profile = profile_dataframe(df_bookings)
    logger.info("Input profile: %s", profile)

    # 3. Validate guest count and revenue.
    invalid_records = validate_bookings(df_bookings)

    logger.info(
        "Initial validation found %s invalid bookings out of %s",
        len(invalid_records),
        len(df_bookings),
    )

    logger.info(
        "Initial validation report: %s",
        validation_report(len(df_bookings), len(invalid_records)),
    )

    # 4. Validate dates using a transformed copy of ALL original records.
    # This allows one booking to receive multiple rejection reasons.
    date_check_bookings = transform_dates(df_bookings.copy())

    invalid_dates = count_invalid_dates(date_check_bookings)

    if any(count > 0 for count in invalid_dates.values()):
        logger.warning("Missing or unparseable dates detected: %s", invalid_dates)
    else:
        logger.info("No missing or unparseable dates detected")

    invalid_stay_records = validate_stay_dates(date_check_bookings)

    logger.info(
        "Stay-date validation found %s invalid bookings",
        len(invalid_stay_records),
    )

    # 5. Aggregate initial and stay-date failures.
    rejected_before_metrics = aggregate_rejections(
        df_bookings,
        invalid_records,
        invalid_stay_records,
    )

    rejected_ids_before_metrics = set(
        rejected_before_metrics["booking_id"].tolist()
    )

    # 6. Create a working dataset containing eligible bookings only.
    eligible_bookings = clean_bookings(df_bookings)

    working_bookings = eligible_bookings.loc[
        ~eligible_bookings["booking_id"].isin(rejected_ids_before_metrics)
    ].copy()

    logger.info(
        "%s bookings remain after initial and stay-date validation",
        len(working_bookings),
    )

    # 7. Transform dates and calculate metrics for eligible bookings.
    working_bookings = transform_dates(working_bookings)
    working_bookings = create_booking_metrics(working_bookings)

    logger.info("Booking metrics created successfully")

    # 8. Validate derived metrics.
    invalid_metric_records = validate_booking_metrics(working_bookings)

    logger.info(
        "Metric validation found %s invalid bookings",
        len(invalid_metric_records),
    )

    metric_report = booking_metric_validation_report(
        len(working_bookings),
        len(invalid_metric_records),
    )

    logger.info("Booking metric validation report: %s", metric_report)

    # 9. Combine all rejection reasons into one row per booking_id.
    rejected_bookings = aggregate_rejections(
        df_bookings,
        invalid_records,
        invalid_stay_records,
        invalid_metric_records,
    )

    rejected_ids = set(rejected_bookings["booking_id"].tolist())

    # Keep transformed dates and metrics in the clean output.
    cleaned_bookings = working_bookings.loc[
        ~working_bookings["booking_id"].isin(rejected_ids)
    ].copy()

    # 10. Verify that clean and rejected outputs do not overlap.
    cleaned_ids = set(cleaned_bookings["booking_id"].tolist())
    rejected_id_set = set(rejected_bookings["booking_id"].tolist())

    if cleaned_ids.intersection(rejected_id_set):
        raise RuntimeError(
            "Record reconciliation failed: cleaned and rejected outputs overlap"
        )

    # Verify that every input record appears in exactly one output.
    accounted_records = len(cleaned_bookings) + len(rejected_bookings)

    if accounted_records != len(df_bookings):
        raise RuntimeError(
            "Record reconciliation failed: "
            f"input={len(df_bookings)}, "
            f"cleaned={len(cleaned_bookings)}, "
            f"rejected={len(rejected_bookings)}"
        )

    logger.info(
        "Record reconciliation passed: input=%s, cleaned=%s, rejected=%s",
        len(df_bookings),
        len(cleaned_bookings),
        len(rejected_bookings),
    )

    # 11. Save the final outputs.
    save_records(
        cleaned_bookings,
        "processed/cleaned_bookings.csv",
    )

    save_records(
        rejected_bookings,
        "rejected/invalid_bookings.csv",
    )

    logger.info("Hotel bookings data pipeline completed successfully")


if __name__ == "__main__":
    main()
