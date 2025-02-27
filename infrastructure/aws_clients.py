import boto3
from core.exceptions import RedshiftConnectionError

def get_redshift_client():
    """Returns a Redshift Data API client."""
    try:
        return boto3.client("redshift-data", region_name="ap-south-2")
    except Exception as e:
        raise RedshiftConnectionError(f"Redshift client initialization failed: {str(e)}")

def get_cloudwatch_client():
    """Returns an AWS CloudWatch client."""
    try:
        return boto3.client("cloudwatch", region_name="us-east-1")
    except Exception as e:
        raise RedshiftConnectionError(f"CloudWatch client initialization failed: {str(e)}")
