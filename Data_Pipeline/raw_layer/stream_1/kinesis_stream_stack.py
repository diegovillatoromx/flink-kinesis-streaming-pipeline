from aws_cdk import Stack, aws_kinesis as kinesis, Duration
from constructs import Construct
from decouple import config

FIRST_STREAM_NAME = config("FIRST_STREAM_NAME")

class KinesisStreamStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stream_name = kinesis.Stream(
            self,
            "KinesisStream",
            stream_name=FIRST_STREAM_NAME,
            shard_count=1,
            retention_period=Duration.hours(24),
        )
