import os
import requests


class WeatherTool:
    """Fetch current weather data using the OpenWeather API."""

    def __init__(self):
        self.url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = os.environ["OPENWEATHER_API_KEY"]

    def get_current_weather(self, location: str) -> dict:
        response = requests.get(
            self.url,
            params={
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            },
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

        return {
            "location": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "condition": data["weather"][0]["description"]
        }


if __name__ == "__main__":
    weather_tool = WeatherTool()

    weather = weather_tool.get_current_weather("Pune")
    print(weather)

# Basic Concepts:
#
# 1. API:
#    An API allows one application to communicate with another application
#    and exchange data.
#
# 2. OpenWeather API:
#    A weather service that provides current weather information and
#    forecasts through HTTP API endpoints.
#
# 3. API Key:
#    A secret credential used to authenticate our application with
#    the OpenWeather API.
#
# 4. requests Library:
#    A Python library used to send HTTP requests to external services.
#    Here, requests.get() sends a GET request to the OpenWeather API.
#
# 5. WeatherTool Class:
#    Encapsulates the logic for fetching and processing weather data.
#
# 6. Query Parameters:
#    The parameters "q", "appid", and "units" are sent with the request.
#    - q: Specifies the location, such as Pune.
#    - appid: Provides the OpenWeather API key.
#    - units: Specifies metric units, such as Celsius for temperature.
#
# 7. JSON Response:
#    The API returns weather data in JSON format.
#    response.json() converts that JSON response into a Python dictionary.
#
# 8. Error Handling:
#    response.raise_for_status() raises an exception if the HTTP response
#    indicates an unsuccessful request, such as an HTTP 401 or 404 error.
#
# Execution Flow:
#
# 1. Import the required libraries: os and requests.
#
# 2. Initialize WeatherTool and read the API key from the environment.
#
# 3. Call get_current_weather("Pune") to request current weather data.
#
# 4. Send an HTTP GET request to the OpenWeather API with the location,
#    API key, and metric unit parameters.
#
# 5. Check the HTTP response status and convert the JSON response
#    into a Python dictionary.
#
# 6. Extract the location, temperature, humidity, wind speed,
#    and weather condition from the response.
#
# 7. Return the extracted information as a Python dictionary.
#
# 8. Print the weather information.
#
# Overall Flow:
# Python Application
#     -> WeatherTool
#     -> HTTP GET Request
#     -> OpenWeather API
#     -> Weather Data in JSON
#     -> Python Dictionary
#     -> Display Weather Information
