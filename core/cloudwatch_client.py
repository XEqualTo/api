import boto3
from core.config import Settings

class CloudWatchClient:
    def __init__(self):
        self.client = boto3.client(
            "logs",
            region_name=Settings.AWS_REGION,
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
        )

    def get_log_events(self, log_group_name, log_stream_name, limit=10):
        """Fetch latest log events from CloudWatch Logs"""
        try:
            response = self.client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                limit=limit
            )
            return response["events"]
        except Exception as e:
            raise Exception(f"Error fetching logs from CloudWatch: {str(e)}")
