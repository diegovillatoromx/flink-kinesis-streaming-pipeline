import aws_cdk as cdk

class MyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket S3 for storing the CDK code
        bucket = cdk.Bucket(self, "MyBucket")

        # Create a CDK project
        project = cdk.Project(self, "MyProject")

        # Create a Kinesis Analytics application
        application = cdk.KinesisAnalyticsApplication(self, "MyApplication")

        # Create an output for the Glue table
        glue_output = cdk.KinesisAnalyticsOutput(
            application,
            "GlueOutput",
            table_name="us_accidents_stream",
            database_name="us_accidents_stream",
        )

        # Create an output for the destination Kinesis stream
        destination_output = cdk.KinesisAnalyticsOutput(
            application,
            "DestinationOutput",
            stream_name="us-accidents-data-stream-2",
        )

        # Create an output for the results Kinesis stream
        results_output = cdk.KinesisAnalyticsOutput(
            application,
            "ResultsOutput",
            stream_name="us_accidents-data-stream-1-results",
            sql="SELECT timestamp, accident_id, location, severity FROM ${us_accidents_stream}",
        )

        # Deploy the Kinesis Analytics application
        application.deploy()

