def validate_bookings(df):
    invalid_records = df[(df['no_guests'] <= 0) | (df['no_guests'].isna()) | (df['revenue_generated'] <= 0)]

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
