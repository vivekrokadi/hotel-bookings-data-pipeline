import pandas as pd

date_columns = ['check_in_date', 'checkout_date', 'booking_date']

def transform_dates(df):
   
   for column in date_columns:
      df[column]= pd.to_datetime(df[column], format="mixed", dayfirst=True, errors="coerce")
      
   return df

def count_invalid_dates(df):

   invalid_count = {}
   
   for column in date_columns:
      invalid_count[column] = df[column].isna().sum()
      
   return invalid_count


def create_booking_metrics(df):
   df['lead_time_days'] = (df['check_in_date'] - df['booking_date']).dt.days
   df['no_of_days_stayed']= (df['checkout_date'] - df['check_in_date']).dt.days
   return df
