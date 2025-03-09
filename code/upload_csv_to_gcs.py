from pyspark.sql import SparkSession
from google.cloud import storage
import argparse

def organize_files_in_gcs(raw_directory, gcs_bucket):
    """
    Organize CSV files from a raw folder in GCS to weekends and weekdays folders in GCS using PySpark.
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

        # Determine the destination path based on the file name
        if filename.endswith('_weekends.csv'):
            destination_path = f"gs://{gcs_bucket}/csv/weekends/{filename}"
        elif filename.endswith('_weekdays.csv'):
            destination_path = f"gs://{gcs_bucket}/csv/weekdays/{filename}"
        else:
            continue  # Skip irrelevant files

        # Read CSV from GCS using Spark
        gcs_file_path = f"gs://{bucket_name}/{blob.name}"
        df = spark.read.option("header", "true").csv(gcs_file_path)

        # Write the CSV file to the appropriate GCS folder
        df.write.mode("overwrite").option("header", "true").csv(destination_path)

        print(f"Moved {filename} to {destination_path}")

    # Stop the Spark session
    spark.stop()

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Organize CSV files in GCS using PySpark.")
    parser.add_argument("--source_directory", type=str, required=True, help="GCS path to the raw dataset folder.")
    parser.add_argument("--gcs_bucket", type=str, required=True, help="Target GCS bucket name.")

    args = parser.parse_args()

    # Organize files in GCS
    organize_files_in_gcs(args.source_directory, args.gcs_bucket)
