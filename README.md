# AWS Cost Optimization Tool

This project is an AWS cost optimization tool that helps analyze and optimize AWS Redshift queries and CloudWatch logs.

## Features
- **Redshift Query Analysis**: Identify slow and expensive queries.
- **CloudWatch Log Monitoring**: Retrieve logs and detect anomalies.
- **Cost Reports**: Generate cost reports based on AWS usage.

## Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **pip** (Python package manager)
- **Docker (optional)** (For containerized deployment)
- **AWS Account** with necessary permissions

## Installation
### 1. Clone the repository
```sh
git clone https://github.com/XEqualTo/api.git
cd api
```

### 2. Create and activate a virtual environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

## Configuration
1. Copy `.env.example` to `.env` and set up your environment variables:
```sh
cp .env.example .env
```
2. Update `.env` with your AWS credentials and Redshift details:
```ini
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=your-region
REDSHIFT_CLUSTER_ID=your-cluster-id
REDSHIFT_DATABASE=your-database-name
REDSHIFT_USER=your-username
REDSHIFT_PASSWORD=your-password
```

## Running the Application
### 1. Start the FastAPI server
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Access the API Documentation
Once the server is running, open your browser and visit:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Running with Docker (Optional)
### 1. Build and run the Docker container
```sh
docker build -t aws-cost-optimizer .
docker run -p 8000:8000 --env-file .env aws-cost-optimizer
```

## Folder Structure
```
aws-cost-optimization/
│── core/             # Core utilities and response handlers
│── routes/           # API route definitions
│── service/          # Business logic and service implementations
│── infrastructure/   # AWS clients, database connections
│── repositories/     # Data access layer for querying Redshift & CloudWatch
│── .env.example      # Example environment variables
│── main.py           # Application entry point
│── requirements.txt  # Python dependencies
│── README.md         # Project documentation
```
