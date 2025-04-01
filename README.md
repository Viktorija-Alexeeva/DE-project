# DE-project 'Airbnb prices EU'
The Final project was developed as part of Data Engineering Zoomcamp. 

This project is based on data from Inside Airbnb platform, which provides detailed datasets about Airbnb listings, including information on hosts, reviews, pricing, availability, and more. These datasets are valuable for analyzing trends in the short-term rental market, understanding host behavior, and evaluating the impact of Airbnb on housing markets. The datasets are updated quarterly. 

Source link: [Inside Airbnb](https://insideairbnb.com/get-the-data.) 

By developing an automated data pipeline and an interactive dashboard, project aims to solve such problems as:
- Identifying high-density Airbnb areas to analyze market concentration and competition. 
- Understanding pricing variations across different cities and regions.
- Evaluating market positioning by determining whether listings skew toward luxury, budget-friendly, or mid-range accommodations.
- Analyzing room type distribution to help hosts and policymakers make data-driven decisions on supply and demand dynamics.

Technoligies, used in project:
- Cloud: GCP
- Infrastructure as Code (IaC): Terraform
- Workflow Orchestration: Kestra + Docker
- Data Lake: Google Cloud Storage
- Data Warehousing: BigQuery
- Data Transformation: DBT
- Data Visualisation: Looker Studio

Project Data Flow:
![Data Flow](<Data flow.png>)

Data Flow explanation: 
1. Kestra, using Python script, extracts CSV files from Https source and uploads them into GCS bucket.
2. Kestra reads CSV files from bucket and uploads data into BigQuery table. 
3. DBT reads data from BigQuery table, transforms it and inserts into Data Mart (in BigQuery). 
4. Looker Studio visualizes data from Data Mart. 

Moreover, I have implemented a Continuous Integration job in DBT project, that triggers on every pull request in Git. This ensures that all transformations are validated before merging into main brach, maintaining data quality and consistency in the pipeline.

Since the source datasets are updated quarterly, there is no need to trigger the pipelines daily.
Kestra triggers Data Flow on the 1st day of each month, DBT runs on the 2nd day of each month. 
As a result, dashboard data is refreshed once a month. 

Example of dashboard: 
![dashboard](<looker/Prices statistics.png>)


If you are interested in reproducing this project, please follow the instructions below:

1. To configure environment for the project follow instructions in setup_environment.md file.

2. To reproduce the project follow instructions in reproduce.md file. 
















