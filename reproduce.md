Steps to reproduce. 

1. in GCP start VM instance. 
copy external IP and paste it into config file. 
connect to VM via ssh. 
in bash: 
```
ssh -i ~/.ssh/proj viktorija@34.79.46.252
```
will connect to de-project.

2. Google Cloud SDK Authentication
in bash: under viktorija@de-project:~$
```
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/airbnb.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```
output: Activated service account credentials for: [terraform-runner@airbnb-prices-project.iam.gserviceaccount.com]

3. using terraform, create new bucket and dataset.  

in bash in DE-project/terraform:
```
terraform init
terraform plan
terraform apply
```
in gcp will be created new bucket 'airbnb-prices-bucket' and new dataset 'airbnb_prices_dataset'. 

4. download dataset 'airbnb prices' to VM. 
create folder DE-project/dataset. Then download un unzip files. 

in bash in DE-project/dataset:
```
kaggle datasets download -d thedevastator/airbnb-prices-in-european-cities 
unzip airbnb-prices-in-european-cities.zip 
rm airbnb-prices-in-european-cities.zip
```

5. download csv files from VM to GCS raw folder.
in bash:
```
gsutil -m cp -r dataset/ gs://airbnb-prices-bucket/raw
```

6. copy csv files from raw folder to weekends and weekdays folders using pyspark and Dataproc cluster.

To run PySpark:
in bash in /code:
```
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```

Will be using code/upload_csv_to_gcs.py script. 
to copy script to gcs:
in bash in /code:
```
gsutil cp upload_csv_to_gcs.py gs://airbnb-prices-bucket/code/upload_csv_to_gcs.py
```

To submit jobs to Dataproc cluster:
in bash in /code:
```
gcloud dataproc jobs submit pyspark \
    --cluster=de-project-cluster \
    --region=europe-west1 \
    gs://airbnb-prices-bucket/code/upload_csv_to_gcs.py \
    -- \
        --source_directory=gs://airbnb-prices-bucket/raw/ \
        --gcs_bucket=airbnb-prices-bucket
```




