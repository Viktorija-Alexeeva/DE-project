Steps to reproduce. 

1. in GCP start VM instance. 
copy external IP and paste it into config file. 
connect to VM via ssh. 
in bash: 
```
ssh -i ~/.ssh/proj-vm viktorija@34.38.125.214
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
in gcp will be created new bucket 'airbnb-prices-eu-bucket' and new dataset 'airbnb_prices_eu_dataset'. 

7. run Kestra (using docker-compose). 
in bash in /kestra:
```
docker-compose up -d
```
it will run 2 containers (kestra-metadata and kestra) and 1 network. 
in google go to localhost:8080 - will open Kestra UI. 

4. download dataset 'airbnb prices' to VM. 
download un unzip files. remove zip file from folder.

in bash in DE-project/dataset:
```
kaggle datasets download -d thedevastator/airbnb-prices-in-european-cities 
unzip airbnb-prices-in-european-cities.zip 
rm airbnb-prices-in-european-cities.zip
```

5. download csv files from VM to GCS raw folder.
in bash 
```
gsutil -m cp -r dataset/* gs://airbnb-prices-eu-bucket/raw
```

6.  rearrange csv files in gcs bucket (from raw/ into csv/ folder) + add column 'city' using pyspark and Dataproc cluster.

To run PySpark:
in bash in /code:
```
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```

Will be using code/organize_files_in_gcs.py script. 
to copy script to gcs:
in bash in /code:
```
gsutil cp organize_files_in_gcs.py gs://airbnb-prices-bucket/code/organize_files_in_gcs.py
```






export KAGGLE_CONFIG_DIR=~/.kaggle
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/airbnb.json
