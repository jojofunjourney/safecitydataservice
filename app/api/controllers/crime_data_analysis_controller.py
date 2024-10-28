from fastapi import APIRouter, HTTPException, Query

from app.services import analyze_crime_data, analyze_coordinate_crime_data
from app.models import CITIES, TIME_RANGES, CrimeDataList, CoordinateCrimeDataList
from app.util import logger

router = APIRouter()

@router.get("/", response_model=CrimeDataList)
async def analyze_crime_data_route(
    city: CITIES = Query(..., description="City to analyze"),
    time_range: TIME_RANGES = Query(..., description="Time range for analysis")
) -> CrimeDataList:
    try:
        logger.info(f"Received request for crime data analysis: city={city}, time_range={time_range}")
        crimeData = analyze_crime_data(city, time_range)
        logger.info(f"Analyzed crime result: {crimeData}")
        return crimeData
    except Exception as e:
        logger.error(f"Error during crime data analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/coordinate", response_model=CoordinateCrimeDataList)
async def coordinate_crime_data_route(
    city: CITIES = Query(..., description="City to analyze"),
    time_range: TIME_RANGES = Query(..., description="Time range for analysis")
) -> CoordinateCrimeDataList:
    try:
        logger.info(f"Analyzing coordinate crime data for {city} with time range: {time_range}")
        result = analyze_coordinate_crime_data(city, time_range)
        return result
    except Exception as e:
        logger.error(f"Error during coordinate crime data analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
