import pandas as pd

import src.main as pipeline


def test_pipeline_processes_valid_and_invalid_bookings(monkeypatch):
    input_df = pd.DataFrame({
        "booking_id": ["B101", "B102", "B103", "B104"],
        "booking_date": [
            "2026-10-01",
            "2026-10-02",
            "2026-10-03",
            "2026-10-04"
        ],
        "check_in_date": [
            "2026-10-15",
            "2026-10-20",
            "2026-10-25",
            "2026-10-18"
        ],
        "checkout_date": [
            "2026-10-18",
            "2026-10-17", 
            "2026-10-23",  
            "2026-10-21"
        ],
        "no_guests": [0, 2, 0, 3],
        "revenue_generated": [5000, 6000, 7000, 8000]
    })

    saved_outputs = {}

    monkeypatch.setattr(
        pipeline,
        "load_csv",
        lambda filename: input_df.copy()
    )

    monkeypatch.setattr(
        pipeline,
        "setup_logger",
        lambda: None
    )

    def fake_save_records(df, filename):
        saved_outputs[filename] = df.copy()

    monkeypatch.setattr(
        pipeline,
        "save_records",
        fake_save_records
    )

    pipeline.main()

    cleaned = saved_outputs["processed/cleaned_bookings.csv"]
    rejected = saved_outputs["rejected/invalid_bookings.csv"]

    assert cleaned["booking_id"].tolist() == ["B104"]

    assert "lead_time_days" in cleaned.columns
    assert "no_of_days_stayed" in cleaned.columns

    assert cleaned.iloc[0]["no_of_days_stayed"] == 3

    assert set(rejected["booking_id"]) == {
        "B101",
        "B102",
        "B103"
    }

    assert rejected["booking_id"].tolist().count("B103") == 1

    b103_reasons = rejected.loc[
        rejected["booking_id"] == "B103",
        "validation_reason"
    ].iloc[0]

    assert "negative_no_guests" in b103_reasons
    assert "invalid_stay_dates" in b103_reasons

    cleaned_ids = set(cleaned["booking_id"])
    rejected_ids = set(rejected["booking_id"])

    assert cleaned_ids.isdisjoint(rejected_ids)

    assert len(cleaned) + len(rejected) == len(input_df)

    assert cleaned_ids.union(rejected_ids) == set(input_df["booking_id"])
