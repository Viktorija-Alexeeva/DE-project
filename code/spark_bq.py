#!/usr/bin/env python
# coding: utf-8

import argparse
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import md5, concat_ws
from pyspark.sql import types


parser = argparse.ArgumentParser()

parser.add_argument('--country', required=True)
parser.add_argument('--input_base_path', required=True)
parser.add_argument('--output_base_path', required=True)

args = parser.parse_args()

country = args.country
input_base_path = args.input_base_path
output_base_path = args.output_base_path

spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

spark.conf.set('temporaryGcsBucket', 'dataproc-temp-europe-west1-95215738418-sjnvgog3')

# Define schemas column types
df_schema = types.StructType([
    types.StructField("id", types.IntegerType(), True),
    types.StructField("name", types.StringType(), True),
    types.StructField("host_id", types.IntegerType(), True),
    types.StructField("host_name", types.StringType(), True),
    types.StructField("neighbourhood_group", types.StringType(), True),
    types.StructField("neighbourhood", types.StringType(), True),
    types.StructField("latitude", types.StringType(), True),
    types.StructField("longitude", types.StringType(), True),
    types.StructField("room_type", types.StringType(), True),
    types.StructField("price", types.DoubleType(), True),
    types.StructField("minimum_nights", types.IntegerType(), True),
    types.StructField("number_of_reviews", types.IntegerType(), True),
    types.StructField("last_review",types.DateType(), True),  
    types.StructField("reviews_per_month", types.DoubleType(), True),
    types.StructField("calculated_host_listings_count", types.IntegerType(), True),
    types.StructField("availability_365", types.IntegerType(), True),
    types.StructField("number_of_reviews_ltm", types.IntegerType(), True),
    types.StructField("license", types.StringType(), True),
    types.StructField("country", types.StringType(), True),
    types.StructField("region", types.StringType(), True),
    types.StructField("city", types.StringType(), True),
    types.StructField("release_date", types.DateType(), True) 
])


input_path = f"{input_base_path}/{country}/"
output_source_table = f"{output_base_path}.{country}_listings_temp"
output_target_table = f"{output_base_path}.{country}_listings"


# Read csv, add unique_row_id and write into temp table
df_source = spark.read \
    .option("header", "true") \
    .schema(df_schema) \
    .csv(input_path)

df_source = df_source \
    .withColumn("unique_row_id", md5(concat_ws("|", "country", "region", "city", "release_date", "id", "host_id")))

df_source.write \
    .format('bigquery') \
    .option('table', output_source_table) \
    .mode("overwrite") \
    .save()

# Read bq tables
df_source = spark.read \
    .format("bigquery") \
    .option("table", output_source_table) \
    .load()

df_target = spark.read \
    .format("bigquery") \
    .option("table", output_target_table) \
    .load()

# Identify new rows that are not in the target table
df_new_records = df_source.join(df_target, "unique_row_id", "left_anti") 
 
# Append new records to target table
df_new_records.write \
    .format("bigquery") \
    .option("table", output_target_table) \
    .mode("append") \
    .save()

print(f"Successfully merged {output_source_table} into {output_target_table}  table.")
