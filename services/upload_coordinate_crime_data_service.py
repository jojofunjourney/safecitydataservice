from typing import List, Dict
from models.crime_data_models import UnifiedCrimeData
from util.logger import logger
from util.gcs_util import upload_to_gcs
from io import StringIO
import csv
from util.crime_data_util import count_crimes_by_coordinate


def convert_coordinate_crime_data_to_csv(data: Dict[str, int]) -> str:
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['coordinate', 'crime_count'])
    
    for coordinate, count in data.items():
        writer.writerow([coordinate, count])
    return output.getvalue()


def upload_coordinate_crime_data_to_gcs(data: List[UnifiedCrimeData], city: str, time_range: str, bucket_name: str):
    file_name = f"{city.lower()}_coordiante_crime_data_{time_range.lower()}.csv"
    print(f"Uploading coordiante crime data: {file_name} to {bucket_name}")
    
    # Transform data
    logger.info(f"Counting crimes by coordinate for {city.lower()}-{time_range.lower()}")
    coordinate_crime_data = count_crimes_by_coordinate(data)
    logger.info(f"Counted {len(coordinate_crime_data)} crimes by coordinate for {city}")
    
    # Load data to GCS
    logger.info(f"Converting {file_name} to CSV")
    csv_data = convert_coordinate_crime_data_to_csv(coordinate_crime_data)
    logger.info(f"Uploading {file_name} to GCS in {bucket_name}")
    upload_to_gcs(csv_data, bucket_name, file_name)
