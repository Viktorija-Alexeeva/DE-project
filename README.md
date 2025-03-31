# DE-project
Final project was developed as part of the Data Engineering Zoomcamp. 

This project is based on data from Inside Airbnb platform, which provides detailed datasets about Airbnb listings, including information on hosts, reviews, pricing, availability, and more. These datasets are valuable for analyzing trends in the short-term rental market, understanding host behavior, and evaluating the impact of Airbnb on housing markets. The datasets are updated quarterly. 

Source link: https://insideairbnb.com/get-the-data. 

By developing automated data pipeline and interactive dashboard, project can help to solve such problems as:
- Identifying high-density Airbnb areas to analyze market concentration and competition. 
- Understanding pricing variations across different cities and regions.
- Avaluating market positioning by determining whether listings skew toward luxury, budget-friendly, or mid-range accommodations.
- Analyzing room type distribution to help hosts and policymakers make data-driven decisions on supply and demand dynamics.

Technoligies, used in project:
- Cloud: GCP
- Infrastructure as code (IaC): Terraform
- Workflow orchestration: Kestra 
- Data lake: Google Cloud Storage
- Data warehousing: BigQuery
- Data transformation: DBT
- Data visualisation: Looker Studio

Project Data flow:
![Data Flow](<Data flow.png>)





If you are interested in reproducing this project, please check instructions below:

1. To configure environment for the project follow instructions in setup_environment.md file.

2. To reproduce the project follow instructions in reproduce.md file. 
















