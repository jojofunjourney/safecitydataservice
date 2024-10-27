# app/api/routes/__init__.py

from fastapi import APIRouter
from app.api.controllers import (
    crime_data_analysis_controller,
    upload_crime_data_controller,
)

# Initialize the main router
router = APIRouter()

# Include the controllers' routers with versioned prefixes
router.include_router(crime_data_analysis_controller, prefix="/api/v1/crime-data-analysis")
router.include_router(upload_crime_data_controller, prefix="/api/v1/upload-crime-data")

# Expose the main router for easy import in the main app
__all__ = ["router"]
