from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_cloudwatch as cloudwatch
)

from constructs import Construct

class S3AlertStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket.from_bucket_attributes(
            self,
            'alerting-bucket',
            bucket_arn = 'arn:aws:s3:::mygarbageforthenet'
        )

        bucket_count_metric = cloudwatch.Metric(
            namespace = "AWS/S3",
            metric_name = "NumberOfObjects",
            dimensions_map = {
                "BucketName": bucket.bucket_name,
                "StorageType": "AllStorageTypes",
            },
            period = Duration.hours(1),
            statistic="Maximum",
        )

        hourly_count_alarm = cloudwatch.Alarm(
            self,
            "Hourly Count Alarm",
            comparison_operator = cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 10,
            evaluation_periods = 1,
            metric = bucket_count_metric
        )

