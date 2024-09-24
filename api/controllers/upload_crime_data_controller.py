from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal, Type
from services.upload_crime_data_service import upload_crime_data_to_gcs
from services.upload_coordinate_crime_data_service import upload_coordinate_crime_data_to_gcs
from config import GCS_BUCKET_NAME
from models.crime_data_models import TIME_RANGES, CITIES
from util.fetch_crime_data import fetch_city_data
from util.logger import logger

router = APIRouter()

class UpLoadCrimeDataRequest(BaseModel):
    city: CITIES
    time_range: TIME_RANGES

class UpLoadCrimeDataResponse(BaseModel):
    message: str

@router.post("/upload_crime_data", response_model=UpLoadCrimeDataResponse)
async def upload_crime_data(request: UpLoadCrimeDataRequest) -> UpLoadCrimeDataResponse:
    try:
        city = request.city.value
        time_range = request.time_range.value
        logger.info(f"Received request to upload crime data for {city} with time range: {time_range}")
        
        # fetch crime raw data
        logger.info(f"Fetching raw crime data for {city}")
        raw_data = fetch_city_data(city, time_range)
        logger.info(f"Successfully fetched {len(raw_data)} records of raw data for {city}")
        
        # upload all crime data to GCS
        logger.info(f"Uploading all crime data to GCS for {city}")
        transformed_data = upload_crime_data_to_gcs(raw_data, city, time_range, GCS_BUCKET_NAME)
        logger.info(f"Successfully uploaded all crime data to GCS for {city}")
        
        # upload coordinate crime data to GCS
        logger.info(f"Uploading coordinate crime data to GCS for {city}")
        upload_coordinate_crime_data_to_gcs(transformed_data, city, time_range, GCS_BUCKET_NAME)
        logger.info(f"Successfully uploaded coordinate crime data to GCS for {city}")
        
        success_message = f"Crime data for {city} loaded successfully"
        logger.info(success_message)
        return UpLoadCrimeDataResponse(message=success_message)
    except Exception as e:
        error_message = f"Error uploading crime data for {city}: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)