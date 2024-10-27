import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as api_router
from app.util import logger
from app.core.config import settings

print("Loading app/main.py")
print(f"Config object in main: {settings}")
print(f"Config dict in main: {settings.dict()}")

# Get the environment from the ENV variable or default to 'local'
env = os.getenv("ENVIRONMENT", "local")
logger.info(f"Running in {env} environment")

# Initialize FastAPI app with environment-specific title and version
app = FastAPI(
    title=f"City Crime Data API - {env.capitalize()}",
    version="1.0.0"
)

# Include the API router in the FastAPI app
app.include_router(api_router)

# Configure CORS based on environment (example: more open CORS for local)
origins = (
    ["http://localhost", "http://localhost:8000", "http://localhost:3000"]
    if env == "local"
    else ["https://your-production-site.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event handler
@app.on_event("startup")
async def startup_event():
    logger.info("Starting the FastAPI application")

# Shutdown event handler (optional, for clean shutdown)
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the FastAPI application")

# Run the application with environment-specific options
if __name__ == "__main__":
    # Reload only for the 'local' environment
    reload = env == "local"
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=reload)
