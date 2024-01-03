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
- [Adding Policies to the Associated EC2 Instance](#Adding-Policies-to-the-Associated-EC2-Instance)
- [Setting up the enviroment](#setting-up-the-enviroment)
- [Cloning GitHub repository to AWS Cloud9](#Cloning-GitHub-repository-to-AWS-Cloud9)
- [Contribution](#contribution)
- [Contact](#contact)

## Description

The primary objective of this project is to develop an Extract, Transform, Load (ETL) solution using AWS for the analysis of traffic accident analysis and prediction data. This process involves the construction of a serverless pipeline, in which Lambda functions are employed for data extraction from an app simulation and subsequent streaming into Kinesis streams. Additionally, a standalone Lambda function will be created to consume data from the Kinesis stream, apply essential transformations, and store them in s3.

To conduct real-time data analytics within the Kinesis streams, we will utilize Apache Flink and Apache Zeppelin. These tools will empower us to extract insights and derive valuable information from the data. AWS serverless technologies, including Amazon Lambda and Amazon Glue, will be leveraged for efficient processing and transformation of data from three distinct data sources.

Furthermore, Amazon Athena, a query service, will be used to analyze the transformed data stored in S3. This will facilitate efficient querying and data exploration, enabling us to extract meaningful insights and make informed decisions based on traffic accident analysis and prediction data.


## Architecture

![diagram](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/flink_kinesis.png)

## Dataset

The dataset [US car accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) is available for download either from Kaggle or directly through the terminal. To obtain it, you can use the following command in your terminal:  
```bash
kaggle datasets download -d sobhanmoosavi/us-accidents
```
In order to make this dataset accessible within our AWS environment, it's necessary to copy the downloaded file from your local machine to an S3 bucket. We have a specific S3 bucket named `'us-accidents-dataset-useast1-dev'` that has been created for this purpose. Additionally, a folder within the bucket named `'raw_us_accidents_dataset'` has been set up.

You can use the AWS Command Line Interface (CLI) to upload the file to the S3 bucket with the following command:
```terminal
aws s3 cp <local-file-path> s3://us-accidents-dataset-useast1-dev/raw_us_accidents_dataset/
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

![raw_layer](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/raw_layer.png)
1. Creating an S3 bucket with the dataset
   ```
   📂 us-accidents-dataset-useast1-dev
      |_📂 raw_us_accidents_dataset
         |_📜 us_accidents_dataset.csv
   ```
2. Upload the RAW data file to S3.
   ```terminal
   aws s3 cp <local-file-path> s3://us-accidents-dataset-useast1-dev/raw_us_accidents_dataset/
   ```
   Make sure to replace `<local-file-path>` with the actual path to the downloaded dataset on your local machine. Once the file is copied to the S3 bucket, it will be accessible for further data processing and analysis within our AWS environment.

3. To create a Data Stream named `us-accidents-data-stream-1` do the following:
   - Inside the AWS Console, click on the "Kinesis" tab.
   - Create the Data Stream:
     - Name: `us-accidents-data-stream-1`
     - Capacity Mode: `On-demand`
     - Data Retention Period: `1 day`

5. Setup a Cloud9 environment and run [the simulation Code](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/Coding/app-simulation.py):
   
   - Read the file from S3.
   - Convert each row to JSON.
   - Typecast strings to Datetime objects.
   - Add a Transaction Timestamp (`Txn_Timestamp`).
   - Push each data point to `us-accidents-data-stream-1`.
6. After implementing the Analytical and Real-time Layer, archive the Raw data to S3 as part of the [Single Source Of Truth](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/Coding/app-simulation.py) (SSOT) process.


### Steps in Analytical Layer
![diagram](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/analytic_layer.png)

#### Amazon Kinesis Data Stream Configuration
As part of our real-time data processing architecture, we have established an Amazon Kinesis Data Stream named `'us-accidents-data-stream-2'`. This data stream is designed to store and manage real-time transformed data originating from our data analytics application within Amazon Kinesis Analytics.
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/data-streams-2.png))

##### Configuration Details:

- **Name:** us-accidents-data-stream-2
- **Capacity Mode:** On-demand
- **Data Retention Period:** 1 day

These settings allow us to efficiently maintain the data flow and manage processing capacity according to our requirements. The 1-day data retention period ensures that data remains available for analysis over a defined timeframe.

This data stream plays a pivotal role in our architecture, enabling us to store and process real-time transformed data. It facilitates live analysis and provides valuable insights to make informed decisions within our business environment.

You can use this text to document the setup of the 'us-accidents-data-stream-2' data stream in your project as an AWS data engineer. Feel free to customize it to meet your specific needs.

#### Creating an Amazon S3 Bucket to Store Transformed Data
A key component of our data processing architecture is the Amazon S3 bucket named 'us-accidents-raw-useast1-dev.' This bucket will be configured to serve as a repository for storing real-time transformed data tables generated by AWS Glue. Here are the steps to create this bucket:
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/raw-bucket.png))

##### Create a New Bucket
- Click on the `"Create bucket"` button to initiate the creation process.
- Set the bucket name as `'us-accidents-raw-useast1-dev'`, a descriptive name related to the project.
- Choose the AWS region where you want to store the data.

#### Creating a Database in AWS Glue

As part of our data processing architecture, we have configured a database in AWS Glue with the name `'db_streaming_datapipeline'`. This database will be used to manage and organize tables generated by our real-time data processing pipeline. Here are the steps to create this database:
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/aws-glue.png))

##### Create a New Database
- In the databases section of AWS Glue, click "Add database" to initiate the creation process.
- Define the name of the database as `'db_streaming_datapipeline'`, which is descriptive and related to the project.


#### Creating an Amazon Kinesis Analytics Job for Data Transformation

As part of our real-time data processing architecture, we are setting up an Amazon Kinesis Analytics job to transform data from the first Kinesis data stream (`'us-accidents-data-stream-1'`) to the second Kinesis data stream (`'us-accidents-data-stream-2'`). This job will play a crucial role in processing and enriching data on-the-fly. Here are the steps to create this Kinesis Analytics job:

##### Create an Studio Notebook
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/1studio_notebook.png)
##### To give a name
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/2name.png)
##### Then, to create a database on glue
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/3databaseglue.png)
##### To include sources with IAM polices
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/4sources.png)
###### To choose kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/4.1sources.png)
###### To save changes
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/4.2sources.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/5destinatios.png)
###### To browse kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/5.1sources.png)
###### To choose kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/5.2sources.png)
##### To browse destinations on s3 bucket
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/6bucket.png)
###### To choose s3 bucket destination
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/6.1bucket.png)
##### To choose the role associated to analytics kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/7roles.png)
###### To attach policies to the role
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/7.1roles.png)
###### To check policies to the role
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_analytics/7.2.png)


#### Test the Flink application using the provided [SQL code](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/Coding/us-accidents-datapipeline_2JFAG2QSD.zpln). 
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
    'aws.region' = 'us-east-1',
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
    'aws.region' = 'us-east-1',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601'
);
```
***Send only the selective data from 'us_accidents_stream' table to `'us_accidents_stream_1_results'` table***

```sql
INSERT INTO us_accidents_stream_1_result
SELECT ID, Severity, City, County, Txn_Timestamp
FROM us_accidents_stream
WHERE Severity > 3;
```

#### Build and deploy the Flink application in Kinesis Data Analytics (KDA).
Apache Flink is a robust stream processing framework that enables the development of real-time data processing applications. This guide outlines the steps to create an Apache Flink application.

##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/1KDA.png)
###### To browse kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/1.1KDA.png)
###### To browse kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/1.2KDA.png)
###### To browse kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/1.3KDA.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/2KDAdeploy.png)
###### To browse kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/2.1KDAdeploy.png)
###### To browse kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/2.2KDAdeployrole.png)
###### To browse kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/2.3KDAdeploycreate.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/3KDArole.png)
###### To browse kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/3.1KDAattach.png)
###### To browse kinesis data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/3.2KDAattachpolicies.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/4KDArun.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/5KDAflink.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/6stream2.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/7monitoring.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/8database.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/9tables.png)
##### To include destinations with IAM policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/KDA_images/10tableproperties.png)


### Steps in Real-Time Layer
The next step in our real-time architecture involves creating a Lambda function responsible for processing information and forwarding it to CloudWatch while generating notifications through SNS to our email address. It is worth noting that within the Lambda function, data must be decoded as the event record data is base64 encoded.
![diagram](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images/real-time_layer.png)

1. Read the stream in Lambda and deaggregate the records using Kinesis Producer Library (KPL) (loop-in the generator to start receiving records)
   ```terminal
   pip install aws_kinesis_agg -t .
   ```
2. The command `"zip -r ../lambda_function.zip"` is used to compress (zip) a directory or file into a ZIP file named `"lambda_function.zip."`
   ```terminal
   zip -r ../lambda_function.py
   ```
4. This command is used to copy the `'lambda_function.zip'` file to the specified path in your S3 bucket.
   ```terminal
   aws s3 cp lambda_function.zip s3://nombre-de-tu-bucket/carpeta/
   ```
5. Create CloudWatch metrics for `‘Severity’`, `‘City’` and `‘County'`
6. Push the metrics to CloudWatch with a `Severity > 2`
7. Create Grafana Dashboard for visualizing the data points
8. Setup Email Notifications through AWS SNS to manage `severity > 4`

##### To create a lambda function 
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/1lambdafunction.png)
###### To add trigger data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/1.1lambdafunction.png)
###### To add the source of trigger data-stream kinesis
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/1.2lambdafunction.png)
###### To modify the policies of IAMRole of lambda
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/1.3lambdafunction.png)
###### To attach policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/1.4lambdafunction.png)
###### The permission policies
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/1.5lambdafunction.png)
###### The enviroment variables
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/1.6lambdafunction.png)
###### To configure the test event
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/1.7lambdafunction.png)
###### To decode the data in Lambda as the event record data is `base64` encoded
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/1.7lambdafunction.png)


##### To create sns notification
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/2sns.png)
###### To details to sns 
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/2.1sns.png)
###### To add subscription to sns 
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/2.2sns.png)
###### To create subscription to sns 
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/2.1sns.png)
##### To create sns notification
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/2sns.png)
###### To details to sns 
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/2.1sns.png)
##### To add the last enviroment variables
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/3lambdafunction.png)
###### To add the arn created on sns to lambda function
![image](https://github.com/diegovillatoromx/flink-kinesis-streaming-pipeline/blob/main/images_real_time/3.1lambdafunction.png)

## Modular Code Overview
This project is organized into modules and includes various code files and scripts to support its functionality. 

```
  📂 crypto_incremental_pipeline
    |_📂 kinesis_stream
    |  |_📜 kinesis_stream_stack.py
    |_📂 data_producer
    |  |_📜 data_producer_stack.py
    |_📂 lambda
    |  |_📜 data_consumer_lambda.py
    |_📂 s3_bucket
    |  |_📜 s3_bucket_stack.py
    |_📂 scripts
    |  |_📜 CryptoHourlyETLJob.py
    |  |_📜 flink_script.sql
    |_📂 tests
    |  |_📜 __init__.py
    |  |_📂 unit
    |    |_📜 __init__.py
    |    |_📜 test_crypto_incremental_pipeline_stack.py
    | 📜 app.py
    | 📜 cdk.json 
    | 📜 requirements-dev.txt 
    | 📜 requirements.txt  
    | 📜 source.bat
```
Refer to each module's respective directory and stack file for more details on their implementation.

## Creating an AWS Cloud9 Environment

Below are the steps required to set up the environment and run this Data Engineering project on Cloud9 on AWS.

To create an AWS Cloud9 environment, you can follow these steps:

1. **Open the AWS Management Console:**
   - Go to the AWS Management Console at [https://console.aws.amazon.com](https://console.aws.amazon.com) and sign in to your AWS account.

2. **Navigate to Cloud9:**
   - Use the AWS services search bar or navigate to the "Developer Tools" category and select "Cloud9."

3. **Click "Create Environment":**
   - On the Cloud9 dashboard, click the "Create environment" button.

4. **Provide Environment Details:**
   - Enter a name for your environment. Optionally, enter a description.
   - Choose the environment type (new or clone an existing environment).
   - Select the instance type based on your requirements.
   - Choose the platform (Amazon Linux 2 or Ubuntu).

5. **Configure Settings:**
   - Choose the network settings (either create a new Amazon VPC or use an existing one).
   - Select the subnet for your environment.
   - Choose the IAM role that Cloud9 will use to access AWS resources on your behalf.
   - Configure additional settings as needed.

6. **Review and Create:**
   - Review the configuration details.
   - Enable the option to create an AWS CloudFormation stack if desired.
   - Click "Create environment" to start the provisioning process.

7. **Wait for the Environment to be Created:**
   - The Cloud9 environment creation process may take a few minutes. You can monitor the progress on the Cloud9 dashboard.

8. **Access the Cloud9 IDE:**
   - Once the environment is created, you can click on its name in the Cloud9 dashboard to access the Cloud9 Integrated Development Environment (IDE) in your web browser.
 
## Adding Policies to the Associated EC2 Instance

To enable a Python simulator to extract data from an S3 bucket and send it to a Kinesis stream, you need to add the following policies to the IAM role associated with the EC2 instance:

1. **Sign in to AWS Console**: Go to the [AWS Console](https://aws.amazon.com/console/), sign in to your account, and select the region where your EC2 instance is located.

2. **Open the IAM Service**: In the AWS Console, search and select the "IAM" (Identity and Access Management) service.

3. **Navigate to Roles**: In the left navigation pane, select "Roles" under "Access management."

4. **Find the Role Associated with Your EC2 Instance**: Locate the IAM role associated with your EC2 instance by selecting the relevant role from the list.

5. **Add Policies**: Once you are on the IAM role's details page, you can add the following policies to the role to grant permissions to the EC2 instance:

   a. In the "Permissions" section, select the "Add policies" button.

   b. Search for and select the following policies:
      - AmazonS3FullAccess
      - AmazonKinesisFullAccess

   c. Once you have selected the desired policies, click "Next: Review policy."

   d. Review and confirm the selected policies, and click "Add permissions."

6. **Confirm Changes**: Ensure you review and confirm the changes to the IAM role. You can add more policies if needed.

7. **Assign the IAM Role to Your EC2 Instance**: Make sure your EC2 instance is configured to use the IAM role you just modified. This is typically done when launching the EC2 instance or modifying the IAM role associated with an existing instance from the EC2 console.

## Setting up AWS CDK Environment

Follow these steps to set up your environment for AWS CDK (Cloud Development Kit) in Python:

1. **Install AWS CDK library:**
    - To install the AWS CDK library, run the following command:
    ```terminal
    python -m pip install aws-cdk-lib
    ```
    This installs the AWS CDK library, which is essential for AWS CDK development.

2. **Check CDK version:**
    - To verify the installed AWS CDK version, run the following command:
    ```terminal
    cdk --version
    ```
    This command will display the current AWS CDK version.

3. **Create a directory:**
    - Create a new directory by running:
    ```terminal
    mkdir directory_name
    ```
    This creates a directory with the name you choose.

4. **Navigate to the directory:**
    - Change to the newly created directory using the command:
    ```terminal
    cd directory_name/
    ```
    This takes you to the directory you just created.

5. **List files and directories:**
    - You can list the files and directories in the current directory with:
    ```terminal
    ls
    ```
    This command will show you a list of items in the current directory.

6. **Initialize a Python CDK app:**
    - To initialize a Python AWS CDK app, use the command:
    ```terminal
    cdk init app --language python
    ```
    This sets up a Python AWS CDK project in the current directory.

7. **Activate the virtual environment:**
    - Activate a virtual environment (assuming you already have one set up) with:
    ```terminal
    source .venv/bin/activate
    ```
    This activates the virtual environment, isolating project dependencies.

8. **Install project dependencies:**
    - To install project dependencies, use:
    ```terminal
    pip install -r requirements.txt
    ```
    This installs the libraries specified in the `requirements.txt` file.

9. **Install boto3 library:**
    - Boto3 is an AWS SDK for Python. Install it with:
    ```terminal
    pip install boto3
    ```
    This installs Boto3, enabling AWS service interaction in your project.

10. **Install python-decouple library:**
    - To install the python-decouple library, run:
    ```terminal
    pip install python_decouple
    ```
    This installs the library for working with configuration files in your project.

These steps are designed to help you set up your development environment for AWS CDK in Python.


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
  1. Focus changes on specific improvements.
  2. Follow project's coding style.
  3. Provide detailed descriptions in pull requests.
     
## Reporting Issues
  Use "Issues" to report bugs or suggest improvements.
  
# Contact
For questions or contact, my [Mail](diegovillatormx@gmail.com) or [Twitter](https://twitter.com/diegovillatomx). 

