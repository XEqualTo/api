from fastapi import APIRouter, Depends
from services.cost_service import CostService
from repositories.cost_repository import CostRepository
from infrastructure.aws_clients import get_cloudwatch_client

router = APIRouter()

def get_cost_service():
    cloudwatch_client = get_cloudwatch_client()
    cost_repo = CostRepository(cloudwatch_client)
    return CostService(cost_repo)

@router.get("/cost/total")
async def get_total_cost(service: CostService = Depends(get_cost_service)):
    """Get total AWS Redshift cost."""
    return service.get_total_cost()

@router.get("/cost/top-queries")
async def get_top_queries(service: CostService = Depends(get_cost_service)):
    """Get the most expensive Redshift queries."""
    return service.get_top_queries()

@router.get("/cost/optimization")
async def get_optimization_suggestions(service: CostService = Depends(get_cost_service)):
    """Suggest cost optimization strategies."""
    return service.get_optimization_suggestions()
