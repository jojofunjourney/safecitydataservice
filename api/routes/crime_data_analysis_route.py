from fastapi import APIRouter
from api.controllers.crime_data_analysis_controller import router as crime_data_analysis_router

router = APIRouter()

router.include_router(crime_data_analysis_router, prefix="/api/v1/crime-data-analysis")