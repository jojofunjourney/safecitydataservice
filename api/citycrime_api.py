import logging
import json
import requests
from typing import Dict, List, Any
from config import SOCRATA_APP_TOKEN
from data.city_datasets import CITY_DATASETS

def fetch_city_data(city: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    logging.info(f"Fetching data for {city} from {start_date} to {end_date}")
    dataset = CITY_DATASETS[city]
    api_url = dataset["apiEndpoint"]
    query = f"$limit=100000&$where=date >= '{start_date}T00:00:00' AND date <= '{end_date}T23:59:59'"

    if city == "newYork":
        query += "&$select=cmplnt_fr_dt as date, ofns_desc as crime_type, latitude, longitude"
    elif city == "losAngeles":
        query += "&$select=date_occ as date, crm_cd_desc as crime_type, lat, lon"
    elif city == "chicago":
        query += "&$select=date, primary_type as crime_type, latitude, longitude"
    elif city == "seattle":
        query += "&$select=offense_start_datetime as date, offense as crime_type, latitude, longitude"
    else:
        raise ValueError("City-specific query not implemented")

    try:
        response = requests.get(f"{api_url}?{query}", headers={
            "X-App-Token": SOCRATA_APP_TOKEN,
            "Accept": "application/json",
        })
        response.raise_for_status()
        data = response.json()
        logging.info(f"Successfully fetched {len(data)} records for {city}")
        logging.debug(f"Sample data for {city}:\n{json.dumps(data[:5], indent=2)}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {city}: {str(e)}")
        return []