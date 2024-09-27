import os
import uvicorn
from fastapi import FastAPI
from api.routes.upload_crime_data_route import router as load_crime_data_router
from api.routes.crime_data_analysis_route import router as crime_data_analysis_router
from util.logger import logger

app = FastAPI(title="City Crime Data API", version="1.0.0")

app.include_router(load_crime_data_router)
app.include_router(crime_data_analysis_router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting the FastAPI application")

def main():
    port = os.getenv("PORT", 8000)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    main()