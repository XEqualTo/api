import boto3
from botocore.exceptions import BotoCoreError, ClientError
from datetime import datetime, timedelta
from core.exceptions import CustomAPIException
from core.response import error_response
from core.cloudwatch_client import CloudWatchClient

class CostRepository:
    def __init__(self):
        """Initialize with an AWS CloudWatch client."""
        self.cloudwatch_client = CloudWatchClient()

    def get_total_cost(self):
        """Fetch the total AWS cost for each service using CloudWatch metrics."""
        try:
            response = self.cloudwatch_client.get_metric_statistics(
                Namespace="AWS/Usage",
                MetricName="EstimatedCharges",
                Dimensions=[{"Name": "ServiceName"}],  # Fetch for all services
                StartTime=datetime.utcnow() - timedelta(days=30),
                EndTime=datetime.utcnow(),
                Period=86400,  # 1-day intervals
                Statistics=["Maximum"],
                Unit="None"
            )

            if not response.get("Datapoints"):
                return {"total_cost": 0.0, "service_costs": {}, "message": "No cost data available."}

            service_costs = {}
            for point in response["Datapoints"]:
                service_name = point.get("ServiceName", "Unknown")
                service_costs[service_name] = round(point["Maximum"], 2)

            total_cost = sum(service_costs.values())

            return {
                "total_cost": round(total_cost, 2),
                "service_costs": service_costs
            }

        except (BotoCoreError, ClientError) as e:
            raise CustomAPIException(f"Failed to fetch AWS cost breakdown: {str(e)}")

    def get_top_queries(self):
        """Fetch most expensive queries based on execution time and cost."""
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
                return {"top_queries": [], "message": "No query cost data available."}

            sorted_queries = sorted(response["Datapoints"], key=lambda x: x["Maximum"], reverse=True)
            top_queries = sorted_queries[:5]  # Get top 5 expensive queries

            return {"top_queries": [{"runtime": q["Maximum"], "timestamp": q["Timestamp"]} for q in top_queries]}

        except (BotoCoreError, ClientError) as e:
            raise CustomAPIException(f"Failed to fetch top queries: {str(e)}")

    def get_optimization_suggestions(self):
        """Suggest cost optimization strategies based on usage."""
        try:
            total_cost = self.get_total_cost()["total_cost"]

            suggestions = []
            if total_cost > 1000:
                suggestions.append("Consider switching to Reserved Instances to save up to 75%.")

            if total_cost > 500:
                suggestions.append("Check unused nodes and downscale if necessary.")

            if not suggestions:
                suggestions.append("Your costs are optimized.")

            return {"cost_optimization_tips": suggestions}

        except (BotoCoreError, ClientError) as e:
            raise CustomAPIException(f"Failed to fetch cost optimization tips: {str(e)}")
