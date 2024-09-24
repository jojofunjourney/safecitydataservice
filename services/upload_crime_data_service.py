import csv
from io import StringIO
from typing import List, Type
from dataclasses import asdict
from util.crime_data_util import transform_crime_data
from models.crime_data_models import UnifiedCrimeData, UnifiedCrimeDataFieldNames
from util.logger import logger
from util.gcs_util import upload_to_gcs

def upload_crime_data_to_gcs(raw_data: List[UnifiedCrimeData], city: str, time_range: str, bucket_name: str) -> List[UnifiedCrimeData]:
    file_name = f"{city.lower()}_crime_data_{time_range.lower()}.csv"
    logger.info(f"Uploading crime data for {city} with time range: {time_range} to {file_name} in {bucket_name}")
        
    # Transform data
    logger.info(f"Transforming data for {city.lower()}-{time_range.lower()}")
    transformed_data: List[UnifiedCrimeData] = transform_crime_data(city, raw_data)
    logger.info(f"Transformed {len(transformed_data)} data for {city}")
    
    # Load data to GCS
    logger.info(f"Transform {file_name} into CSV ")
    csv_data = convert_crime_data_to_csv(transformed_data)
    logger.info(f"Uploading {file_name} to GCS in {bucket_name}")
    upload_to_gcs(csv_data, bucket_name, file_name)
    
    return transformed_data
    
def convert_crime_data_to_csv(data: List[Type[UnifiedCrimeData]]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=UnifiedCrimeDataFieldNames)
    writer.writeheader()
    for row in data:
        writer.writerow(asdict(row))
    return output.getvalue()