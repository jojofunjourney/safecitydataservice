# Safe City Walk

Safe City Walk is a FastAPI-based web application that analyzes and visualizes crime data for various cities.

## Project Structure

safe-city-walk/
├── api/
│ ├── controllers/
│ │ ├── crime_data_analysis_controller.py
│ │ └── upload_crime_data_controller.py
│ └── routes/
│ ├── crime_data_analysis_route.py
│ └── upload_crime_data_route.py
├── services/
│ ├── crime_data_analysis_service.py
│ └── upload_crime_data_service.py
├── util/
│ ├── fetch_crime_data.py
│ ├── gcs_util.py
│ ├── logger.py
│ ├── log.py
│ └── transform_crime_data.py
├── models/
│ └── crime_data_models.py
├── config.py
├── constants.py
├── main.py
├── requirements.txt
└── .gitignore

## Key Components

1. **API Controllers**: Handle incoming HTTP requests and responses.
   - `crime_data_analysis_controller.py`: Manages crime data analysis requests.
   - `upload_crime_data_controller.py`: Handles crime data upload requests.

2. **Services**: Contain the core business logic.
   - `crime_data_analysis_service.py`: Analyzes crime data using BigQuery.
   - `upload_crime_data_service.py`: Manages the upload of crime data to Google Cloud Storage.

3. **Utilities**: Provide helper functions and modules.
   - `fetch_crime_data.py`: Fetches crime data from various city APIs.
   - `gcs_util.py`: Utilities for interacting with Google Cloud Storage.
   - `logger.py` and `log.py`: Logging utilities.
   - `transform_crime_data.py`: Transforms raw crime data into a unified format.

4. **Models**: Define data structures and types.
   - `crime_data_models.py`: Contains Pydantic models for crime data.

5. **Configuration**: 
   - `config.py`: Contains configuration variables.
   - `constants.py`: Defines constant values used across the project.

6. **Main Application**: 
   - `main.py`: The entry point of the FastAPI application.

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/safe-city-walk.git
   cd safe-city-walk
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables (refer to `config.py` for required variables).

4. Run the application:
   ```
   uvicorn main:app --reload
   ```

## API Endpoints

- GET `/crime-data-analysis`: Analyze crime data for a specific city and time range.
  - Query parameters: 
    - `city`: City to analyze (e.g., NEW_YORK, LOS_ANGELES)
    - `time_range`: Time range for analysis (e.g., 6months, 1year)

- GET `/crime-data-analysis/coordinate`: Get coordinate-based crime data for a specific city and time range.
  - Query parameters: 
    - `city`: City to analyze
    - `time_range`: Time range for analysis

- POST `/upload-crime-data`: Upload crime data for a specific city and time range.
  - Request body:
    ```json
    {
      "city": "NEW_YORK",
      "time_range": "6months"
    }
    ```

## How It Works

1. The API is initialized in `main.py`.
2. Requests are routed through the appropriate controllers in `api/controllers/`.
3. Controllers call services to process the requests.
4. Services use utility functions from `util/` to fetch, transform, and analyze data.
5. Data is stored in and retrieved from Google Cloud Storage and BigQuery.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.