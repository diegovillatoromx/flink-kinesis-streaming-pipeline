from aws_cdk import Stack, aws_s3 as s3

from constructs import Construct
from decouple import config

PRIMARY_BUCKET_NAME = config("PRIMARY_BUCKET_NAME")


class S3BucketStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket = s3.Bucket(self, id="PrimaryBucket", bucket_name=PRIMARY_BUCKET_NAME)
