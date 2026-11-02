import pandas as pd

from src.data_validation import (
    aggregate_rejections,
    validate_bookings,
    validate_stay_dates,
)
from src.data_transformation import transform_dates

def test_booking_with_multiple_validation_failures():
    df = pd.DataFrame({
        "booking_id": ["B101", "B102", "B103"],
        "no_guests": [0, 2, 3],
        "revenue_generated": [5000, 3000, 4000],
        "booking_date": [
            "2026-oct-01",
            "2026-oct-01",
            "2026-oct-01",
        ],
        "check_in_date": [
            "2026-oct-15",
            "2026-oct-15",
            "2026-oct-20",
        ],
        "checkout_date": [
            "2026-oct-12",
            "2026-oct-18",
            "2026-oct-23",
        ],
    })

    invalid_bookings = validate_bookings(df)

    date_checked_df = transform_dates(df.copy())
    invalid_stays = validate_stay_dates(date_checked_df)

    rejected = aggregate_rejections(
        df,
        invalid_bookings,
        invalid_stays,
    )

    rejected_ids = set(rejected["booking_id"])
    cleaned = df.loc[~df["booking_id"].isin(rejected_ids)].copy()

    
    assert len(rejected) == 1
    assert rejected["booking_id"].tolist() == ["B101"]

    reasons = rejected.iloc[0]["validation_reason"]
    assert "negative_no_guests" in reasons
    assert "invalid_stay_dates" in reasons

    assert set(cleaned["booking_id"]) == {"B102", "B103"}

    assert set(cleaned["booking_id"]).isdisjoint(rejected_ids)
    assert len(cleaned) + len(rejected) == len(df)


def test_aggregate_rejections_returns_empty_dataframe_when_no_rejections():

    original_df = pd.DataFrame({
        "booking_id": ["B101", "B102"],
        "no_guests": [2, 3],
        "revenue_generated": [5000, 7000]
    })

    empty_rejections = original_df.iloc[0:0].copy()
    empty_rejections["validation_reason"] = pd.Series(dtype="object")

    rejected = aggregate_rejections(
        original_df,
        empty_rejections
    )

    assert rejected.empty
    assert len(rejected) == 0

    expected_columns = list(original_df.columns) + ["validation_reason"]

    assert list(rejected.columns) == expected_columns




def test_aggregate_rejections_removes_duplicate_reasons():

    original_df = pd.DataFrame({
        "booking_id": ["B101", "B102"],
        "no_guests": [0, 2],
        "revenue_generated": [5000, 7000]
    })

    rejection_stage_1 = pd.DataFrame({
        "booking_id": ["B101"],
        "validation_reason": ["negative_no_guests"]
    })

    rejection_stage_2 = pd.DataFrame({
        "booking_id": ["B101"],
        "validation_reason": ["negative_no_guests"]
    })

    rejected = aggregate_rejections(
        original_df,
        rejection_stage_1,
        rejection_stage_2
    )

    assert len(rejected) == 1
    assert rejected.iloc[0]["booking_id"] == "B101"

    reasons = rejected.iloc[0]["validation_reason"]

    assert reasons == "negative_no_guests"
    assert reasons.count("negative_no_guests") == 1