Steps to reproduce. 

1. in GCP start VM instance de-project. 

copy external IP and paste it into config file.

connect to VM via ssh: 

in bash: 
```
ssh -i ~/.ssh/proj-vm viktorija@34.38.125.214
```
will connect to de-project.

2. Google Cloud SDK Authentication (if not configured automatically).

in bash: under viktorija@de-project:~$ 
```
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/prices.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```
output: Activated service account credentials for: [terraform-runner@airbnb-prices-eu.iam.gserviceaccount.com]

3. using terraform, create new bucket and dataset.  

in bash: in DE-project/terraform:
```
terraform init
terraform plan
terraform apply
```
in gcp will be created new bucket 'airbnb-prices-eu-bucket' and new dataset 'airbnb_prices_eu_dataset'. 

4. run Kestra (using docker-compose). 

in bash in DE-project/kestra:
```
docker-compose up -d
```
will run 2 containers (kestra and kestra-metadata) and 1 network. 
in google go to localhost:8080 - will open Kestra UI. 

5. upload data from "https://insideairbnb.com/get-the-data/" into gcs bucket. 

in kestra create new flow 'upload_data_to_gcs' and paste there code from DE-project/kestra/upload_data_to_gcs.yaml. 
Execute flow. In result csv files will be uploaded into gcs bucket in appropriate folders. 

6. 


To run PySpark:
in bash in /code:
```
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH"
```





