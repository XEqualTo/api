from fastapi import FastAPI
from routes.database_routes import router as database_router
from routes.query_routes import router as query_router
from routes.cost_routes import router as cost_router
app = FastAPI()

# Include routers
app.include_router(database_router, prefix="/api", tags=["Databases"])
app.include_router(query_router, prefix="/api", tags=["Queries"])
app.include_router(cost_router, prefix="/api", tags=["Cost"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
