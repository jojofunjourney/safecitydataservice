import uvicorn
from fastapi import FastAPI
from api.routes.upload_crime_data_route import router as load_crime_data_router
from api.routes.crime_data_analysis_route import router as crime_data_analysis_router
app = FastAPI(title="City Crime Data API", version="1.0.0")

from util.logger import logger

app.include_router(load_crime_data_router)
app.include_router(crime_data_analysis_router)

if __name__ == "__main__":
    logger.info("Starting the FastAPI application")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)