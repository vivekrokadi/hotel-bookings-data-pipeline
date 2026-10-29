import pandas as pd

def validate_bookings(df):
    invalid_condition = (
            (df['no_guests'] <= 0) |
            (df['revenue_generated'] <= 0) |
            (df['no_guests'].isna()) |
            (df['revenue_generated'].isna())
        )
    invalid_records = df.loc[invalid_condition].copy()
    invalid_records['validation_reason'] = ''

    validation_rules = [
        (
            invalid_records['no_guests'] <= 0,
            'negative_no_guests'
        ),
        (
            invalid_records['revenue_generated'] <= 0,
            'negative_revenue_generated'
        ),
        (
            invalid_records['no_guests'].isna(),
            'missing_no_guests'
        ),
        (
            invalid_records['revenue_generated'].isna(),
            'missing_revenue_generated'
        )
    ]

    for condition, reason in validation_rules:
        current_reason = invalid_records.loc[
            condition, 'validation_reason'
        ]
    
        invalid_records.loc[condition, 'validation_reason'] = (
        current_reason
            .apply(lambda existing: f'{existing}; {reason}' if existing else reason)
        )

    

    return invalid_records

def validation_report(total_records, invalid_count):
    if total_records == 0:
        invalid_percentage = 0
    else:
       invalid_percentage = round((invalid_count/total_records)*100, 2)

        
    return {
    "total_records": total_records,
    "invalid_records": invalid_count,
    "invalid_percentage": invalid_percentage
    }



def validate_booking_metrics(df):
    invalid_condition = (
        (df['lead_time_days'] < 0) |
        (df['no_of_days_stayed'] < 0) |
        (df['lead_time_days'].isna()) |
        (df['no_of_days_stayed'].isna())
    )

    invalid_records = df.loc[invalid_condition].copy()
    invalid_records['validation_reason'] = ''

    validation_rules = [
        (
            invalid_records['lead_time_days'] < 0,
            'negative_lead_time'
        ),
        (
            invalid_records['no_of_days_stayed'] < 0,
            'negative_stay_duration'
        ),
        (
            invalid_records['lead_time_days'].isna(),
            'missing_lead_time'
        ),
        (
            invalid_records['no_of_days_stayed'].isna(),
            'missing_stay_duration'
        )
    ]

    for condition, reason in validation_rules:
        current_reason = invalid_records.loc[
            condition, 'validation_reason'
        ]

        invalid_records.loc[condition, 'validation_reason'] = (
            current_reason
            .apply(lambda existing: f'{existing}; {reason}' if existing else reason)
        )

    return invalid_records


def booking_metric_validation_report(total_records, invalid_metric_records_count):
    if total_records == 0:
        invalid_percentage = 0
    else:
        invalid_percentage = round((invalid_metric_records_count/total_records)*100, 2)

    return {
        'total_records' : total_records,
        'invalid_count': invalid_metric_records_count,
        'invalid_percentage': invalid_percentage
    }

def validate_stay_dates(df):
    invalid_condition = (
        (df['checkout_date'] <= df['check_in_date']) |
        (df['check_in_date'].isna()) | 
        (df['checkout_date'].isna())
    )

    invalid_records = df.loc[invalid_condition].copy()

    invalid_records['validation_reason'] = ''

    validation_rules = [
        (
            invalid_records['checkout_date'] <= invalid_records['check_in_date'], 'invalid_stay_dates'
        ),
        (
            invalid_records['check_in_date'].isna(),
            'missing_check_in_date'
        ),
        (
            invalid_records['checkout_date'].isna(),
            'missing_checkout_date'
        )
    ]

    for condition, reason in validation_rules:
        current_reason = invalid_records.loc[
            condition, 'validation_reason'
        ]
    
        invalid_records.loc[condition, 'validation_reason'] = (
            current_reason
            .apply(lambda existing: f'{existing}; {reason}' if existing else reason)
        )

    return invalid_records


def aggregate_rejections(original_df, *rejection_dataframes):

    reason_frames = []

    for rejected_df in rejection_dataframes:
        if rejected_df.empty:
            continue

        required_columns = {"booking_id", "validation_reason"}
        missing_columns = required_columns - set(rejected_df.columns)

        if missing_columns:
            raise ValueError(
                f"Rejection DataFrame is missing columns: {missing_columns}"
            )

        reasons = rejected_df[["booking_id", "validation_reason"]].copy()
        reasons = reasons.dropna(subset=["booking_id", "validation_reason"])
        reason_frames.append(reasons)

    if not reason_frames:
        result = original_df.iloc[0:0].copy()
        result["validation_reason"] = pd.Series(dtype="object")
        return result

    all_reasons = pd.concat(reason_frames, ignore_index=True)

    all_reasons["validation_reason"] = all_reasons["validation_reason"].str.split("; ")
    all_reasons = all_reasons.explode("validation_reason")
    all_reasons["validation_reason"] = all_reasons["validation_reason"].str.strip()
    all_reasons = all_reasons[
        all_reasons["validation_reason"].ne("")
    ].drop_duplicates(["booking_id", "validation_reason"])

    aggregated_reasons = (
        all_reasons.groupby("booking_id", sort=False)["validation_reason"]
        .agg("; ".join)
        .reset_index()
    )
    rejected_bookings = original_df.merge(
        aggregated_reasons,
        on="booking_id",
        how="inner",
        validate="one_to_one"
    )

    return rejected_bookings
