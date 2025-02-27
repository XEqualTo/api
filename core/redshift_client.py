import boto3
from core.config import Settings

class RedshiftDataClient:
    def __init__(self):
        """Initialize Redshift Data API client"""
        self.client = boto3.client(
            "redshift-data",
            region_name=Settings.AWS_REGION,
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
        )

    def execute_query(self, sql):
        """Execute SQL query using Redshift Data API"""
        try:
            response = self.client.execute_statement(
                Database=Settings.REDSHIFT_DATABASE,
                Sql=sql,
                WorkgroupName=Settings.REDSHIFT_CLUSTER_ID
            )
            return response
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")
