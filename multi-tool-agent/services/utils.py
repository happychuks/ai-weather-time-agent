"""Utility functions for the multi-tool agent."""

import pytz
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from timezonefinder import TimezoneFinder
from typing import Optional, Tuple, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocationUtils:
    """Utilities for handling location-based operations."""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="multi_tool_agent")
        self.tf = TimezoneFinder()
    
    def get_coordinates(self, city: str) -> Optional[Tuple[float, float]]:
        """
        Get latitude and longitude coordinates for a city.
        
        Args:
            city (str): City name
            
        Returns:
            Optional[Tuple[float, float]]: (latitude, longitude) or None if not found
        """
        try:
            location = self.geolocator.geocode(city, timeout=10)
            if location:
                return (location.latitude, location.longitude)
            return None
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            logger.error(f"Geocoding error for {city}: {e}")
            return None
    
    def get_timezone(self, city: str) -> Optional[str]:
        """
        Get timezone identifier for a city.
        
        Args:
            city (str): City name
            
        Returns:
            Optional[str]: Timezone identifier or None if not found
        """
        coordinates = self.get_coordinates(city)
        if coordinates:
            lat, lon = coordinates
            timezone_str = self.tf.timezone_at(lat=lat, lng=lon)
            return timezone_str
        return None
    
    def validate_timezone(self, timezone_str: str) -> bool:
        """
        Validate if a timezone string is valid.
        
        Args:
            timezone_str (str): Timezone identifier
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            pytz.timezone(timezone_str)
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False
    
    def get_city_info(self, city: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a city.
        
        Args:
            city (str): City name
            
        Returns:
            Dict[str, Any]: City information including coordinates, timezone, etc.
        """
        coordinates = self.get_coordinates(city)
        if not coordinates:
            return {
                "success": False,
                "error": f"Could not find location information for '{city}'"
            }
        
        lat, lon = coordinates
        timezone_str = self.tf.timezone_at(lat=lat, lng=lon)
        
        try:
            location = self.geolocator.geocode(city, timeout=10)
            address_parts = location.address.split(", ") if location else []
            
            return {
                "success": True,
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "timezone": timezone_str,
                "full_address": location.address if location else "",
                "country": address_parts[-1] if address_parts else "Unknown"
            }
        except Exception as e:
            return {
                "success": True,
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "timezone": timezone_str,
                "full_address": "",
                "country": "Unknown"
            }

# Global instance for reuse
location_utils = LocationUtils()
