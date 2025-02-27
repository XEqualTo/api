from datetime import datetime, timedelta
from core.config import Settings
from repositories.cost_repository import CostRepository
from core.response import success_response, error_response


class CostService:
    def __init__(self, cost_repo: CostRepository):
        self.cost_repo = cost_repo

    def get_total_cost(self):
        """Fetch total AWS Redshift cost."""
        try:
            total_cost = self.cost_repo.get_total_cost()
            return success_response(total_cost, "Total cost retrieved successfully.")
        except Exception as e:
            return error_response(f"Cost fetch error: {str(e)}")

    def get_top_queries(self):
        """Fetch the most expensive queries."""
        try:
            top_queries = self.cost_repo.get_top_queries()
            return success_response(top_queries, "Top queries retrieved successfully.")
        except Exception as e:
            return error_response(f"Top query fetch error: {str(e)}")

    def get_optimization_suggestions(self):
        """Suggest cost optimization strategies."""
        try:
            suggestions = self.cost_repo.get_optimization_suggestions()
            return success_response(suggestions, "Optimization suggestions retrieved successfully.")
        except Exception as e:
            return error_response(f"Optimization error: {str(e)}")
