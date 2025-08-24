"""Enhanced multi-tool agent with real-time weather and global time support."""

import logging
from typing import Dict, Any, List, Optional
from google.adk.agents import Agent

# Import all services
try:
    from .config import Config
    from .services.weather import weather_service
    from .services.time_service import time_service
    from .services.utils import location_utils
except ImportError:
    from config import Config
    from services.weather import weather_service
    from services.time_service import time_service
    from services.utils import location_utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate configuration on import
Config.validate_config()

def get_weather(city: str, units: str = "metric") -> Dict[str, Any]:
    """Retrieves the current weather report for a specified city with real-time data.

    Args:
        city (str): The name of the city for which to retrieve the weather report.
        units (str): Temperature units - 'metric' (Celsius), 'imperial' (Fahrenheit), or 'kelvin'.

    Returns:
        dict: Status and weather report or error message.
    """
    # Validate inputs
    if not city or not city.strip():
        return {
            "status": "error",
            "error_message": "City name cannot be empty. Please provide a valid city name."
        }
    
    # Normalize units
    units = units.lower()
    if units not in ['metric', 'imperial', 'kelvin']:
        units = 'metric'  # Default to metric if invalid unit provided
    
    return weather_service.get_current_weather(city.strip(), units)


def get_weather_forecast(city: str, days: int = 3, units: str = "metric") -> Dict[str, Any]:
    """Get weather forecast for a specified city.

    Args:
        city (str): The name of the city for the forecast.
        days (int): Number of days for the forecast (1-5).
        units (str): Temperature units - 'metric', 'imperial', or 'kelvin'.

    Returns:
        dict: Status and forecast data or error message.
    """
    # Validate inputs
    if not city or not city.strip():
        return {
            "status": "error",
            "error_message": "City name cannot be empty. Please provide a valid city name."
        }
    
    # Validate and normalize days
    try:
        days = int(days)
        days = min(max(days, 1), 5)  # Ensure days is between 1 and 5
    except (ValueError, TypeError):
        days = 3  # Default to 3 days if invalid
    
    # Normalize units
    units = units.lower()
    if units not in ['metric', 'imperial', 'kelvin']:
        units = 'metric'  # Default to metric if invalid unit provided
    
    return weather_service.get_weather_forecast(city.strip(), units, days)


def get_current_time(city: str, format_type: str = "standard") -> Dict[str, Any]:
    """Returns the current time for any city in the world.

    Args:
        city (str): The name of the city for which to retrieve the current time.
        format_type (str): Format type - 'standard', 'detailed', or 'utc'.

    Returns:
        dict: Status and time information or error message.
    """
    # Validate inputs
    if not city or not city.strip():
        return {
            "status": "error",
            "error_message": "City name cannot be empty. Please provide a valid city name."
        }
    
    # Normalize format type
    format_type = format_type.lower()
    if format_type not in ['standard', 'detailed', 'utc']:
        format_type = 'standard'  # Default to standard if invalid format provided
    
    return time_service.get_current_time(city.strip(), format_type)


def get_time_difference(city1: str, city2: str) -> Dict[str, Any]:
    """Calculate the time difference between two cities.

    Args:
        city1 (str): First city name.
        city2 (str): Second city name.

    Returns:
        dict: Status and time difference information or error message.
    """
    # Validate inputs
    if not city1 or not city1.strip():
        return {
            "status": "error",
            "error_message": "First city name cannot be empty. Please provide valid city names."
        }
    
    if not city2 or not city2.strip():
        return {
            "status": "error",
            "error_message": "Second city name cannot be empty. Please provide valid city names."
        }
    
    if city1.strip().lower() == city2.strip().lower():
        return {
            "status": "success",
            "report": f"Both cities ({city1.strip().title()}) are the same, so there is no time difference.",
            "data": {
                "city1": city1.strip(),
                "city2": city2.strip(),
                "difference_hours": 0
            }
        }
    
    return time_service.get_time_difference(city1.strip(), city2.strip())


def get_world_clock(cities: List[str]) -> Dict[str, Any]:
    """Get current time for multiple cities (world clock).

    Args:
        cities (List[str]): List of city names.

    Returns:
        dict: Status and world clock information or error message.
    """
    # Validate inputs
    if not cities:
        return {
            "status": "error",
            "error_message": "Please provide a list of cities. Example: ['New York', 'London', 'Tokyo']"
        }
    
    # Clean and validate city names
    clean_cities = []
    for city in cities:
        if city and isinstance(city, str) and city.strip():
            clean_cities.append(city.strip())
    
    if not clean_cities:
        return {
            "status": "error",
            "error_message": "No valid city names provided. Please ensure city names are not empty."
        }
    
    # Limit to reasonable number of cities to avoid overwhelming output
    if len(clean_cities) > 10:
        clean_cities = clean_cities[:10]
        truncated_message = f"Limited to first 10 cities out of {len(cities)} provided."
    else:
        truncated_message = None
    
    result = time_service.get_world_clock(clean_cities)
    
    # Add truncation notice if applicable
    if truncated_message and result.get("status") == "success":
        result["report"] += f"\n\nNote: {truncated_message}"
    
    return result


def get_city_info(city: str) -> Dict[str, Any]:
    """Get comprehensive information about a city including coordinates and timezone.

    Args:
        city (str): The name of the city.

    Returns:
        dict: Status and city information or error message.
    """
    # Validate inputs
    if not city or not city.strip():
        return {
            "status": "error",
            "error_message": "City name cannot be empty. Please provide a valid city name."
        }
    
    info = location_utils.get_city_info(city.strip())
    
    if info["success"]:
        report = f"""Information for {city.title()}:
Coordinates: {info['latitude']:.4f}, {info['longitude']:.4f}
Timezone: {info['timezone']}
Full address: {info['full_address']}
Country: {info['country']}"""
        
        return {
            "status": "success",
            "report": report,
            "data": info
        }
    else:
        return {
            "status": "error",
            "error_message": info["error"]
        }


# Create the enhanced agent with comprehensive weather and time capabilities
root_agent = Agent(
    name="enhanced_weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Advanced agent that provides real-time weather data and time information for any city worldwide. "
        "Supports weather forecasts, time zone conversions, world clock, and city information lookup."
    ),
    instruction=(
        "You are a helpful and knowledgeable assistant with access to real-time weather data and comprehensive global time zone information. "
        "Your expertise covers weather conditions, forecasts, time zones, and geographical information for any city worldwide."
        
        "\n\n=== CORE CAPABILITIES ==="
        "\n• Real-time weather data from OpenWeatherMap API with fallback to demo data"
        "\n• Weather forecasts up to 5 days for any city"
        "\n• Current time and timezone information for any global location"
        "\n• Time zone conversions and differences between cities"
        "\n• World clock functionality for multiple cities"
        "\n• Comprehensive city information including coordinates and timezone details"
        
        "\n\n=== WEATHER HANDLING ==="
        "\n• When users ask for weather, use get_weather() for current conditions"
        "\n• For forecasts, use get_weather_forecast() and specify the number of days (1-5)"
        "\n• Support all temperature units: metric (Celsius), imperial (Fahrenheit), kelvin"
        "\n• If weather data fails, explain the issue and suggest checking city spelling"
        "\n• When API key is not configured, explain demo data limitations clearly"
        "\n• For ambiguous city names, suggest including country or state for clarity"
        
        "\n\n=== TIME HANDLING ==="
        "\n• Use get_current_time() for single city time queries"
        "\n• Support multiple format types: 'standard', 'detailed', or 'utc'"
        "\n• Use get_time_difference() to compare times between two cities"
        "\n• Use get_world_clock() for multiple cities simultaneously"
        "\n• Always specify the timezone in your responses"
        "\n• Handle daylight saving time transitions gracefully"
        "\n• For scheduling questions, provide times in multiple relevant zones"
        
        "\n\n=== CITY AND LOCATION HANDLING ==="
        "\n• Use get_city_info() for geographical details about locations"
        "\n• Handle various city name formats (with/without country, abbreviations)"
        "\n• For ambiguous names, ask for clarification (e.g., 'Paris, France' vs 'Paris, Texas')"
        "\n• Provide coordinates and timezone information when helpful"
        "\n• Handle historical city names and common misspellings gracefully"
        
        "\n\n=== ERROR HANDLING AND EDGE CASES ==="
        "\n• If a tool returns an error, explain the issue clearly to the user"
        "\n• For invalid city names, suggest alternatives or ask for clarification"
        "\n• When API limits are reached, explain the situation and suggest alternatives"
        "\n• Handle network timeouts by suggesting to try again later"
        "\n• For cities with multiple locations, ask for country/state specification"
        "\n• If coordinates are provided instead of city names, acknowledge but ask for city name"
        
        "\n\n=== USER INTERACTION GUIDELINES ==="
        "\n• Always be helpful, accurate, and conversational"
        "\n• Provide context for your responses (timezone, data source, etc.)"
        "\n• When data is unavailable, explain why and offer alternatives"
        "\n• For complex queries, break down information clearly"
        "\n• Offer related information that might be useful (e.g., when giving weather, mention if it's unusual for the season)"
        "\n• Use proper units and formats based on user preference or location"
        
        "\n\n=== SPECIAL SCENARIOS ==="
        "\n• For travel planning: provide weather and time info for multiple destinations"
        "\n• For scheduling: show times in multiple relevant zones"
        "\n• For emergency information: prioritize accuracy and clarity"
        "\n• For scientific queries: provide precise coordinates and UTC times when relevant"
        "\n• For historical questions: explain that current tools provide present data only"
        
        "\n\n=== DATA SOURCE TRANSPARENCY ==="
        "\n• Always mention when using demo data vs real-time data"
        "\n• Explain API key requirements for full functionality when relevant"
        "\n• Acknowledge data limitations and suggest setup instructions when needed"
        "\n• Be clear about data freshness and update frequency"
        
        "\nRemember: Your goal is to provide accurate, helpful, and contextually appropriate information while handling edge cases gracefully and maintaining a helpful, professional tone."
    ),
    tools=[
        get_weather,
        get_weather_forecast,
        get_current_time,
        get_time_difference,
        get_world_clock,
        get_city_info
    ],
)