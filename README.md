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

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/happychuks/ai-weather-time-agent.git
cd ai-weather-time-agent
```

### 2. Set Up Python Environment

```bash
# Create a virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd multi-tool-agent
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file and add your API keys
# Required: OPENWEATHER_API_KEY (get from https://openweathermap.org/api)
# Required: GOOGLE_API_KEY (get from https://makersuite.google.com/app/apikey)
```

### 5. Run the Agent

#### Option A: Google ADK Web Interface (Recommended)

```bash
# Navigate to the parent directory
cd ..

# Start the ADK web server
adk web
```

Then open http://localhost:8000 in your browser to interact with the agent.

#### Option B: Direct Python Usage

```bash
# From the multi-tool-agent directory
cd multi-tool-agent

# Test the agent
python test_agent.py

# Or use in your own Python script
python -c "
from agent import root_agent
from weather import weather_service

# Test weather function
result = weather_service.get_current_weather('London')
print(result)
"
```

## Setup

## Detailed Configuration

### 1. API Keys Setup

#### Google AI API Key (Required)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new project or select existing one
3. Generate an API key
4. Add to your `.env` file:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

#### OpenWeatherMap API Key (Optional but Recommended)

1. Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your API key from the dashboard
3. Add it to your `.env` file:

```bash
OPENWEATHER_API_KEY=your_api_key_here
```

### 2. Environment File Configuration

Create a `.env` file in the `multi-tool-agent` directory:

```bash
# Required for Google AI
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_google_api_key_here

# Required for real-time weather data
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Optional configurations
WEATHER_DEFAULT_UNITS=metric
WEATHER_DEFAULT_LANG=en
REQUEST_TIMEOUT=10
```

### 3. Verify Installation

```bash
# Test that everything is working
cd multi-tool-agent
python -c "
from agent import root_agent
print('✓ Agent loaded successfully!')
print(f'✓ Available functions: {len(root_agent.tools)}')
"
```

### 4. Running Tests

```bash
# Run the comprehensive test suite
cd multi-tool-agent
python test_agent.py
```

## Usage

### Using with Google ADK Web Interface

This is the recommended way to interact with the agent:

```bash
# From the project root directory
cd ai-weather-time-agent
adk web
```

Open <http://localhost:8000> in your browser and start chatting with the agent.

### Direct Python Usage

```python
# Add the multi-tool-agent directory to your Python path
import sys
sys.path.append('./multi-tool-agent')

from agent import root_agent

# The agent is ready to use with all enhanced capabilities
# You can also import individual services:
from weather import weather_service
from time_service import time_service
```

### Programmatic Usage

```python
# Import specific functions
from multi_tool_agent.agent import (
    get_weather,
    get_weather_forecast,
    get_current_time,
    get_time_difference,
    get_world_clock,
    get_city_info
)

# Use directly
weather_data = get_weather("London")
time_data = get_current_time("Tokyo")
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

## Project Structure

```
ai-weather-time-agent/               # Repository root
├── README.md                        # This file
├── .gitignore                      # Git ignore rules
└── multi-tool-agent/               # Agent implementation
    ├── .env.example                # Environment template
    ├── .gitignore                  # Agent-specific ignores
    ├── .vscode/                    # VS Code settings
    │   └── settings.json
    ├── __init__.py                 # Package initialization
    ├── agent.py                    # Main agent with 6 functions
    ├── config.py                   # Configuration management
    ├── weather.py                  # Weather service
    ├── time_service.py             # Time service
    ├── utils.py                    # Location utilities
    ├── requirements.txt            # Python dependencies
    └── test_agent.py              # Test suite
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

## Troubleshooting

### Common Issues

#### 1. "Module not found" errors

```bash
# Make sure you're in the right directory
cd ai-weather-time-agent/multi-tool-agent

# Check if all dependencies are installed
pip install -r requirements.txt

# For programmatic usage, ensure proper path setup
import sys
sys.path.append('./multi-tool-agent')
```

#### 2. API key not working

```bash
# Verify your .env file exists and has the correct format
cat multi-tool-agent/.env

# Test API key directly
curl "http://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
```

#### 3. ADK web server not starting

```bash
# Make sure you're in the project root directory
cd ai-weather-time-agent

# Check if port 8000 is available
lsof -i :8000

# Install Google ADK if missing
pip install google-adk-agents
```

#### 4. Weather data not loading

- Without `OPENWEATHER_API_KEY`: Agent uses demo data for 5 major cities
- Check API key validity and usage limits
- Verify internet connectivity

### Getting Help

- Check the [Issues](https://github.com/happychuks/ai-weather-time-agent/issues) page
- Review the example usage in `test_agent.py`
- Ensure all environment variables are properly set

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

**Happy Felix Chukwuma**

[![GitHub](https://img.shields.io/badge/GitHub-happychuks-blue?style=flat&logo=github)](https://github.com/happychuks)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Happy%20Felix%20Chukwuma-blue?style=flat&logo=linkedin)](https://linkedin.com/in/happyfelixchukwuma)

- 🐙 **GitHub**: [github.com/happychuks](https://github.com/happychuks)
- 💼 **LinkedIn**: [linkedin.com/in/happyfelixchukwuma](https://linkedin.com/in/happyfelixchukwuma)
- 📧 **Email**: [happychukwuma@gmail.com](mailto:happychukwuma@gmail.com)

> **Note**: Right-click on the links above and select "Open in new tab" to keep this page open while viewing my profiles.

Feel free to reach out for questions, contributions, or collaboration opportunities!
