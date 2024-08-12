# Weather Microservice

This microservice provides endpoints for requesting weather data and checking the progress of requests. It interacts with the OpenWeather API to fetch weather information and stores it in a SQLite database.

## Available Endpoints

### 1. POST /user/register

**Purpose:** Generate a new user request ID for use with other endpoints.

**Request Body:**
- **None:** This endpoint does not require any parameters in the request body.
  
### 2. **POST /weather**

**Purpose:** Request weather data for a list of cities.

**Description:**

* Validates the user_request_id to ensure it exists in the database and is unique for the request.
* Reads city IDs from a CSV file and fetches weather data for these cities from the OpenWeather API.
* Stores the weather data in the database under the given user_request_id.

**Request Body:**

```json
{
  "user_request_id": "string"  // Unique identifier for the request
}
```

### 3. GET /weather/progress

**Purpose:** Retrieve the progress of a specific weather request.

**Description:**

* Retrieves the progress of a weather data request based on the provided `user_request_id`.
* The response includes the percentage of cities for which weather data has been collected.
* If the `user_request_id` is missing, invalid, or does not exist, appropriate error messages are returned.

**Request Body:**

```json
{
  "user_request_id": "string"  // Unique identifier for the request
}
```
