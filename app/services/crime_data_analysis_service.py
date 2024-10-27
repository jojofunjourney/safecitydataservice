# from pyspark.sql import SparkSession, DataFrame, Row
# from pyspark.sql.functions import count, col, round
# from pyspark.storagelevel import StorageLevel
from typing import Any, Callable, Union

from google.cloud import bigquery
from google.oauth2 import service_account

from app.core.config import settings as config
from app.util import Environment, logger
from app.models import CITIES, TIME_RANGES, DATA_TYPE, BigQueryDataset, BigQueryTableName, CreateCrimeData, CreateCoordinateCrimeData, CrimeDataList, CoordinateCrimeDataList

CrimeDataResult = Union[CrimeDataList, CoordinateCrimeDataList]

def create_bigquery_client():
    env = config.ENVIRONMENT
    logger.debug(f"Environment: {env}")
    if env in [Environment.PROD, Environment.STAGE]:
        client = bigquery.Client()
    else:
        credentials_file = config.GOOGLE_CREDENTIALS_FILE
        logger.debug(f"Using credentials file: {credentials_file}")
        credentials = service_account.Credentials.from_service_account_file(credentials_file)
        logger.debug(f"Credentials: {credentials}")
        logger.debug(f"Project ID from credentials: {credentials.project_id}")
        
        # Use the project ID from settingsq
        project_id = config.GCP_PROJECT_ID
        logger.debug(f"Using project ID: {project_id}")
        
        client = bigquery.Client(credentials=credentials, project=project_id)
    return client

def read_data_from_bigquery(query: str, process_data: Callable[[bigquery.table.RowIterator], CrimeDataResult]) -> CrimeDataResult:
    client = create_bigquery_client()
    try:
        query_job = client.query(query)
        result = query_job.result()
        return process_data(result)
    except Exception as e:
        logger.error(f"Error executing BigQuery query: {str(e)}")
        raise

def create_bigquery_query(project_id: str, city: CITIES, time_range: TIME_RANGES, data_type: DATA_TYPE) -> str:
    logger.info(f"Creating BigQuery query for city: {city}, time_range: {time_range}, data_type: {data_type}")

    try:
        dataset = BigQueryDataset(city).get_dataset_name()
        table = BigQueryTableName(city, time_range, data_type).get_table_name()
        
        logger.debug(f"Dataset: {dataset}")
        logger.debug(f"Table: {table}")
        
        if data_type == DATA_TYPE.CRIME_DATA:
            query = f"""
            SELECT 
                offense_type,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
            FROM 
                `{project_id}.{dataset}.{table}`
            GROUP BY 
                offense_type
            ORDER BY 
                count DESC
            """
        elif data_type == DATA_TYPE.COORDINATE_CRIME_DATA:
            query = f"""
            SELECT 
                coordinate,
                COUNT(*) as crime_count
            FROM 
                `{project_id}.{dataset}.{table}`
            GROUP BY 
                coordinate
            ORDER BY 
                crime_count DESC
            """
        logger.debug(f"Generated query: {query}")
        return query
    except Exception as e:
        logger.error(f"Error creating BigQuery query: {str(e)}")
        raise

def process_all_crime_data_bigquery(rows: bigquery.table.RowIterator) -> CrimeDataList:
    logger.info("Processing all crime data from BigQuery")
    rows_list = list(rows)
    if not rows_list:
        logger.warning("No data found in the BigQuery result.")
        raise ValueError("No data found in the BigQuery result.")
    
    crime_statistics = []
    for row in rows_list:
        logger.debug(f"Processing row: {row}")
        crime_statistics.append(CreateCrimeData(crime_type=row["offense_type"], count=row["count"], percentage=row["percentage"]))
        
    total_crimes = 0
    for stat in crime_statistics:
        logger.debug(f"Processing crime statistic: {stat}")
        total_crimes += stat.count
    
    logger.info(f"Processed {len(crime_statistics)} crime statistics")
    logger.debug(f"Total crimes: {total_crimes}")
    return CrimeDataList(
        total_crimes=total_crimes,
        crime_statistics=crime_statistics
    )
      
def analyze_crime_data(city: CITIES, time_range: TIME_RANGES) -> CrimeDataList:
    logger.info(f"Analyzing crime data for city: {city}, time_range: {time_range}")
    project_id = config.GCP_PROJECT_ID
    query = create_bigquery_query(project_id, city, time_range, DATA_TYPE.CRIME_DATA)
    logger.debug(f"Executing query: {query}")
    return read_data_from_bigquery(query, process_all_crime_data_bigquery)

def process_coordinate_crime_data(rows: bigquery.table.RowIterator) -> CoordinateCrimeDataList:
    logger.info("Processing coordinate crime data from BigQuery")
    rows_list = list(rows)
    if not rows_list:
        logger.warning("No data found in the BigQuery result.")
        raise ValueError("No data found in the BigQuery result.")
    
    coordinate_crime_data = []
    for row in rows_list:
        coordinate_crime_data.append(CreateCoordinateCrimeData(coordinate=row["coordinate"], crime_count=row["crime_count"]))
    
    logger.info(f"Processed {len(coordinate_crime_data)} coordinate crime data points")
    return CoordinateCrimeDataList(
        coordinate_crime_data=coordinate_crime_data
    )

def analyze_coordinate_crime_data(city: CITIES, time_range: TIME_RANGES) -> CoordinateCrimeDataList:
    logger.info(f"Analyzing coordinate crime data for city: {city}, time_range: {time_range}")
    project_id = config.GCP_PROJECT_ID
    query = create_bigquery_query(project_id, city, time_range, DATA_TYPE.COORDINATE_CRIME_DATA)
    logger.debug(f"Executing query: {query}")
    return read_data_from_bigquery(query, process_coordinate_crime_data)
