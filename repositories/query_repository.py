import boto3
import psycopg2
from botocore.exceptions import BotoCoreError, ClientError
from psycopg2 import OperationalError, DatabaseError
from datetime import datetime, timedelta
from core.exceptions import CustomAPIException
from core.response import error_response
from core.redshift_client import RedshiftDataClient
from core.cloudwatch_client import CloudWatchClient

class QueryRepository:
    def __init__(self):
        """Initialize with a Redshift database connection and AWS CloudWatch client."""
        self.redshift_client = RedshiftDataClient()
        self.cloudwatch_client = CloudWatchClient()

    def get_long_running_queries(self):
        """Fetch long-running queries from Redshift system tables."""
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT query, user, starttime, total_exec_time
                    FROM stl_query
                    WHERE total_exec_time > 10000  -- Queries taking longer than 10s
                    ORDER BY total_exec_time DESC
                    LIMIT 10
                """)
                queries = cursor.fetchall()

            return [
                {
                    "query_id": q[0],
                    "user": q[1],
                    "start_time": q[2],
                    "execution_time_ms": q[3]
                } for q in queries
            ]

        except (OperationalError, DatabaseError) as e:
            raise CustomAPIException(f"Database error while fetching long-running queries: {str(e)}")

    def get_slow_queries_from_cloudwatch(self):
        """Fetch slow queries based on CloudWatch logs."""
        try:
            response = self.cloudwatch_client.get_metric_statistics(
                Namespace="AWS/Redshift",
                MetricName="QueryRuntime",
                Dimensions=[{"Name": "ClusterIdentifier", "Value": "your-cluster-id"}],
                StartTime=datetime.utcnow() - timedelta(days=7),
                EndTime=datetime.utcnow(),
                Period=3600,  # 1-hour intervals
                Statistics=["Maximum"],
                Unit="Seconds"
            )

            if not response.get("Datapoints"):
                return {"slow_queries": [], "message": "No slow query data available."}

            slow_queries = sorted(response["Datapoints"], key=lambda x: x["Maximum"], reverse=True)[:5]

            return {
                "slow_queries": [{"runtime": q["Maximum"], "timestamp": q["Timestamp"]} for q in slow_queries]
            }

        except (BotoCoreError, ClientError) as e:
            raise CustomAPIException(f"Failed to fetch slow queries from CloudWatch: {str(e)}")

    def get_query_statistics(self):
        """Fetch query statistics including total count, avg runtime, and errors."""
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*), AVG(total_exec_time), COUNT(CASE WHEN aborted = 1 THEN 1 END)
                    FROM stl_query
                    WHERE starttime >= CURRENT_DATE - INTERVAL '7 days'
                """)
                stats = cursor.fetchone()

            return {
                "total_queries": stats[0],
                "avg_execution_time_ms": round(stats[1], 2) if stats[1] else 0,
                "failed_queries": stats[2]
            }

        except (OperationalError, DatabaseError) as e:
            raise CustomAPIException(f"Database error while fetching query statistics: {str(e)}")
    
    def get_query_history(self, start_time=None, end_time=None, limit=10):
        """
        Fetches query execution history from Amazon Redshift.

        :param start_time: (Optional) Start time for query filtering.
        :param end_time: (Optional) End time for query filtering.
        :param limit: Number of queries to retrieve.
        :return: List of executed queries with execution times and status.
        """
        try:
            # Default to last 24 hours if no time range provided
            if not start_time:
                start_time = datetime.utcnow() - timedelta(days=1)
            if not end_time:
                end_time = datetime.utcnow()

            sql_query = f"""
                SELECT query, starttime, endtime, total_exec_time, querytxt, aborted
                FROM stl_query
                WHERE userid > 1
                AND starttime BETWEEN '{start_time}' AND '{end_time}'
                ORDER BY starttime DESC
                LIMIT {limit}
            """

            response = self.redshift_client.execute_statement(
                ClusterIdentifier=self.cluster_identifier,
                Database=self.database,
                DbUser=self.db_user,
                Sql=sql_query
            )

            statement_id = response["Id"]

            # Wait for query execution to complete
            while True:
                status = self.redshift_client.describe_statement(Id=statement_id)
                if status["Status"] in ["FINISHED", "FAILED", "ABORTED"]:
                    break

            if status["Status"] != "FINISHED":
                raise CustomAPIException(f"Failed to fetch query history: {status['Error']}")

            # Retrieve results
            results = self.redshift_client.get_statement_result(Id=statement_id)

            query_history = []
            for record in results["Records"]:
                query_history.append({
                    "query_id": record[0]["stringValue"],
                    "start_time": record[1]["stringValue"],
                    "end_time": record[2]["stringValue"],
                    "execution_time_ms": float(record[3]["stringValue"]),
                    "query_text": record[4]["stringValue"],
                    "aborted": record[5]["booleanValue"]
                })

            return {"query_history": query_history}

        except (BotoCoreError, ClientError) as e:
            raise CustomAPIException(f"Failed to retrieve query history: {str(e)}")

    def execute_query(self, sql: str):
        """
        Executes a given SQL query on Amazon Redshift and returns the results.

        :param sql: The SQL query string to be executed.
        :return: Query execution results or an error message.
        """
        try:
            response = self.redshift_client.execute_statement(
                ClusterIdentifier=self.cluster_identifier,
                Database=self.database,
                DbUser=self.db_user,
                Sql=sql
            )

            statement_id = response["Id"]

            # Wait for the query execution to complete
            while True:
                status = self.redshift_client.describe_statement(Id=statement_id)
                if status["Status"] in ["FINISHED", "FAILED", "ABORTED"]:
                    break

            if status["Status"] != "FINISHED":
                raise CustomAPIException(f"Query execution failed: {status.get('Error', 'Unknown error')}")

            # Fetch query results
            results = self.redshift_client.get_statement_result(Id=statement_id)

            query_results = []
            column_names = [column["name"] for column in results["ColumnMetadata"]]

            for record in results["Records"]:
                row = {column_names[i]: list(record[i].values())[0] for i in range(len(column_names))}
                query_results.append(row)

            return {
                "message": "Query executed successfully.",
                "query_results": query_results
            }

        except (BotoCoreError, ClientError) as e:
            raise CustomAPIException(f"Error executing query: {str(e)}")