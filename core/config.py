import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-2")
    
    REDSHIFT_CLUSTER_ID: str = os.getenv("REDSHIFT_CLUSTER_ID")
    REDSHIFT_DATABASE: str = os.getenv("REDSHIFT_DATABASE")
    REDSHIFT_USER: str = os.getenv("REDSHIFT_USER")
    REDSHIFT_PASSWORD: str = os.getenv("REDSHIFT_PASSWORD")
    REDSHIFT_PORT: int = int(os.getenv("REDSHIFT_PORT", 5439))  # Added port

settings = Settings()
