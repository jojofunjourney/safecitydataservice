# app/api/controllers/__init__.py

from app.api.controllers.crime_data_analysis_controller import (
    router as crime_data_analysis_controller
)
from app.api.controllers.upload_crime_data_controller import (
    router as upload_crime_data_controller
)

# Expose the routers for easy import in the main router
__all__ = ["crime_data_analysis_controller", "upload_crime_data_controller"]
