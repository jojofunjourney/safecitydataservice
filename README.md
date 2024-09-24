### Folder and File Descriptions
```
project_root/
├── api/
│ ├── controllers/
│ │ └── load_crime_data_controller.py
│ └── routes/
│ └── load_crime_data_route.py
├── services/
│ └── load_crime_data_service.py
├── util/
│ ├── fetch_crime_data.py
│ └── transform_crime_data.py
├── models/
│ └── crime_data_models.py
├── config.py
├── constants.py
└── main.py
```


#### api/
Contains the API-related code, including controllers and routes.

- **controllers/**: Handles the logic for API endpoints.
  - `load_crime_data_controller.py`: Defines the endpoint for loading crime data.

- **routes/**: Manages the routing for the API.
  - `load_crime_data_route.py`: Sets up the router for the load crime data endpoint.

#### services/
Contains the business logic of the application.

- `load_crime_data_service.py`: Orchestrates the process of fetching, transforming, and loading crime data to GCS.

#### util/
Contains utility functions used across the application.

- `fetch_crime_data.py`: Handles fetching raw crime data from various city APIs.
- `transform_crime_data.py`: Transforms the raw crime data into a unified format.

#### models/
Contains data models used in the application.

- `crime_data_models.py`: Defines the data structures for crime data.

#### Root Directory Files

- `config.py`: Contains configuration settings for the application.
- `constants.py`: Stores constant values used throughout the application.
- `main.py`: The entry point of the application, sets up the FastAPI app.

## How It Works

1. The API is initialized in `main.py`.
2. When a request is made to load crime data, it's routed through `api/routes/load_crime_data_route.py`.
3. The request is then handled by `api/controllers/load_crime_data_controller.py`.
4. The controller calls `services/load_crime_data_service.py` to process the request.
5. The service uses utility functions from `util/` to fetch and transform the data.
6. Finally, the transformed data is loaded into Google Cloud Storage.

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your environment variables:
   ```
   SOCRATA_APP_TOKEN=your_socrata_app_token_here
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-credentials.json
   ```

3. Obtain a Google Cloud service account key:
   - Go to the Google Cloud Console (https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Firestore API for your project
   - Go to "IAM & Admin" > "Service Accounts"
   - Create a new service account or select an existing one
   - Generate a new JSON key and download it
   - Place the JSON key file in a secure location on your machine
   - Update the GOOGLE_APPLICATION_CREDENTIALS path in your .env file to point to this JSON key file

## Running the Application

To run the FastAPI application:
python main.py
This will start the server on `http://0.0.0.0:8000`. You can access the API documentation at `http://0.0.0.0:8000/docs`.

## API Documentation

The API provides the following endpoint:

- POST `/api/v1/load_crime_data`: Load crime data for a specific city and date range into Google Cloud Storage.

For detailed API documentation, please refer to the Swagger UI available at `http://0.0.0.0:8000/docs` when the server is running.
