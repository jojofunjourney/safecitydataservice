import requests
from typing import List
from config import SOCRATA_APP_TOKEN
from models.crime_data_models import UnifiedCrimeData
from constants import CITY_DATASETS
from datetime import datetime, timedelta

def fetch_city_data(city: str, time_range: str) -> List[UnifiedCrimeData]:
    print(f"Fetching data for {city} with time range: {time_range}")
    end_date = datetime.now()
    
    if time_range == "1year":
        start_date = end_date - timedelta(days=365)
    elif time_range == "6months":
        start_date = end_date - timedelta(days=180)
    elif time_range == "3months":
        start_date = end_date - timedelta(days=90)
    else:
        raise ValueError("Invalid time range")

    # Convert dates to string format required by the API
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    city_api = CITY_DATASETS.__dict__[city]
    
    api_url = f"{city_api.apiEndpoint}?{city_api.query.format(start_date=start_date_str, end_date=end_date_str)}"
    print(f"Fetching data for {city} with api_url: {api_url}")
    
    try:    
        response = requests.get(api_url, headers={
            "X-App-Token": SOCRATA_APP_TOKEN,
            "Accept": "application/json"
        })
        response.raise_for_status()
        data = response.json()

        print(f"Received {len(data)} rows for {city}")
        return data
    except requests.RequestException as error:
        print(f"Error fetching data for {city}: {error}")
        raise
