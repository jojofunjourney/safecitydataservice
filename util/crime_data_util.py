from typing import List, Dict, Type
from models.crime_data_models import UnifiedCrimeData, NewYorkCrimeData, LosAngelesCrimeData, SeattleCrimeData, ChicagoCrimeData, CITY_DATA_MODELS, CITIES
from collections import defaultdict
city_dataclass_map: Dict[CITIES, Type[CITY_DATA_MODELS]] = {
    CITIES.NEW_YORK: NewYorkCrimeData,
    CITIES.LOS_ANGELES: LosAngelesCrimeData,
    CITIES.SEATTLE: SeattleCrimeData,
    CITIES.CHICAGO: ChicagoCrimeData
}

def transform_crime_data(city: CITIES, data: List[CITY_DATA_MODELS]) -> List[UnifiedCrimeData]:
    try:
        
        city_dataclass = city_dataclass_map[city]
        transformed_data: List[UnifiedCrimeData] = [
            city_dataclass(**record).transform() for record in data
        ]
        
        print(f"Transformed {len(transformed_data)} rows for {city}")
        print(f"First 5 items in transformed data: {transformed_data[:5]}")
        
        return transformed_data
    except Exception as e:
        print(f"Error transforming data for {city}: {e}")
        raise
    
def count_crimes_by_coordinate(data: List[UnifiedCrimeData]) -> dict:
    crime_count = {}
    for record in data:
        coordinate = (record.latitude, record.longitude)
        if coordinate not in crime_count:
            crime_count[coordinate] = 0
        crime_count[coordinate] += 1
        
    return crime_count