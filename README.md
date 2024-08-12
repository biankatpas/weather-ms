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
## Running the Project

Follow these steps to run the Weather Microservice using Docker:

### 1. Prerequisites

Before starting the project, ensure you have the following:

- **Docker**: Make sure Docker is installed on your machine. You can download it from [Docker's official website](https://www.docker.com/get-started).
- **OpenWeather API Key**: Register for an API key from OpenWeather at [OpenWeather API](https://openweathermap.org/api). 

### 2. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

Replace `<repository-url>` with the URL of your repository and `<repository-directory>` with the name of the directory created by the clone command.

### 3. Configure Environment Variables

The project uses a .env file as a base, which should be configured based on example.env.

Make sure to replace the placeholder in the .env file with your actual OpenWeather API key.

To run the Weather Microservice project using Docker, follow these steps:

### 4. Start the Docker Container

   Navigate to the root directory of the project and run the following command:

   ```bash
   docker-compose up --build
   ```
### 5.Use Postman to Test Endpoints

Open Postman and use the following endpoints:

* POST /user/register: Generates a new user_request_id.
* POST /weather: Requests weather data for a list of cities.
* GET /weather/progress: Retrieves the progress of a specific weather request.

Ensure that you include the correct `user_request_id` in the request body when using the `/weather` and `/weather/progress` endpoints.

Note: If the `.env` file is not correctly configured or the Docker container is not running, the endpoints will not be accessible.

## Running Tests

Unit tests are currently under development. Once available, they will be located in the `app/tests` directory of the project. Please check back later for updates on how to run and use the test suite.

