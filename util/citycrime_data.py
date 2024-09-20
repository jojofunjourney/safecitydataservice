import logging
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import Counter, defaultdict

def count_crime_by_coordinate(city: str, raw_data: list) -> dict:
    coordinate_map = defaultdict(int)
    for crime in raw_data:
        lat = crime.get('latitude') or crime.get('lat')
        lon = crime.get('longitude') or crime.get('lon')
        if lat and lon:
            coordinate = (float(lat), float(lon))
            coordinate_map[coordinate] += 1
    return dict(coordinate_map)

def load_coordinate_map_to_bigtable(table, city: str, coordinate_map: dict):
    rows = []
    for (lat, lon), count in coordinate_map.items():
        row_key = f"{city}_{lat:.6f}_{lon:.6f}".encode()
        row = table.direct_row(row_key)
        row.set_cell("cf1", "city".encode(), city.encode())
        row.set_cell("cf1", "latitude".encode(), str(lat).encode())
        row.set_cell("cf1", "longitude".encode(), str(lon).encode())
        row.set_cell("cf1", "crime_count".encode(), str(count).encode())
        rows.append(row)

    table.mutate_rows(rows)
    logging.info(f"Loaded {len(rows)} rows for {city} into Bigtable")


def transform_data(city: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforms raw crime data for a given city into a standardized format.

    This function processes a list of crime data items, extracting and normalizing
    key information such as date, crime type, latitude, and longitude. It handles
    different field names that might be present in various data sources.

    Args:
        city (str): The name of the city for which data is being transformed.
        data (List[Dict[str, Any]]): A list of dictionaries containing raw crime data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries with standardized crime data,
        sorted by date in descending order. Each dictionary contains 'date', 
        'crime_type', 'latitude', and 'longitude' keys.

    Example return value:
    [
        {
            "date": "2023-04-15T14:30:00.000",
            "crime_type": "THEFT",
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        {
            "date": "2023-04-14T09:15:00.000",
            "crime_type": "ASSAULT",
            "latitude": 40.7135,
            "longitude": -74.0070
        }
    ]
    """
    logging.info(f"Transforming data for {city}")
    transformed_data = []
    for item in data:
        latitude = item.get("latitude") or item.get("lat")
        longitude = item.get("longitude") or item.get("lng") or item.get("lon")
        
        if not latitude or not longitude:
            logging.warning(f"Skipping item due to missing latitude or longitude:\n{json.dumps(item, indent=2)}")
            continue
        
        date_str = item.get("date") or item.get("cmplnt_fr_dt") or item.get("date_occ") or item.get("offense_start_datetime")
        try:
            # Parse the date string and convert it to a standard format
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
            standardized_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            logging.warning(f"Skipping item due to invalid date format: {date_str}")
            continue
        
        transformed_item = {
            "date": standardized_date,
            "crime_type": item["crime_type"],
            "latitude": float(latitude),
            "longitude": float(longitude),
        }
        transformed_data.append(transformed_item)
    
    # Sort the transformed data by date in descending order
    transformed_data.sort(key=lambda x: x["date"], reverse=True)
    
    logging.info(f"Transformed {len(transformed_data)} records for {city}")
    logging.debug(f"Sample transformed data for {city}:\n{json.dumps(transformed_data[:5], indent=2)}")
    return transformed_data

def calculate_time_range_data(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Calculates crime statistics for different time ranges based on the provided crime data.

    This function analyzes the transformed crime data and computes statistics for
    three time ranges: 3 months, 6 months, and 1 year. For each time range, it
    calculates the total number of crimes and a breakdown of crime types with their counts.

    Args:
        data (List[Dict[str, Any]]): A list of dictionaries containing transformed crime data.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary where keys are time range names
        ("3months", "6months", "1year") and values are dictionaries containing:
        - "totalCrime": The total number of crimes in that time range
        - "crimeBreakdown": A list of dictionaries, each containing a crime type
          and its count, sorted in descending order by count.

    Example return value:
    {
        "3months": {
            "totalCrime": 1000,
            "crimeBreakdown": [
                {"crimeType": "THEFT", "count": 300},
                {"crimeType": "ASSAULT", "count": 200},
                {"crimeType": "BURGLARY", "count": 150}
            ]
        },
        "6months": {
            "totalCrime": 2200,
            "crimeBreakdown": [
                {"crimeType": "THEFT", "count": 700},
                {"crimeType": "ASSAULT", "count": 450},
                {"crimeType": "BURGLARY", "count": 350}
            ]
        },
        "1year": {
            "totalCrime": 4500,
            "crimeBreakdown": [
                {"crimeType": "THEFT", "count": 1500},
                {"crimeType": "ASSAULT", "count": 1000},
                {"crimeType": "BURGLARY", "count": 750}
            ]
        }
    }
    """
    logging.info("Calculating time range data")
    today = datetime.now()
    time_ranges = {
        "3months": today - timedelta(days=90),
        "6months": today - timedelta(days=180),
        "1year": today - timedelta(days=365),
    }
    
    result = {}
    for range_name, start_date in time_ranges.items():
        filtered_data = [
            item for item in data
            if datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S.%f") >= start_date
        ]
        
        crime_counts = {}
        for item in filtered_data:
            crime_type = item["crime_type"]
            crime_counts[crime_type] = crime_counts.get(crime_type, 0) + 1
        
        total_crime = len(filtered_data)
        
        crime_breakdown = [
            {"crimeType": crime_type, "count": count}
            for crime_type, count in crime_counts.items()
        ]
        crime_breakdown.sort(key=lambda x: x["count"], reverse=True)
        
        result[range_name] = {
            "totalCrime": total_crime,
            "crimeBreakdown": crime_breakdown
        }
        
        logging.info(f"Calculated {total_crime} total crimes for {range_name}")
        logging.debug(f"Sample data for {range_name}:\n{json.dumps(result[range_name], indent=2)}")
    
    return result