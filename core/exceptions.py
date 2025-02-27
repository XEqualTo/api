class RedshiftConnectionError(Exception):
    """Exception raised when Redshift connection fails."""
    def __init__(self, message="Failed to connect to Redshift cluster"):
        self.message = message
        super().__init__(self.message)

class QueryExecutionError(Exception):
    """Exception raised when a query fails."""
    def __init__(self, message="Error executing query on Redshift"):
        self.message = message
        super().__init__(self.message)

class CustomAPIException(Exception):
    """Custom exception class to handle API errors gracefully."""
    
    def __init__(self, message: str, status_code: int = 400):
        """
        :param message: Error message to be displayed.
        :param status_code: HTTP status code (default: 400 Bad Request).
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """Convert exception details into a dictionary for JSON responses."""
        return {"error": self.message, "status_code": self.status_code}
