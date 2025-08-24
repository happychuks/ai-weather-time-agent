# Enhanced Multi-Tool Agent

A robust Google AI agent that provides real-time weather data and comprehensive time information for any city worldwide.

## Features

### Weather Capabilities

- **Real-time weather data** from OpenWeatherMap API
- **Current weather conditions** with temperature, humidity, wind speed, pressure
- **Weather forecasts** up to 5 days
- **Multiple unit systems** (Celsius, Fahrenheit, Kelvin)
- **Fallback demo data** when API key is not configured

### Time Capabilities

- **Current time** for any city worldwide
- **Timezone detection** using coordinates
- **Time differences** between cities
- **World clock** for multiple cities
- **Multiple time formats** (standard, detailed, UTC)

### Location Services

- **City information** including coordinates and timezone
- **Geocoding** for any city worldwide
- **Comprehensive error handling** and validation

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get OpenWeatherMap API Key (Optional but Recommended)

1. Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your API key from the dashboard
3. Add it to your `.env` file:

```bash
# Create or edit .env file in the project directory
echo "OPENWEATHER_API_KEY=your_api_key_here" >> .env
```

**Alternative:** Set as environment variable:

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

**Note:** The agent automatically loads the API key from `.env` file using `python-dotenv`. Without an API key, it works using demo data for major cities, but real-time data requires the API key.

### 3. Usage

```python
from multi_tool_agent.agent import root_agent

# The agent is ready to use with all enhanced capabilities
```

## Available Tools

### Weather Tools

#### `get_weather(city, units="metric")`

Get current weather for any city.

- **city**: City name (e.g., "London", "New York", "Tokyo")
- **units**: "metric" (°C), "imperial" (°F), or "kelvin" (K)

#### `get_weather_forecast(city, days=3, units="metric")`

Get weather forecast for up to 5 days.

- **city**: City name
- **days**: Number of days (1-5)
- **units**: Temperature units

### Time Tools

#### `get_current_time(city, format_type="standard")`

Get current time for any city worldwide.

- **city**: City name
- **format_type**: "standard", "detailed", or "utc"

#### `get_time_difference(city1, city2)`

Calculate time difference between two cities.

- **city1**: First city name
- **city2**: Second city name

#### `get_world_clock(cities)`

Get current time for multiple cities.

- **cities**: List of city names

### Location Tools

#### `get_city_info(city)`

Get comprehensive city information.

- **city**: City name

## Example Usage

```python
# Get weather for Lagos
weather = get_weather("Lagos", "metric")
print(weather["report"])

# Get 5-day forecast for Lagos
forecast = get_weather_forecast("Lagos", days=5)
print(forecast["report"])

# Get current time in Lagos with detailed format
time_info = get_current_time("Lagos", "detailed")
print(time_info["report"])

# Compare time between New York and Lagos
time_diff = get_time_difference("New York", "Lagos")
print(time_diff["report"])

# World clock for multiple cities
world_time = get_world_clock(["New York", "London", "Lagos", "Nairobi"])
print(world_time["report"])

# Get city information
city_info = get_city_info("Abuja")
print(city_info["report"])
```

## Architecture

### Core Components

- **`agent.py`**: Main agent definition with enhanced tool functions
- **`config.py`**: Configuration management for API keys and settings
- **`weather.py`**: Weather service with OpenWeatherMap API integration
- **`time_service.py`**: Time service with global timezone support
- **`utils.py`**: Location utilities for geocoding and timezone detection

### Key Features

- **Robust error handling**: Graceful fallbacks and informative error messages
- **Global coverage**: Works with any city worldwide
- **Flexible formatting**: Multiple output formats for different use cases
- **Demo mode**: Works without API keys using sample data
- **Comprehensive logging**: Built-in logging for debugging and monitoring

## Error Handling

The agent provides graceful error handling:

- **Invalid city names**: Clear error messages with suggestions
- **API failures**: Fallback to cached or demo data when possible
- **Network issues**: Timeout handling and retry logic
- **Timezone issues**: Automatic timezone detection with fallbacks

## Dependencies

- **requests**: HTTP client for API calls
- **pytz**: Timezone handling
- **geopy**: Geocoding services
- **timezonefinder**: Timezone detection from coordinates
- **numpy**: Required by timezonefinder
- **python-dotenv**: Load environment variables from .env file
- **google.adk.agents**: Google AI agent framework

## Demo Cities (Available without API key)

When no API key is configured, demo weather data is available for:

- New York
- London
- Tokyo
- Paris
- Sydney

Time information works for any city worldwide regardless of API key status.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Author

Happy Felix Chukwuma - [GitHub](www.github.com/happychuks), [LinkedIn](www.linkedin.com/in/happyfelixchukwuma)
