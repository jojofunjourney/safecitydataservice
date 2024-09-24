# from pyspark.sql import SparkSession, DataFrame, Row
# from pyspark.sql.functions import count, col, round
# from pyspark.storagelevel import StorageLevel
from config import GOOGLE_APPLICATION_CREDENTIALS_JSON
from typing import Any, Callable

from google.cloud import bigquery
from google.oauth2 import service_account

def create_bigquery_client():
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS_JSON)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    return client

def read_data_from_bigquery(query: str, process_data: Callable[[bigquery.table.RowIterator], Any]) -> Any:
      client = create_bigquery_client()
      query_job = client.query(query)
      result = query_job.result()
      return process_data(result)

def process_all_crime_data_bigquery(rows: bigquery.table.RowIterator) -> dict[str, Any]:
      rows_list = list(rows)
      if not rows_list:
            raise ValueError("No data found in the BigQuery result.")
      
      crime_statistics = []
      for row in rows_list:
            crime_statistics.append({
                  "crime_type": row["offense_type"],
                  "count": row["count"],
                  "percentage": row["percentage"]
            })
            
      total_crimes = sum(row['count'] for row in rows_list)
      
      return {
            "total_crimes": total_crimes,
            "crime_statistics": crime_statistics
      }
      
def analyze_crime_data(city:str, time_range:str) -> dict[str, Any]:
      query = f"""
      SELECT 
            offense_type,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
      FROM 
            `safe-city-walk.city_crime_data.newyork_city_crime_data_6months`
      GROUP BY 
            offense_type
      ORDER BY 
            count DESC
      """
      return read_data_from_bigquery(query, process_all_crime_data_bigquery)

def process_coordinate_crime_data(rows: bigquery.table.RowIterator) -> list:
      rows_list = list(rows)
      if not rows_list:
            raise ValueError("No data found in the BigQuery result.")
      
      coordinate_crime_data = []
      for row in rows_list:
            coordinate_crime_data.append({
                  "coordinate": row["coordinate"],
                  "crime_count": row["crime_count"]
            })
      
      return coordinate_crime_data

def analyze_coordinate_crime_data(city: str, time_range: str) -> list[dict]:
      query = f"""
      SELECT 
            coordinate,
            COUNT(*) as crime_count
      FROM 
            `safe-city-walk.coordinate_crime_data.newyork_coordiante_crime_data_6months`
      GROUP BY 
            coordinate
      ORDER BY 
            crime_count DESC
      """
      return read_data_from_bigquery(query, process_coordinate_crime_data)

      
''' Use Spark to process the crime data
def create_spark_session():
      spark = SparkSession.builder \
            .appName("CrimeDataAnalysis") \
            .config("spark.jars", "https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar") \
            .config("google.cloud.auth.service.account.enable", "true") \
            .config("google.cloud.auth.service.account.json.keyfile", GOOGLE_APPLICATION_CREDENTIALS_JSON) \
            .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
            .config("spark.executor.memory", "4g") \
            .config("spark.executor.cores", "4") \
            .config("spark.driver.memory", "4g") \
            .config("spark.driver.cores", "4") \
            .config("spark.network.timeout", "800s") \
            .config("spark.rpc.askTimeout", "600s") \
            .getOrCreate()
            
      #   .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \

      # Set Hadoop configurations for GCS
      # hadoop_conf = spark._jsc.hadoopConfiguration()
      # hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
      # hadoop_conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
      # hadoop_conf.set("google.cloud.auth.service.account.enable", "true")
      # hadoop_conf.set("google.cloud.auth.service.account.json.keyfile", GOOGLE_APPLICATION_CREDENTIALS_JSON)
      
      return spark

def read_file_from_gcs_and_process(file_name: str, process_df: Callable[[DataFrame], DataFrame]) -> Any:
      # Initialize Spark session
      spark = create_spark_session()
      
      # read the csv file directly from GCS
      df = spark.read.csv(file_name, header=True, inferSchema=True)
      
      # Repartition the DF to optimize the parallelism
      df = df.repartition(100)
      
      # Cache the DF on disk
      df.cache()
      
      # Process the DF
      result = process_df(df)
      
      # Unpersist the cached DataFrame
      df.unpersist()
      
      # Stop spark session
      spark.stop()
      
      return result

def process_all_crime_data(df: DataFrame) -> dict[str, Any]:
      # ensure the 'offense_type' column exists
      if 'offense_type' not in df.columns:
            raise ValueError("The 'offense_type' column is missing from the dataset.")
      
      # Count total crimes
      total_crimes = df.count()
      
      # Calculate crime counts by type
      grouped_df = df.groupBy("offense_type")
      
      # Aggregate the grouped DF to count the occurrence
      agg_df = grouped_df.agg(count("*").alias("count"))
      
      # Order the aggregated DF by the count in DESC
      ordered_df = agg_df.orderBy("count", ascending=False)
      
      # Calculate percentages
      crime_df = ordered_df.withColumn("percentage", round(col("count") / total_crimes * 100, 2))
      
      # Collect the results
      crime_list = crime_df.collect()
      
      # Prepare the result dictionary
      result = {
            "total_crimes": total_crimes,
            "crime_statistics": [
                  {
                        "crime_type": row["offense_type"],
                        "count": row["count"],
                        "percentage": row["percentage"]
                  } for row in crime_list
            ]
      }
      
      return result

def analyze_crime_data(city: str, time_range: str) -> dict[str, Any]:
      # Read file from GCS and process the DF
      file_name = f"gs://{GCS_BUCKET_NAME}/{city.lower()}_crime_data_{time_range.lower()}.csv"
      result = read_file_from_gcs_and_process(file_name, process_all_crime_data)
      
      return result'''
