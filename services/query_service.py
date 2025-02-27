from repositories.query_repository import QueryRepository
from core.response import success_response, error_response

class QueryService:
    def __init__(self, query_repo: QueryRepository):
        self.query_repo = query_repo

    def execute_query(self, sql: str):
        """Execute a SQL query on Redshift."""
        try:
            result = self.query_repo.execute_query(sql)
            return success_response(result, "Query executed successfully.")
        except Exception as e:
            return error_response(f"Query execution error: {str(e)}")

    def get_query_history(self):
        """Get query execution history."""
        try:
            history = self.query_repo.get_query_history()
            return success_response(history, "Query history retrieved successfully.")
        except Exception as e:
            return error_response(f"Query history fetch error: {str(e)}")

    def get_long_running_queries(self):
        """Fetch long-running queries."""
        try:
            queries = self.query_repo.get_long_running_queries()
            return success_response(queries, "Long-running queries retrieved successfully.")
        except Exception as e:
            return error_response(f"Error fetching long-running queries: {str(e)}")

    def get_slow_queries_from_cloudwatch(self):
        """Fetch slow queries from CloudWatch logs."""
        try:
            slow_queries = self.query_repo.get_slow_queries_from_cloudwatch()
            return success_response(slow_queries, "Slow queries retrieved successfully.")
        except Exception as e:
            return error_response(f"Error fetching slow queries from CloudWatch: {str(e)}")

    def get_query_statistics(self):
        """Fetch query statistics."""
        try:
            stats = self.query_repo.get_query_statistics()
            return success_response(stats, "Query statistics retrieved successfully.")
        except Exception as e:
            return error_response(f"Error fetching query statistics: {str(e)}")