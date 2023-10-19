# Real-time streaming data pipeline with Flink and Kinesis: Build, deploy, and scale a scalable and durable data pipeline

Improving traffic safety is a paramount public concern, but many studies on traffic accident analysis and prediction have been constrained by small-scale datasets, limiting their effectiveness and applicability. Large-scale datasets often lack accessibility, are outdated, or lack essential contextual information like weather and points of interest. To bridge these gaps, we have meticulously gathered, integrated, and enriched data to create the expansive US-Accidents database.

Data Engineering AWS played a vital role in the process. The US-Accidents database encompasses a vast collection of information, including 2.25 million instances of traffic accidents that occurred in the contiguous United States over the past three years. Each accident record is enriched with intrinsic and contextual attributes such as location, time, natural language descriptions, weather conditions, time of day, and points of interest.  

 
## Table of Contents

- [Description](#description)
- [Architecture](#architecture)
- [Dataset](#Dataset)
- [Methodology](#Methodology)
- [Modular Code Overview](#modular-code-overview)
- [Creating an AWS Cloud9 environment](#creating-an-AWS-Cloud9-environment)
- [Setting up the enviroment](#setting-up-the-enviroment)
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

![diagram](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/flink_kinesis.png)

## Dataset

The dataset [US car accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) is available for download either from Kaggle or directly through the terminal. To obtain it, you can use the following command in your terminal:  
```bash
kaggle datasets download -d sobhanmoosavi/us-accidents
```
In order to make this dataset accessible within our AWS environment, it's necessary to copy the downloaded file from your local machine to an S3 bucket. We have a specific S3 bucket named `'us-accidents-raw-us_east_1-dev'` that has been created for this purpose. Additionally, a folder within the bucket named `'raw_us-accidents'` has been set up.

You can use the AWS Command Line Interface (CLI) to upload the file to the S3 bucket with the following command:
```terminal
aws s3 cp <local-file-path> s3://us-accidents-raw-us_east_1-dev/raw_us-accidents/
```
Make sure to replace `<local-file-path>` with the actual path to the downloaded dataset on your local machine. Once the file is copied to the S3 bucket, it will be accessible for further data processing and analysis within our AWS environment.

The dataset encompasses a range of variables, but our primary focus lies on a specific set of variables. These variables are designed to be utilized in real-time to feed our Python-based simulator. This simulator, in turn, will feed data into the Kinesis streaming service, enabling us to conduct real-time processing and analysis. The variables we will concentrate on and subsequently transform using Kinesis Analytics are as follows:
- `severity`
- `Start_Time`
- `End_Time`
- `Location`
- `Description`
- `City`
- `State`

## Methodology 

### Steps in Raw-Layer
1. Create an S3 bucket.
2. Upload the RAW data file to S3.
3. Create a Data Stream named `us-accidents-data-stream-1`.
4. Setup a Cloud9 environment and run the simulation Code:
   - Read the file from S3.
   - Convert each row to JSON.
   - Typecast strings to Datetime objects.
   - Add a Transaction Timestamp (`Txn_Timestamp`).
   - Push each data point to `us-accidents-data-stream-1`.
5. After implementing the Analytical and Real-time Layer, archive the Raw data to S3 as part of the Single Source of Truth (SSOT) process.

![raw_layer](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/raw_layer.png)

### Steps in Analytical Layer
1. Test the Flink application using the provided SQL or Python code.
2. Build and deploy the Flink application in Kinesis Data Analytics (KDA).
3. The Flink Application includes:
   - Create a table in the Glue database and ingest the `'us-accidents-data-stream-1'` data via the Glue Catalog.
   - Apply a watermark on `Txn_Timestamp` with a 5-second interval.
   - Partition the data based on the `'Severity'` field.
   - Create a second table for the Real-time layer by filtering the following fields and pushing them to `'us-accidents-data-stream-2'`:
     * `ID`
     * `Severity`
     * `City`
     * `County`
     * `Txn_Timestamp`

***Create a table to store data from the `'us-accidents-data-stream-1'` kinesis stream into the Glue database***
 ``` sql
DROP TABLE IF EXISTS us_accidents_stream;
CREATE TABLE us_accidents_stream (
    `ID` VARCHAR(50),
    `Severity` bigint,
    `Start_Time` TIMESTAMP(3),
    `End_Time` TIMESTAMP(3),
    -- Other columns ...
    `City` VARCHAR(50),
    `County` VARCHAR(50),
    -- Other columns ...
    `Txn_Timestamp` TIMESTAMP(3),
    WATERMARK FOR Txn_Timestamp as Txn_Timestamp - INTERVAL '5' SECOND
)
PARTITIONED BY (Severity)
WITH (
    'connector' = 'kinesis',
    'stream' = 'us-accidents-data-stream-1',
    'aws.region' = 'eu-west-1',
    'scan.stream.initpos' = 'LATEST',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601'
);
```
***Create a table to store only the selective columns and send it to `'us-accidents-data-stream-2'`***
```sql
DROP TABLE IF EXISTS us_accidents_stream_1_results;
CREATE TABLE us_accidents_stream_1_results (
    `ID` VARCHAR(50),
    `Severity` bigint,
    `City` VARCHAR(50),
    `County` VARCHAR(50),
    `Txn_Timestamp` TIMESTAMP(3)
)
PARTITIONED BY (Severity)
WITH (
    'connector' = 'kinesis',
    'stream' = 'us-accidents-data-stream-2',
    'aws.region' = 'eu-west-1',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601'
);
```
***Send only the selective data from 'us_accidents_stream' table to `'us_accidents_stream_1_results'` table***

```sql
INSERT INTO us_accidents_stream_1_result6
SELECT ID, Severity, City, County, Txn_Timestamp
FROM us_accidents_stream
WHERE Severity > 3;
```
![diagram](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/analytic_layer.png)

### Steps in Real-Time Layer
1. Read the stream in Lambda and deaggregate the records using Kinesis Producer Library (KPL) (loop-in the generator to start receiving records)
   ```terminal
   pip install aws_kinesis_agg
   ```
2. Decode the data in Lambda as the event record data is `base64` encoded
3. Create CloudWatch metrics for `‘Severity’`, `‘City’` and `‘County'`
4. Push the metrics to CloudWatch with a `Severity > 2`
5. Create Grafana Dashboard for visualizing the data points
6. Setup Email Notifications through AWS SNS to manage `severity > 4`
![diagram](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/real-time_layer.png)


## Creating an AWS Cloud9 environment
 
Below are the steps required to set up the environment and run this Data engineering project on cloud9 on aws.
To create an AWS Cloud9 environment, you can follow these steps:

1. Open the AWS Management Console: Go to the AWS Management Console (https://console.aws.amazon.com) and sign in to your AWS account.
2. Navigate to Cloud9: Use the AWS services search bar or navigate to the "Developer Tools" category and select "Cloud9."
3. Click "Create environment": On the Cloud9 dashboard, click the "Create environment" button.
4. Provide environment details:
 - Enter a name for your environment. Optionally, enter a description.
 - Choose the environment type (new or clone an existing environment).
 - Select the instance type based on your requirements.
 - Choose the platform (Amazon Linux 2 or Ubuntu).
5. Configure settings:
 - Choose the network settings (either create a new Amazon VPC or use an existing one).
 - Select the subnet for your environment.
 - Choose the IAM role that Cloud9 will use to access AWS resources on your behalf.
 - Configure additional settings as needed.
6. Review and create:
 - Review the configuration details.
 - Enable the option to create an AWS CloudFormation stack if desired.
 - Click "Create environment" to start the provisioning process.
7. Wait for the environment to be created: The Cloud9 environment creation process may take a few minutes. You can monitor the progress on the Cloud9 dashboard.
8. Access the Cloud9 IDE: Once the environment is created, you can click on its name in the Cloud9 dashboard to access the Cloud9 integrated development environment (IDE) in your web browser.

## Setting up the enviroment

## Cloning GitHub repository to AWS Cloud9 

1. Open your AWS Cloud9 environment: Access the [AWS Management Console](https://console.aws.amazon.com) and go to the Cloud9 service. Select the Cloud9 environment you wish to link with GitHub.
2. Configure Git credentials: In your Cloud9 environment, open a new terminal by clicking on the "Window" menu and selecting "New Terminal." Run the following commands to configure your Git credentials:
   ```bash
   git config --global user.name "Your GitHub Username"
   git config --global user.email "Your GitHub Email"
   ```
3. Generate and add an SSH key: To securely connect Cloud9 with your GitHub account, you need
to generate an SSH key pair and add the public key to your GitHub account. Run the following
command in your Cloud9 terminal:
   ```bash
   ssh-keygen -t rsa -b 4096 -C "Your GitHub Email"
   ```
4. View and copy the public key: Run the following command to display your public key:
   ```terminal
   cat ~/.ssh/id_rsa.pub
   ```
   Copy the entire contents of the public key that is displayed in the terminal.
5. Add the public key to your GitHub account: Go to your [GitHub account settings](https://github.com/settings/profile) and navigate to the "SSH and GPG keys" section. Click on
"New SSH key" and give it a descriptive title. Paste the public key you copied in the previous step
and click "Add SSH key."
6. Test the connection: To test if the SSH connection between Cloud9 and GitHub is successful, run
the following command in the Cloud9 terminal:
   ```terminal
   ssh -T git@github.com
   ```
   You should see a success message indicating that you've successfully authenticated with GitHub.
7. Clone a GitHub repository: In your Cloud9 environment, navigate to the directory where you want to clone the GitHub repository. Run the following command to clone the repository:
   ```bash
   git clone git@github.com:username/repository.git
   ```
   Replace username with your GitHub username and repository with the name of the repository you want to clone.

## Contribution
  1. Focus changes on spec ific improvements.
  2. Follow project's coding style.
  3. Provide detailed descriptions in pull requests.
## Reporting Issues
  Use "Issues" to report bugs or suggest improvements.
# Contact
For questions or contact, my [Mail](diegovillatormx@gmail.com) or [Twitter](https://twitter.com/diegovillatomx). 

