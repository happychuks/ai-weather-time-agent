"""Weather service module for real-time weather data."""

import requests
import logging
from typing import Dict, Any, Optional

# Handle both relative and absolute imports
try:
    from ..config import Config
    from .utils import location_utils
except ImportError:
    from config import Config
    from services.utils import location_utils

# Set up logging
logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching real-time weather data from OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = Config.OPENWEATHER_BASE_URL
        self.has_api_key = bool(self.api_key)
    
    def _make_api_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make a request to the OpenWeatherMap API.
        
        Args:
            endpoint (str): API endpoint
            params (Dict[str, Any]): Request parameters
            
        Returns:
            Optional[Dict[str, Any]]: API response or None if failed
        """
        if not self.has_api_key:
            return None
            
        params['appid'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def get_current_weather(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Get current weather data for a city.
        
        Args:
            city (str): City name
            units (str): Temperature units (metric, imperial, kelvin)
            
        Returns:
            Dict[str, Any]: Weather data with status
        """
        if not self.has_api_key:
            return self._get_mock_weather(city)
        
        params = {
            'q': city,
            'units': units,
            'lang': Config.DEFAULT_LANGUAGE
        }
        
        data = self._make_api_request('weather', params)
        
        if not data:
            return {
                "status": "error",
                "error_message": f"Failed to fetch weather data for '{city}'. Please check the city name and try again."
            }
        
        # Check for API errors
        if data.get('cod') != 200:
            return {
                "status": "error",
                "error_message": data.get('message', f"Weather data not available for '{city}'")
            }
        
        return self._format_weather_response(data, city, units)
    
    def get_weather_forecast(self, city: str, units: str = "metric", days: int = 5) -> Dict[str, Any]:
        """
        Get weather forecast for a city.
        
        Args:
            city (str): City name
            units (str): Temperature units
            days (int): Number of days (max 5 for free tier)
            
        Returns:
            Dict[str, Any]: Forecast data with status
        """
        if not self.has_api_key:
            return {
                "status": "error",
                "error_message": "Weather forecast requires an API key. Please set OPENWEATHER_API_KEY environment variable to get forecasts, or use get_weather() for current conditions with demo data."
            }
        
        params = {
            'q': city,
            'units': units,
            'lang': Config.DEFAULT_LANGUAGE,
            'cnt': min(days * 8, 40)  # 8 forecasts per day, max 40 for free tier
        }
        
        data = self._make_api_request('forecast', params)
        
        if not data or data.get('cod') != '200':
            return {
                "status": "error",
                "error_message": f"Failed to fetch forecast data for '{city}'"
            }
        
        return self._format_forecast_response(data, city, units, days)
    
    def _format_weather_response(self, data: Dict[str, Any], city: str, units: str) -> Dict[str, Any]:
        """Format the weather API response into a readable format."""
        try:
            main = data['main']
            weather = data['weather'][0]
            wind = data.get('wind', {})
            
            temp_unit = self._get_temperature_unit(units)
            speed_unit = self._get_speed_unit(units)
            
            report = f"""Current weather in {city.title()}:
Temperature: {main['temp']:.1f}°{temp_unit} (feels like {main['feels_like']:.1f}°{temp_unit})
Condition: {weather['description'].title()}
Humidity: {main['humidity']}%
Wind: {wind.get('speed', 0):.1f} {speed_unit}"""
            
            if 'visibility' in data:
                report += f"\nVisibility: {data['visibility'] / 1000:.1f} km"
            
            if main.get('pressure'):
                report += f"\nPressure: {main['pressure']} hPa"
            
            return {
                "status": "success",
                "report": report,
                "data": {
                    "temperature": main['temp'],
                    "feels_like": main['feels_like'],
                    "condition": weather['description'],
                    "humidity": main['humidity'],
                    "wind_speed": wind.get('speed', 0),
                    "pressure": main.get('pressure'),
                    "units": units
                }
            }
        except (KeyError, IndexError) as e:
            logger.error(f"Error formatting weather response: {e}")
            return {
                "status": "error",
                "error_message": "Failed to parse weather data"
            }
    
    def _format_forecast_response(self, data: Dict[str, Any], city: str, units: str, days: int) -> Dict[str, Any]:
        """Format the forecast API response into a readable format."""
        try:
            forecasts = data['list'][:days * 8:8]  # Take one forecast per day
            temp_unit = self._get_temperature_unit(units)
            
            report = f"Weather forecast for {city.title()}:\n"
            
            for i, forecast in enumerate(forecasts):
                date = forecast['dt_txt'].split(' ')[0]
                temp = forecast['main']['temp']
                condition = forecast['weather'][0]['description']
                report += f"Day {i+1} ({date}): {temp:.1f}°{temp_unit}, {condition.title()}\n"
            
            return {
                "status": "success",
                "report": report.strip(),
                "data": {
                    "forecasts": forecasts,
                    "units": units
                }
            }
        except (KeyError, IndexError) as e:
            logger.error(f"Error formatting forecast response: {e}")
            return {
                "status": "error",
                "error_message": "Failed to parse forecast data"
            }
    
    def _get_temperature_unit(self, units: str) -> str:
        """Get temperature unit symbol based on units."""
        unit_map = {
            'metric': 'C',
            'imperial': 'F',
            'kelvin': 'K'
        }
        return unit_map.get(units, 'C')
    
    def _get_speed_unit(self, units: str) -> str:
        """Get wind speed unit based on units."""
        unit_map = {
            'metric': 'm/s',
            'imperial': 'mph',
            'kelvin': 'm/s'
        }
        return unit_map.get(units, 'm/s')
    
    def _get_mock_weather(self, city: str) -> Dict[str, Any]:
        """
        Provide mock weather data when API key is not available.
        
        Args:
            city (str): City name
            
        Returns:
            Dict[str, Any]: Mock weather data
        """
        # Simple mock data for demonstration
        mock_data = {
            "new york": {
                "temp": 22.5,
                "condition": "partly cloudy",
                "humidity": 65,
                "wind_speed": 3.2
            },
            "london": {
                "temp": 15.8,
                "condition": "overcast",
                "humidity": 78,
                "wind_speed": 2.1
            },
            "lagos": {
                "temp": 31.3,
                "condition": "sunny",
                "humidity": 55,
                "wind_speed": 1.8
            },
            "paris": {
                "temp": 18.7,
                "condition": "light rain",
                "humidity": 82,
                "wind_speed": 2.5
            },
            "sydney": {
                "temp": 24.1,
                "condition": "clear sky",
                "humidity": 60,
                "wind_speed": 4.1
            }
        }
        
        city_lower = city.lower()
        if city_lower in mock_data:
            data = mock_data[city_lower]
            report = f"""Current weather in {city.title()} (Demo Data):
Temperature: {data['temp']:.1f}°C
Condition: {data['condition'].title()}
Humidity: {data['humidity']}%
Wind: {data['wind_speed']:.1f} m/s
Note: This is demo data. Set OPENWEATHER_API_KEY for real-time data."""
            
            return {
                "status": "success",
                "report": report,
                "data": data
            }
        else:
            return {
                "status": "error",
                "error_message": f"Demo weather data not available for '{city}'. Supported cities: {', '.join(mock_data.keys()).title()}"
            }

# Global instance
weather_service = WeatherService()
