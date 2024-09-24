from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.crime_data_analysis_service import analyze_crime_data, analyze_coordinate_crime_data
from models.crime_data_models import CITIES, TIME_RANGES

router = APIRouter()

class CrimeDataAnalysisRequest(BaseModel):
      city: CITIES
      time_range: TIME_RANGES

class CrimeDataAnalysisResponse(BaseModel):
      total_crimes: int
      crime_statistics: list[dict]
      
class CoordinateCrimeDataRequest(BaseModel):
      city: CITIES
      time_range: TIME_RANGES

class CoordinateCrimeDataResponse(BaseModel):
      coordinate_crime_data: list[dict]

@router.get("/crime-data")
async def analyze_crime_data_route(request: CrimeDataAnalysisRequest) -> CrimeDataAnalysisResponse:
    try:
      city = request.city.value
      time_range = request.time_range.value
      result = analyze_crime_data(city, time_range)
      print(f"Analyzed crime result: {result}")
      return CrimeDataAnalysisResponse(
              total_crimes=result["total_crimes"],
              crime_statistics=result["crime_statistics"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e) )
  
@router.get("/coordinate-crime-data")
async def coordinate_crime_data_route(request: CoordinateCrimeDataRequest) -> CoordinateCrimeDataResponse:
      try:
            city = request.city.value
            time_range = request.time_range.value
            print(f"Analyzing coordinate crime data for {city} with time range: {time_range}")
            result = analyze_coordinate_crime_data(city, time_range)
            return CoordinateCrimeDataResponse(
                  coordinate_crime_data=result
            )
      except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            