import logging
from datetime import datetime, timedelta
from collections import defaultdict
from google.cloud import bigtable
from google.cloud.bigtable import column_family
from api.citycrime_api import fetch_city_data
from data.city_datasets import CITY_DATASETS
from util.citycrime_data import count_crime_by_coordinate, load_coordinate_map_to_bigtable

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("Starting main function")
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    logging.info(f"Fetching data from {start_date} to {end_date}")

    # Initialize Bigtable client
    client = bigtable.Client(project="your-project-id", admin=True)
    instance = client.instance("your-instance-id")
    table = instance.table("city_crime_coordinate")

    # Create the table if it doesn't exist
    if not table.exists():
        logging.info("Creating table: city_crime_coordinate")
        table.create()
        cf = table.column_family("cf1")
        cf.create()

    for city in CITY_DATASETS.keys():
        try:
            logging.info(f"Processing {city}")
            raw_data = fetch_city_data(city, start_date, end_date)
            logging.debug(f"Fetched {len(raw_data)} raw records for {city}")
            
            if not raw_data:
                logging.warning(f"No data fetched for {city}, skipping further processing")
                continue
            
            coordinate_map = count_crime_by_coordinate(city, raw_data)
            logging.debug(f"Processed data for {city}: {len(coordinate_map)} unique coordinates")
            
            try:
                logging.info(f"Attempting to save data for {city} to Bigtable")
                load_coordinate_map_to_bigtable(table, city, coordinate_map)
                logging.info(f"Completed processing for {city}")
            except Exception as e:
                logging.error(f"Failed to save data for {city} to Bigtable. Error: {str(e)}")
                # Implement a retry mechanism or alert system here if needed
        except Exception as e:
            logging.error(f"Error processing {city}: {str(e)}")

    logging.info("Main function completed")

if __name__ == "__main__":
    main()