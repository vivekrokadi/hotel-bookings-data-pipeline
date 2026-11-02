# Hotel Bookings Data Pipeline

A Python-based ETL pipeline built using **Pandas** to process hotel booking data, perform data quality checks, transform booking information, calculate useful metrics, and separate valid and invalid records.

## 1. Project Overview

This project demonstrates a batch data processing workflow using Python and Pandas.

The pipeline reads raw hotel booking data from a CSV file, performs data profiling and validation, cleans records, transforms date columns, calculates booking metrics, and generates separate outputs for valid and rejected records.

The project also includes automated tests using Pytest to verify individual processing functions and the overall pipeline workflow.

## 2. Business Problem

Raw booking data may contain invalid values, missing information, or inconsistent date information.

Processing such data without proper validation can lead to inaccurate metrics and unreliable analytical results.

This pipeline addresses these problems by:

- Profiling incoming booking data.
- Identifying invalid booking records.
- Validating booking and stay-date information.
- Transforming date columns into appropriate datetime formats.
- Calculating booking-related metrics.
- Maintaining rejection reasons for invalid records.
- Producing separate cleaned and rejected datasets.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Pipeline implementation |
| Pandas | Data processing and transformation |
| Pytest | Automated testing |
| Logging | Pipeline execution tracking |
| CSV | Input and output data storage |
| Git & GitHub | Version control |

## 4. Pipeline Architecture

```text
          Raw Booking Data
           fact_bookings.csv
                  |
                  v
             Data Loading
                  |
                  v
             Data Profiling
                  |
                  v
          Initial Validation
                  |
                  v
          Date Transformation
                  |
                  v
          Stay-Date Validation
                  |
                  v
          Rejection Aggregation
                  |
                  v
          Eligible Bookings
                  |
                  v
         Booking Metric Creation
                  |
                  v
          Metric Validation
                  |
                  v
          Record Reconciliation
                  |
             +----+----+
             |         |
             v         v
       Cleaned Data   Rejected Data
             |         |
             v         v
      cleaned_
      bookings.csv   invalid_bookings.csv
```

## 5. Project Structure

```text
Hotels-Analysis/
│
├── data/
│   ├── raw/
│   │   └── fact_bookings.csv
│   │
│   ├── processed/
│   │   └── cleaned_bookings.csv
│   │
│   └── rejected/
│       └── invalid_bookings.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_validation.py
│   ├── data_cleaning.py
│   ├── data_transformation.py
│   ├── data_profiling.py
│   ├── data_writer.py
│   ├── logger_config.py
│   └── main.py
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_data_validation.py
│   ├── test_data_cleaning.py
│   ├── test_data_transformation.py
│   ├── test_data_profiling.py
│   ├── test_data_writer.py
│   ├── test_rejection_aggregation.py
│   └── test_pipeline.py
│
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

## 6. Pipeline Workflow

### Step 1: Data Loading

Loads the raw hotel booking dataset from a CSV file using Pandas.

### Step 2: Data Profiling

Generates an initial overview of the dataset, including:

- Total number of rows.
- Total number of columns.
- Missing values.
- Duplicate rows.

### Step 3: Data Validation

Validates important booking attributes, including:

- Guest count.
- Generated revenue.
- Missing values in critical fields.
- Stay-date consistency.

Invalid records are identified along with their validation reasons.

### Step 4: Data Cleaning

Filters out records that fail the initial guest-count and revenue conditions.

### Step 5: Date Transformation

Converts booking, check-in, and checkout dates into datetime values.

Unparseable date values are converted to missing datetime values for validation.

### Step 6: Booking Metrics

Calculates:

- **Lead Time:** Number of days between booking date and check-in date.
- **Stay Duration:** Number of days between check-in and checkout dates.

### Step 7: Rejection Aggregation

Combines rejection reasons from different validation stages.

Each rejected booking is maintained once, even if it fails multiple validation rules.

### Step 8: Record Reconciliation

Verifies that:

- Cleaned and rejected records do not overlap.
- Every input booking is accounted for.
- The total number of cleaned and rejected records matches the input count.

### Step 9: Output Generation

Saves the final datasets into separate CSV files:

- `data/processed/cleaned_bookings.csv`
- `data/rejected/invalid_bookings.csv`

## 7. Data Quality Rules

The pipeline applies the following validation checks:

| Field | Validation rule |
|---|---|
| booking_id | Must be present and unique |
| no_guests | Must be greater than zero |
| revenue_generated | Must be greater than zero |
| check_in_date | Must be present and valid |
| checkout_date | Must be after check-in date |
| lead_time_days | Must not be negative or missing |
| no_of_days_stayed | Must not be negative or missing |

The pipeline also maintains rejection reasons to help identify why individual records failed validation.

**Note:** Missing ratings are not automatically treated as invalid because ratings may be optional in booking data.

## 8. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- pip

### Clone the repository

```bash
git clone https://github.com/vivekrokadi/hotel-bookings-data-pipeline.git

cd Hotels-Analysis
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

Place the source dataset at:

```text
data/raw/fact_bookings.csv
```

## 9. Running the Pipeline

From the project root directory, execute:

```bash
python src/main.py
```

The pipeline processes the input dataset and generates the cleaned and rejected CSV outputs.

Execution details are recorded through Python logging.

## 10. Running Tests

This project uses Pytest for automated testing.

Run the complete test suite:

```bash
pytest
```

Run tests with detailed output:

```bash
pytest -v
```

Run the integration test separately:

```bash
pytest tests/test_pipeline.py -v
```

**Current test result: 30 tests passed.**

The test suite covers data loading, validation, cleaning, transformations, profiling, output writing, rejection aggregation, and pipeline integration.

## 11. Sample Execution Results

The pipeline was executed against a dataset containing 134,590 booking records.

| Metric | Result |
|---|---:|
| Total input records | 134,590 |
| Cleaned records | 134,578 |
| Rejected records | 12 |
| Invalid record percentage | 0.01% |
| Unaccounted records | 0 |
| Overlapping booking IDs | 0 |

The record reconciliation check passed successfully.

These results represent one execution against the project dataset.






