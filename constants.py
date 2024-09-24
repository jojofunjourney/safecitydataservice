from models.crime_data_models import CityDataset, CityDatasets

DATA_LIMIT = 10000

CITY_DATASETS: CityDatasets = CityDatasets(
    newYork=CityDataset(
        endpoint="data.cityofnewyork.us",
        identifier="5uac-w243",
        datasetUrl="https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243",
        apiEndpoint="https://data.cityofnewyork.us/resource/5uac-w243.json",
        query="$where=cmplnt_fr_dt >= '{start_date}T00:00:00' AND cmplnt_fr_dt <= '{end_date}T23:59:59'"
    ),
    seattle=CityDataset(
        endpoint="data.seattle.gov",
        identifier="tazs-3rd5",
        datasetUrl="https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5",
        apiEndpoint="https://data.seattle.gov/resource/tazs-3rd5.json",
        query="$where=offense_start_datetime >= '{start_date}T00:00:00' AND offense_start_datetime <= '{end_date}T23:59:59'"
    ),
    losAngeles=CityDataset(
        endpoint="data.lacity.org",
        identifier="2nrs-mtv8",
        datasetUrl="https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8",
        apiEndpoint="https://data.lacity.org/resource/2nrs-mtv8.json",
        query="$where=date_occ >= '{start_date}T00:00:00' AND date_occ <= '{end_date}T23:59:59'"
    ),
    chicago=CityDataset(
        endpoint="data.cityofchicago.org",
        identifier="ijzp-q8t2",
        datasetUrl="https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2",
        apiEndpoint="https://data.cityofchicago.org/resource/ijzp-q8t2.json",
        query="$where=date >= '{start_date}T00:00:00' AND date <= '{end_date}T23:59:59'"
    )
)