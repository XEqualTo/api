from fastapi import APIRouter, Depends
from services.query_service import QueryService
from repositories.query_repository import QueryRepository
from infrastructure.aws_clients import get_redshift_client

router = APIRouter()

def get_query_service():
    redshift_client = get_redshift_client()
    query_repo = QueryRepository(redshift_client)
    return QueryService(query_repo)

@router.post("/query/execute")
async def execute_query(query: dict, service: QueryService = Depends(get_query_service)):
    """Execute a Redshift query."""
    return service.execute_query(query["sql"])

@router.get("/query/history")
async def get_query_history(service: QueryService = Depends(get_query_service)):
    """Get query execution history."""
    return service.get_query_history()


@router.get("/query/long-running")
async def get_long_running_queries(service: QueryService = Depends(get_query_service)):
    """Get long-running queries from Redshift."""
    return service.get_long_running_queries()

@router.get("/query/slow")
async def get_slow_queries(service: QueryService = Depends(get_query_service)):
    """Get slow queries from CloudWatch logs."""
    return service.get_slow_queries_from_cloudwatch()

@router.get("/query/statistics")
async def get_query_statistics(service: QueryService = Depends(get_query_service)):
    """Get query statistics from Redshift."""
    return service.get_query_statistics()
