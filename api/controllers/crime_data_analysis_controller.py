from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
from services.crime_data_analysis_service import analyze_crime_data, analyze_coordinate_crime_data
from models.crime_data_models import CITIES, TIME_RANGES
from util.logger import logger

router = APIRouter()

class CrimeDataAnalysisResponse(BaseModel):
    total_crimes: int
    crime_statistics: list[dict]

class CoordinateCrimeDataResponse(BaseModel):
    coordinate_crime_data: list[dict]

@router.get("/", response_model=CrimeDataAnalysisResponse)
async def analyze_crime_data_route(
    city: CITIES = Query(..., description="City to analyze"),
    time_range: TIME_RANGES = Query(..., description="Time range for analysis")
) -> CrimeDataAnalysisResponse:
    try:
        logger.info(f"Received request for crime data analysis: city={city.value}, time_range={time_range.value}")
        result = analyze_crime_data(city.value, time_range.value)
        logger.info(f"Analyzed crime result: {result}")
        return CrimeDataAnalysisResponse(
            total_crimes=result["total_crimes"],
            crime_statistics=result["crime_statistics"]
        )
    except Exception as e:
        logger.error(f"Error during crime data analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/coordinate", response_model=CoordinateCrimeDataResponse)
async def coordinate_crime_data_route(
    city: CITIES = Query(..., description="City to analyze"),
    time_range: TIME_RANGES = Query(..., description="Time range for analysis")
) -> CoordinateCrimeDataResponse:
    try:
        logger.info(f"Analyzing coordinate crime data for {city.value} with time range: {time_range.value}")
        result = analyze_coordinate_crime_data(city.value, time_range.value)
        return CoordinateCrimeDataResponse(
            coordinate_crime_data=result
        )
    except Exception as e:
        logger.error(f"Error during coordinate crime data analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
