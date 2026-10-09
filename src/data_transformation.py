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