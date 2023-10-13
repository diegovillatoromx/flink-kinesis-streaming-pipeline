# Real-time streaming data pipeline with Flink and Kinesis: Build, deploy, and scale a scalable and durable data pipeline

Cryptocurrency, represented by digital or virtual currencies utilizing cryptographic techniques for secure transactions and asset verification, operates on decentralized blockchain technology. Bitcoin, introduced in 2009 as the pioneering decentralized cryptocurrency and the largest by market capitalization, paved the way for numerous alternative cryptocurrencies or "altcoins."

In the domain of Data Engineering within AWS, cryptocurrency data analytics involves systematic examination and interpretation of cryptocurrency and market data. This plays a pivotal role in understanding market trends, making informed decisions, and discovering opportunities within the cryptocurrency landscape. Key aspects encompass *market data analysis*, *blockchain analysis*, *sentiment analysis*, *trading strategies*, *predictive modeling*, and *risk assessment*. Employing data analytics in AWS enables data-driven decision-making, facilitating effective navigation of the dynamic cryptocurrency domain and risk management.  
 
 
## Table of Contents

- [Description](#description)
- [Architecture](#architecture)
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
<img src='https://github.com/diegovillatoromx/Incremental_ETL_Pipeline/blob/main/images/etl-alpha.gif' alt="incremental_etl_alpha_api">

### Methodology 
First and foremost, we'll underscore the importance of avoiding the use of the root user for enhanced cloud security. Simultaneously, we'll initiate the creation of a new user responsible for establishing the entire architecture. In addition, we'll craft new roles, including those tailored for Lambda and AWS Glue, each meticulously configured with their requisite permissions.
<img src='https://github.com/diegovillatoromx/Incremental_ETL_Pipeline/blob/main/images/iam_user.gif' alt="iam_user.gif">

Next, a Python script that fetches cryptocurrency exchange rate data from the Alpha Vantage API
and stores it in an AWS Kinesis data stream.

<img src='https://github.com/diegovillatoromx/Incremental_ETL_Pipeline/blob/main/images/data_production.gif' alt="lambda.gif">

Then, a Python script that defines an AWS Lambda function for processing records from a Kinesis data stream and storing the transformed data in an Amazon DynamoDB table.
<img src='https://github.com/diegovillatoromx/Incremental_ETL_Pipeline/blob/main/images/data_consumer.gif' alt="lambda.gif">

