
from constructs import Construct
from decouple import config

DATASET_BUCKET_NAME = config("DATASET_BUCKET_NAME")

class S3BucketStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket = s3.Bucket(self, id="DATASET_BUCKET_NAME", bucket_name=DATASET_BUCKET_NAME)
