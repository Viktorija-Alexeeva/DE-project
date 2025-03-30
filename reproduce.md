Steps to reproduce the project 'airbnb-prices-eu'. 

1. In GCP start VM instance 'de-project'. 

Copy external IP and paste it into config file.

Connect to VM via ssh: 

In bash: 
```
ssh -i ~/.ssh/proj-vm viktorija@34.38.125.214
```
Will connect to de-project.
Since Google Cloud SDK Authentication is configured, will see output:
```
Activated service account credentials for: [terraform-runner@airbnb-prices-eu.iam.gserviceaccount.com]
```

2. Configure Terraform files to create new bucket and dataset. 

In folder DE-project/terraform create and configure files main.tf and variables.tf.

In variables.tf:
```
project: airbnb-prices-eu
region: europe-west1
dataset: airbnb_prices_eu_dataset
bucket: airbnb-prices-eu-bucket
```

Using Terraform, create new bucket and dataset.  

In bash in DE-project/terraform:
```
terraform init
terraform plan
terraform apply
```
In GCP will be created new bucket 'airbnb-prices-eu-bucket' and new dataset 'airbnb_prices_eu_dataset'. 

3. Use Kestra to upload csv files from "https://insideairbnb.com/get-the-data/" into GCS bucket and BQ table. 

3.1. Run Kestra (using docker-compose). 

In DE-project/kestra create and configure 'docker-compose.yaml' file:
- to configure Kestra and Kestra-metadata containers connection. 
- mount /.gc/prices.json file to configure Kestra access to GCP. 

In VS code add forwarded ports: 5432, 8080 and 8081.

To run Kestra: 

In bash in DE-project/kestra:
```
docker-compose up -d
``` 
Then in google open http://localhost:8080 - will open Kestra UI. 

3.2. Create flow gcp_kv.yaml to pass GCP parameters to Kestra.

After flow execution in Namespaces - de-project - kv store -  will appear 4 keys. 

3.3. Create flow upload_data_to_gcs_and_bq.yaml to upload csv files into GCS bucket and BQ table.

Flow has input section, so user can either select from dropdown list or write any other country manually. 
6 countries are selected for the project: Spain, Portugal, Italy, Greece, France, Germany. 

Flow will have several tasks:
- id: extract_and_add_columns:
    this task will:
    - download 'visualisations/listings.csv' files from "https://insideairbnb.com/get-the-data/".
    - rename csv files as: {country}_{region}_{city}_{release_date}_listings.csv.
    - clean data: remove extra tabs, spaces, quotes. set encoding.
    - filter rows with only expected number of columns.
    - add 4 additional columns: country, region, city, release_date.
    - save modified files.

- id: create_bq_table: will create {country}_listings table (target table, where will be stored all data) in BigQuery. Table is partitioned by release_date and clustered by city for better performance.
- id: upload_to_gcs: will save modified csv files into gcs bucket in appropriate {country} folder.
- id: create_bq_table_ext: will create external table {country}_listings_ext from csv file.
- id: create_bq_table_temp: will create materialized table {country}_listings_temp from {country}_listings_ext table and generate unique_row_id.
- id: merge_bq_table: will insert new rows from {country}_listings_temp table into {country}_listings table. 
- id: drop_bq_tables_ext_temp: will drop _ext and _temp tables after execution. 

The result of flow execution:
- GCS bucket with 6 {country} folders and several csv files in each of them. 
- dataset in BQ with 6 {country}_listings tables and uploaded data. 

Also there are triggers for each country, according to which the flow will run automatically on the 1st day of each month, and, in case new csv file is pubished on site, it will be uploaded to GCS bucket and data will be added into appropriate BQ table. 

4. Create DBT project for data transformation. 

For DBT project will be used existing terraform-runner service account.
For development will be used 'airbnb_prices_eu_dev' dataset, for deployment - 'airbnb_prices_eu_dataset'.

DBT will take data from source tables (airbnb_prices_eu_dataset), transform it, on its basis will create fact table and datamart with prices statistics.  

4.1. Setup account, connection, project details, initialize dbt project. 

In VS code in DE-project create folder dbt-airbnb, where dbt project code will be stored.

In google go to https://www.getdbt.com/. Sign up there. Create dbt cloud account 'dbt-project'. 

After logged in create dbt project. 

Setup database connection:
```
connection name: BigQuery
upload prices.json key 
```

Setup project details (project name with '_'):
```
project name: airbnb_prices_eu
project subdirectory: dbt-airbnb
connection: BigQuery
development credentials: 
    dataset: airbnb_prices_eu_dev
setup repository (Git clone - copy SSH in repo): git@github.com:Viktorija-Alexeeva/DE-project.git
```

Add a link to github account. 
Configure integration in github: github - personal account - settings - applications - dbt cloud - repository access - add repo 'DE-project' - save.  

Initialize dbt-project: Develop - Cloud IDE - click 'initialize-dbt-project' - will be created project inside dbt-airbnb folder. 

Create new branch for commits: 'de-branch'.

Commit - create pull request - merge. 

As a result in github main branch will be stored dbt-project. 

4.2. Configure dbt_project.yml file. 

In Develop - Cloud IDE - file explorer - folder DE-project/dbt-airbnb:

file dbt_project.yml:
```
name: 'airbnb_prices_eu'

models:
  airbnb_prices_eu:
	staging:
      +materialized: view
    core:
      +materialized: table
	  
vars:
  room_type_values: ["Entire home/apt", "Private room", "Hotel room", "Shared room"]
```
These settings will provide:
- models on staging level will be views.
- models on core level will be materialized tables.
- values of room_type column should be from mentioned list. 

In dbt cli: 
```
dbt build
```

4.3. Install packages. 

For the project will be used 2 packages: 
- dbt_utils (to automatically generate ID for the rows, where ID is missing in source)
- codegen (to automatically generate info about dbt models (for schema.yml files))
 
In DE-project/dbt-airbnb create file 'packages.yml':
```
packages:
  - package: dbt-labs/dbt_utils
    version: 1.3.0
  - package: dbt-labs/codegen
    version: 0.13.1
```

In dbt cli:
```
dbt deps
```	 

4.4. Configure staging models. 

In folder DE-project/dbt-airbnb/models create folder 'staging'.

4.4.1. In models/staging create and configure 'schema.yml' file to generate models on staging level.

Here will be added info about sources (files from airbnb_prices_eu_dataset) and models on staging level. 

In dbt DBT_DATABASE = GCP projectID; DBT_SCHEMA = GCP dataset.

In staging/schema.yml:
```
version: 2

sources:
  - name: staging
    database: airbnb-prices-eu
    schema: airbnb_prices_eu_dataset
	
	tables:
      - name: france_listings
```
Save file. 

Click on 'generate model'- dbt will create 'stg_staging__france_listings.sql' file in subfolder 'models/staging/staging'. 
Rename file into 'stg_france_listings.sql' and replace into 'models/staging'. Delete subfolder 'models/staging/staging'.

Now in staging/schema.yml add names and generate models for the rest of source tables (should be 6 sources). Rename and replace files (the same as with france_listings). 
 
In dbt cli: 
```
dbt build
```
 
As a result in BQ airbnb_price_eu_dev will be created 6 stg_ views. 

4.4.2. Do some corrections in stg_.sql files. 

To do in stg_.sql files:
- rename some regions. For ex., in Italy there are 2 csv files from the same region, which spells differently: Lombardia (in italian language) and Lombardy (in english). Will rename it to Lombardy. In Germany and Spain there are regions named in 2 letters, will rename to full region name.  
- filter listing only with prices. 
- add additional bit column 'has_license', which check, whether listing has licence. 
- cast values of columns country, region, city - start from capital letter. 
- add release_year and release_month columns as extract of release_date. 
- generate surrogate key for listing_id, where value is null in source. 
- concat values of latitude and longitude into 1 column.  

4.4.3. In staging/schema.ylm need to add info about models. To generate info automatically will use package codegen.

Go to  https://hub.getdbt.com/dbt-labs/codegen/latest/ , choose 'generate_model_yaml (source)'. 

In new file paste: 
```
{% set models_to_generate = codegen.get_models(directory='staging') %}
{{ codegen.generate_model_yaml(
    model_names = models_to_generate
) }}
```
Click 'Compile'. Copy info into staging/schema.yml. Add some description where necessary. 
 
4.4.4. Add some tests to columns. 

To do in staging/schema.yml:
- add not_null tests to listing_id and price columns. Severity: warn. 
- add accepted_values test for room_type column: var room_type_values. Severity: warn.
	

4.5. Configure core models. 

In folder DE-project/dbt-airbnb/models create folder 'core'.

4.5.1. In models/core create file fct_listings.sql.

This is fact table, which unions data from all stg_ files (from staging models). 

4.5.2. In models/core create file dm_prices_statistics.sql. 

This is datamart with special info about prices. 

In datamart are created columns price_level_country and price_level_city. 
They will define price level according to price distribution for partition room_type and country/city.  
For that will be used function PERCENTILE_CONT for 30%, 75%, 95%.
There are 4 possible values for price levels: low cost, middle cost, high cost, luxury. 
low cost <= 30%; middle cost > 30% and <= 75%; high cost > 75% and <= 95%; luxury > 95%.

4.5.3. In models/core create schema.yml file. 

Use codegen to generate info about models in core. Add some description where necessary. 

4.6. Create documentation. 

In dbt cli:
```
dbt docs generate
```
Then click on button right to the name of branch to check the generated documentation for the project. 
It will open tab 'dbt Docs' (https://kl743.us1.dbt.com/accounts/70471823449159/develop/70471823694887/docs/index.html#!/overview).

4.7. Configure deployment evnironment, schedule monthly job, configure CI job. 

4.7.1. Setup deployment environment. 

To setup deployment environment in dbt click on deploy - environments - create environment. 
```
environment name: Production
Set deployment type: PROD
connection: BigQuery
dataset: airbnb_prices_eu_dataset
```
Save. 

4.7.2. Create and schedule monthly job.

Since we know that our source reports are published quaterly, it is enough to run a job once a month. 

Before run a job always: 
- commit changes into git
- create PR
- merge with main branch

To configure a job: deploy - jobs - click on 'create job' - deploy job. 
```
job name: Monthly
Environment: Production
run source freshness: no
commands: dbt build
generate docs on run: yes
run on schedule: yes
timing: cron schedule
custom cron schedule: 0 0 2 * *
job completion: no
```
Trigger will run a job every 2nd day of each month. 

After job is created, click 'run now' to test a job. 

As a result in BQ airbnb_proces_eu_dataset will be created 6 stg_ views and 2 tables from core models: fct_listings and dm_prices_statistics.

Add artifacts: in dbt main page click on dashboard - settings - on the right will see project settings, go to artifacts - documentation: 'monthly' job - save. 

4.7.3. Create CI job.

To configure continuous integration create another job.

Deploy - jobs - click on 'create job' - continuous integration job. 
```
job name: CI checks
description: avoid breaking production
triggered by PR: yes
commands: dbt build --select state:modified+
```

This job is triggered by PR. When create PR in git, it will automatically run CI checks job. When check is finished, will see 'dbt Cloud — dbt Cloud run success', only after that can merge PR. 

5. Create dashboard in Looker Studio to visualise data from datamart. 

5.1. Create dashboard in Looker Studio. 

To create a dashboard in Look studio go to https://lookerstudio.google.com/u/1/navigation/reporting.

Create connection: click create - data source - BigQuery - project 'airbnb-prices-eu' - dataset 'airbnb_prices_eu_dataset' - table 'dm_prices_statistics' - connect.

In 'default aggregation' change 'sum' to 'none' for all columns. 
In 'type' change:
- 'text' to 'geo'- 'Latitude, Longitude' for column 'latitude_longitude'.
- 'text' to 'geo' - 'country' for column 'country'.
- 'text' to 'geo' - 'city' for column 'city'.
- 'text' to 'geo' - 'country subdivision 1st level' for column 'region'.
- 'number' to 'currency EUR' for column 'price'.  

Click 'Create report'. 

5.2. Create tiles. 

All settings are on screenshots in folder DE-project/looker. 

Create a dashboard with 4 tiles:
- Listings map (on basis of latitude_longitude). The more listings are on area, the bigger size of bubbles. Each room type has different bubble color. 
- Prices by city. Values of prices are shown according to applied filters. 
- Price level in city (on basis of price_level_city). Shows how data is distributed among different price levels.  
- Number of listings by room type. Shows actual number of listings for each room type. 

5.3. Create filters. 

All settings are on screenshots in folder DE-project/looker. 

Add 4 dropdown filters: 
- Release year
- Country
- Region
- City

5.4. Check how tiles works. 

All tiles have cross-filtering interaction, so when user implements filter on 1 tile, it is applied for all tiles. 
Compare screenshots 'Prices statistics' (without any filters) with 'Spain, low cost' and 'Spain, Portugal, private room'. 
Should see the changes in charts.


Reproduction is finished. 

