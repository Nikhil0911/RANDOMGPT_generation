import boto3
import io
import zipfile
import pandas as pd

# Initialize the S3 client
s3 = boto3.client('s3', region_name='us-west-2')  # Replace with your region

# Define the S3 bucket and file key
bucket_name = 'your-bucket-name'
zip_file_key = 'path/to/yourfile.zip'

# Stream the ZIP file from S3
zip_obj = s3.get_object(Bucket=bucket_name, Key=zip_file_key)
buffer = io.BytesIO(zip_obj['Body'].read())

# Extract the CSV file from the ZIP file
with zipfile.ZipFile(buffer, 'r') as zip_ref:
    # Assuming there's only one CSV file in the ZIP, otherwise specify the filename
    for file_name in zip_ref.namelist():
        if file_name.endswith('.csv'):
            with zip_ref.open(file_name) as csv_file:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(csv_file)
                break

# Display the contents of the DataFrame
print(df)
