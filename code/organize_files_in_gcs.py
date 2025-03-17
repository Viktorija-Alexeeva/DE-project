import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from google.cloud import storage
import os

def list_files_in_gcs(bucket_name, folder):
    """List all files in a specific GCS folder"""
    client = storage.Client()
    blobs = client.list_blobs(bucket_name, prefix=folder)
    return [blob.name for blob in blobs]

def organize_files(input_path, output_path, bucket_name):
    # Initialize Spark session
    spark = SparkSession.builder \
        .master("spark://de-project.europe-west1-b.c.airbnb-prices-eu.internal:7077") \
        .appName("OrganizeCSVFiles") \
        .getOrCreate()

    # List all files in the folder specified by input_path (this is passed as 'folder')
    files = list_files_in_gcs(bucket_name, input_path)  # input_path is passed to 'folder'
    
    for file in files:
        if file.endswith(".csv"):
            # Extract city and day type from the filename
            base_filename = os.path.basename(file)  # Get just the file name (without path)
            city, day_type = base_filename.split('_')[:2]  # Extract city and day type
            day_type = day_type.split('.')[0]  # Remove '.csv' to get weekends/weekdays

            # Read the CSV file from GCS
            df = spark.read.option("header", "true").csv(f"{input_path}/{file}")

            # Add 'city' column to the DataFrame
            df = df.withColumn("city", lit(city))

            # Define the output folder (weekends or weekdays)
            output_folder = f"{output_path}/{day_type}"

            # Write the DataFrame back to GCS (overwrite mode to avoid appending)
            df.write.option("header", "true").mode("overwrite").csv(f"{output_folder}/{city}_{day_type}")
    
    spark.stop()

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Process CSV files from GCS")
    parser.add_argument("--input_path", required=True, help="Path to the raw folder in GCS")
    parser.add_argument("--output_path", required=True, help="Path to the processed folder in GCS")
    parser.add_argument("--bucket_name", required=True, help="Name of the GCS bucket")
    
    args = parser.parse_args()

    # Call the process_files function, passing the arguments to process the files
    organize_files(args.input_path, args.output_path, args.bucket_name)

if __name__ == "__main__":
    main()
