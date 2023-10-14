from aws_cdk import Stack, aws_kinesis as kinesis, aws_kinesisfirehose as firehose, aws_s3 as s3, Duration
from constructs import Construct
from decouple import config

INTRADAY_STREAM_NAME = config("INTRADAY_STREAM_NAME")
RAW_DATA_BUCKET_NAME = config("RAW_DATA_BUCKET_NAME")
AWS_REGION = config("AWS_REGION")
AWS_ACCOUNT_ID = config("AWS_ACCOUNT_ID")  # New environment variable for account ID

class DataTransferStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get the S3 bucket from the environment
        raw_data_bucket = s3.Bucket.from_bucket_name(self, "RawDataBucket", RAW_DATA_BUCKET_NAME)

        # Create a Kinesis stream from the ARN of the existing stream
        intraday_stream_arn = f"arn:aws:kinesis:{AWS_REGION}:{AWS_ACCOUNT_ID}:stream/{INTRADAY_STREAM_NAME}"
        intraday_stream = kinesis.Stream.from_stream_arn(
            self, "IntradayKinesisStream", intraday_stream_arn
        )

        # Create a Kinesis Firehose delivery stream that writes data to the S3 bucket
        delivery_stream = firehose.DeliveryStream(
            self, id="DeliveryStream",
            stream_name=INTRADAY_STREAM_NAME,
            source_kinesis_stream=intraday_stream,
            s3_destination_configuration=firehose.S3DestinationConfiguration(
                bucket=raw_data_bucket,
                prefix="firehose-data",
            ),
        )


