# Real-time streaming data pipeline with Flink and Kinesis: Build, deploy, and scale a scalable and durable data pipeline

Improving traffic safety is a paramount public concern, but many studies on traffic accident analysis and prediction have been constrained by small-scale datasets, limiting their effectiveness and applicability. Large-scale datasets often lack accessibility, are outdated, or lack essential contextual information like weather and points of interest. To bridge these gaps, we have meticulously gathered, integrated, and enriched data to create the expansive US-Accidents database.

Data Engineering AWS played a vital role in the process. The US-Accidents database encompasses a vast collection of information, including 2.25 million instances of traffic accidents that occurred in the contiguous United States over the past three years. Each accident record is enriched with intrinsic and contextual attributes such as location, time, natural language descriptions, weather conditions, time of day, and points of interest.  


 
## Table of Contents

- [Description](#description)
- [Architecture](#architecture)
- [Dataset](#Datset)
- [Methodology](#Methodology)
- [Modular Code Overview](#modular-code-overview)
- [To create an AWS Cloud9 environment](#To-create-an-AWS-Cloud9-environment)
- [Cloning GitHub repository to AWS Cloud9](#Cloning-GitHub-repository-to-AWS-Cloud9)
- [Usage](#usage) 
- [Contribution](#contribution)
- [Contact](#contact)

## Description

The primary objective of this project is to develop an incremental Extract, Transform, Load (ETL) solution using AWS CDK for the analysis of cryptocurrency data. This process involves the construction of a serverless pipeline, in which Lambda functions are employed for data extraction from an API and subsequent streaming into Kinesis streams. Additionally, a standalone Lambda function will be created to consume data from the Kinesis stream, apply essential transformations, and store them in DynamoDB.

To conduct real-time data analytics within the Kinesis streams, we will utilize Apache Flink and Apache Zeppelin. These tools will empower us to extract insights and derive valuable information from the data. AWS serverless technologies, including Amazon Lambda and Amazon Glue, will be leveraged for efficient processing and transformation of data from three distinct data sources.

Furthermore, Amazon Athena, a query service, will be used to analyze the transformed data stored in DynamoDB. This will facilitate efficient querying and data exploration, enabling us to extract meaningful insights and make informed decisions based on cryptocurrency data.

By combining these AWS services and technologies, our aim is to create a robust and scalable solution for cryptocurrency data analysis, enabling comprehensive data processing, transformation, and analysis.

## Architecture

![diagram](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/architecture.png)

## Dataset

This Project uses the [US car accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) dataset which includes a few of the following fields:
- Severity
- Start_Time
- End_Time
- Location
- Description
- City
- State

## Methodology 
