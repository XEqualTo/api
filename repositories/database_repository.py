from core.exceptions import QueryExecutionError
from core.redshift_client import RedshiftDataClient
class DatabaseRepository:
    """Handles database queries related to Redshift."""

    def __init__(self):
        self.redshift_client = RedshiftDataClient()

    def fetch_all_databases(self):
        """Fetch all databases in Redshift."""
        try:
            query = "SELECT datname FROM pg_database;"
            response = self.redshift_client.execute_statement(Database="dev", Sql=query)
            return response['Records']
        except Exception as e:
            raise QueryExecutionError(f"Error fetching databases: {str(e)}")
