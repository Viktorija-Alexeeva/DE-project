from pyspark.sql import SparkSession
from pyspark.sql.functions import lit  # Import 'lit' to create literal columns
from google.cloud import storage
import argparse

def organize_files_in_gcs(raw_directory, gcs_bucket):
    """
    Organize CSV files from a raw folder in GCS to weekends and weekdays folders in GCS using PySpark.
    Additionally, add a 'city' column to each CSV file based on the file name (city_weekends.csv or city_weekdays.csv).
    """
    # Initialize PySpark session
    spark = SparkSession.builder.appName("OrganizeCSVFilesInGCS").getOrCreate()

    # Initialize GCS client
    client = storage.Client()
    bucket_name = raw_directory.split('/')[2]  # Extract bucket name from GCS path
    prefix = '/'.join(raw_directory.split('/')[3:])  # Extract folder prefix from GCS path
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)

    # Process each CSV file in the raw folder
    for blob in blobs:
        filename = blob.name.split('/')[-1]  # Extract the file name
        if not filename.endswith('.csv'):
            continue  # Skip non-CSV files

        # Determine the destination path based on the file name and set folder accordingly
        destination_folder = None
        if filename.endswith('_weekends.csv'):
            destination_folder = "csv/weekends"
        elif filename.endswith('_weekdays.csv'):
            destination_folder = "csv/weekdays"
        else:
            continue  # Skip irrelevant files if the naming doesn't match

        destination_path = f"gs://{gcs_bucket}/{destination_folder}/{filename}"

        # Determine the city by splitting the file name (assumes file name in format: city_weekends.csv or city_weekdays.csv)
        city = filename.split('_')[0]

        # Read CSV from GCS using Spark
        gcs_file_path = f"gs://{bucket_name}/{blob.name}"
        df = spark.read.option("header", "true").csv(gcs_file_path)

        # Add the new 'city' column with the extracted city name
        df = df.withColumn("city", lit(city))

        # Write the CSV file to the appropriate GCS folder with the new column added
        df.write.mode("overwrite").option("header", "true").csv(destination_path)

        print(f"Moved {filename} to {destination_path} with city column added: {city}")

    # Stop the Spark session
    spark.stop()

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Organize CSV files in GCS using PySpark and add a 'city' column.")
    parser.add_argument("--source_directory", type=str, required=True, help="GCS path to the raw dataset folder.")
    parser.add_argument("--gcs_bucket", type=str, required=True, help="Target GCS bucket name.")

    args = parser.parse_args()

    # Organize files in GCS
    organize_files_in_gcs(args.source_directory, args.gcs_bucket)
