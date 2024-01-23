import pandas as pd
from datetime import datetime, timedelta

# Given string value
date_string = '2021-01-01 10:30:00'

# Convert string to datetime format
date_format = '%Y-%m-%d %H:%M:%S'
start_date = datetime.strptime(date_string, date_format)

print("Converted string to datetime:", start_date)

# Create a list of 10 values with 1-minute time gap
date_values = [start_date + timedelta(minutes=i) for i in range(10)]

print("List of datetime values with 1-minute gap:", date_values)

# Create a DataFrame with the date field
df = pd.DataFrame({'date': date_values})

print("DataFrame with 'date' field:")
print(df['date'])

# Format the date field as desired
df['formatted_date'] = df['date'].dt.strftime('%y%m%d %H:%M:%S.%f')

print("DataFrame with 'formatted_date' field:")
print(df)
