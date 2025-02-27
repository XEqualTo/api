from fastapi import APIRouter, Depends
from services.database_service import DatabaseService
from repositories.database_repository import DatabaseRepository
from infrastructure.aws_clients import get_redshift_client

router = APIRouter()

def get_database_service():
    redshift_client = get_redshift_client()
    db_repo = DatabaseRepository(redshift_client)
    return DatabaseService(db_repo)

@router.get("/databases")
async def fetch_databases(service: DatabaseService = Depends(get_database_service)):
    """Fetch all databases in Redshift."""
    return service.get_all_databases()

@router.get("/schemas/{database_name}")
async def fetch_schemas(database_name: str, service: DatabaseService = Depends(get_database_service)):
    """Fetch schemas from a specific database."""
    return service.get_schemas(database_name)

@router.get("/tables/{database_name}/{schema_name}")
async def fetch_tables(database_name: str, schema_name: str, service: DatabaseService = Depends(get_database_service)):
    """Fetch tables from a specific schema."""
    return service.get_tables(database_name, schema_name)
