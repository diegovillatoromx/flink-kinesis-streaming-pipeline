from aws_cdk import Stack, aws_s3 as s3

from constructs import Construct
from decouple import config

# Env. variables; i.e. can be OS variables in Lambda
# This is the name of the S3 bucket that will store the raw data
RAW_DATA_BUCKET_NAME = config("RAW_DATA_BUCKET_NAME")


class RawDataBucketStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket = s3.Bucket(self, id="RawDataBucket", bucket_name=RAW_DATA_BUCKET_NAME)