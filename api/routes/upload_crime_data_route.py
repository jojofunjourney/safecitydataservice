from fastapi import APIRouter
from api.controllers.upload_crime_data_controller import router as upload_crime_data_router

router = APIRouter()

router.include_router(upload_crime_data_router, prefix="/api/v1")