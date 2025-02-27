from repositories.database_repository import DatabaseRepository
from core.response import success_response, error_response

class DatabaseService:
    def __init__(self, db_repo: DatabaseRepository):
        self.db_repo = db_repo

    def get_all_databases(self):
        """Fetch all databases."""
        try:
            databases = self.db_repo.fetch_all_databases()
            return success_response(databases, "Databases retrieved successfully.")
        except Exception as e:
            return error_response(f"Database fetch error: {str(e)}")

    def get_schemas(self, database_name: str):
        """Fetch schemas from a specific database."""
        try:
            schemas = self.db_repo.fetch_schemas(database_name)
            return success_response(schemas, f"Schemas retrieved for {database_name}.")
        except Exception as e:
            return error_response(f"Schema fetch error: {str(e)}")

    def get_tables(self, database_name: str, schema_name: str):
        """Fetch tables from a schema."""
        try:
            tables = self.db_repo.fetch_tables(database_name, schema_name)
            return success_response(tables, f"Tables retrieved for {schema_name}.")
        except Exception as e:
            return error_response(f"Table fetch error: {str(e)}")
