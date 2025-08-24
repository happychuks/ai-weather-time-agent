"""Time service module for handling time queries across different cities."""

import datetime
import pytz
from typing import Dict, Any, Optional
import logging

try:
    from .utils import location_utils
except ImportError:
    from services.utils import location_utils

logger = logging.getLogger(__name__)

class TimeService:
    """Service for handling time-related queries for any city worldwide."""
    
    def __init__(self):
        self.location_utils = location_utils
    
    def get_current_time(self, city: str, format_type: str = "standard") -> Dict[str, Any]:
        """
        Get current time for any city in the world.
        
        Args:
            city (str): City name
            format_type (str): Format type - 'standard', 'detailed', or 'utc'
            
        Returns:
            Dict[str, Any]: Time information with status
        """
        # Get timezone for the city
        timezone_str = self.location_utils.get_timezone(city)
        
        if not timezone_str:
            return {
                "status": "error",
                "error_message": f"Could not determine timezone for '{city}'. Please check the city name and try again."
            }
        
        try:
            # Get timezone object
            tz = pytz.timezone(timezone_str)
            
            # Get current time in the timezone
            now = datetime.datetime.now(tz)
            utc_now = datetime.datetime.now(pytz.UTC)
            
            # Format based on type
            if format_type == "detailed":
                report = self._format_detailed_time(city, now, tz, utc_now)
            elif format_type == "utc":
                report = self._format_utc_time(city, now, utc_now)
            else:  # standard
                report = self._format_standard_time(city, now, tz)
            
            return {
                "status": "success",
                "report": report,
                "data": {
                    "city": city,
                    "timezone": timezone_str,
                    "local_time": now.isoformat(),
                    "utc_time": utc_now.isoformat(),
                    "formatted_time": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "day_of_week": now.strftime("%A"),
                    "utc_offset": now.strftime("%z")
                }
            }
            
        except pytz.exceptions.UnknownTimeZoneError:
            return {
                "status": "error",
                "error_message": f"Unknown timezone '{timezone_str}' for city '{city}'"
            }
        except Exception as e:
            logger.error(f"Error getting time for {city}: {e}")
            return {
                "status": "error",
                "error_message": f"Failed to get time information for '{city}'"
            }
    
    def get_time_difference(self, city1: str, city2: str) -> Dict[str, Any]:
        """
        Calculate time difference between two cities.
        
        Args:
            city1 (str): First city
            city2 (str): Second city
            
        Returns:
            Dict[str, Any]: Time difference information
        """
        # Get timezones for both cities
        tz1_str = self.location_utils.get_timezone(city1)
        tz2_str = self.location_utils.get_timezone(city2)
        
        if not tz1_str:
            return {
                "status": "error",
                "error_message": f"Could not determine timezone for '{city1}'"
            }
        
        if not tz2_str:
            return {
                "status": "error",
                "error_message": f"Could not determine timezone for '{city2}'"
            }
        
        try:
            tz1 = pytz.timezone(tz1_str)
            tz2 = pytz.timezone(tz2_str)
            
            # Get current time in both timezones
            now_utc = datetime.datetime.now(pytz.UTC)
            time1 = now_utc.astimezone(tz1)
            time2 = now_utc.astimezone(tz2)
            
            # Calculate difference
            offset1 = time1.utcoffset().total_seconds() / 3600
            offset2 = time2.utcoffset().total_seconds() / 3600
            difference = offset1 - offset2
            
            # Format the response
            if difference == 0:
                report = f"{city1.title()} and {city2.title()} are in the same time zone."
            else:
                ahead_city = city1.title() if difference > 0 else city2.title()
                behind_city = city2.title() if difference > 0 else city1.title()
                hours_diff = abs(difference)
                
                if hours_diff == int(hours_diff):
                    time_diff_str = f"{int(hours_diff)} hour{'s' if hours_diff != 1 else ''}"
                else:
                    hours = int(hours_diff)
                    minutes = int((hours_diff - hours) * 60)
                    time_diff_str = f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
                
                report = f"{ahead_city} is {time_diff_str} ahead of {behind_city}."
            
            report += f"\nCurrent time in {city1.title()}: {time1.strftime('%Y-%m-%d %H:%M:%S %Z')}"
            report += f"\nCurrent time in {city2.title()}: {time2.strftime('%Y-%m-%d %H:%M:%S %Z')}"
            
            return {
                "status": "success",
                "report": report,
                "data": {
                    "city1": city1,
                    "city2": city2,
                    "timezone1": tz1_str,
                    "timezone2": tz2_str,
                    "time1": time1.isoformat(),
                    "time2": time2.isoformat(),
                    "difference_hours": difference
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating time difference: {e}")
            return {
                "status": "error",
                "error_message": f"Failed to calculate time difference between '{city1}' and '{city2}'"
            }
    
    def get_world_clock(self, cities: list) -> Dict[str, Any]:
        """
        Get current time for multiple cities (world clock).
        
        Args:
            cities (list): List of city names
            
        Returns:
            Dict[str, Any]: World clock information
        """
        if not cities:
            return {
                "status": "error",
                "error_message": "Please provide a list of cities"
            }
        
        results = []
        errors = []
        
        for city in cities:
            time_info = self.get_current_time(city)
            if time_info["status"] == "success":
                data = time_info["data"]
                results.append({
                    "city": city.title(),
                    "time": data["formatted_time"],
                    "timezone": data["timezone"],
                    "day": data["day_of_week"]
                })
            else:
                errors.append(f"{city}: {time_info['error_message']}")
        
        if not results:
            return {
                "status": "error",
                "error_message": f"Could not get time for any cities. Errors: {'; '.join(errors)}"
            }
        
        # Format report
        report = "World Clock:\n"
        for result in results:
            report += f"{result['city']}: {result['time']} ({result['day']})\n"
        
        if errors:
            report += f"\nErrors: {'; '.join(errors)}"
        
        return {
            "status": "success",
            "report": report.strip(),
            "data": {
                "results": results,
                "errors": errors,
                "total_cities": len(cities),
                "successful_cities": len(results)
            }
        }
    
    def _format_standard_time(self, city: str, now: datetime.datetime, tz: pytz.BaseTzInfo) -> str:
        """Format time in standard format."""
        return f"The current time in {city.title()} is {now.strftime('%Y-%m-%d %H:%M:%S')} ({tz.zone})"
    
    def _format_detailed_time(self, city: str, now: datetime.datetime, tz: pytz.BaseTzInfo, utc_now: datetime.datetime) -> str:
        """Format time with detailed information."""
        utc_offset = now.strftime("%z")
        utc_offset_formatted = f"UTC{utc_offset[:3]}:{utc_offset[3:]}" if utc_offset else "UTC"
        
        return f"""Time information for {city.title()}:
Local time: {now.strftime('%A, %B %d, %Y at %H:%M:%S')}
Timezone: {tz.zone}
UTC offset: {utc_offset_formatted}
UTC time: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}"""
    
    def _format_utc_time(self, city: str, now: datetime.datetime, utc_now: datetime.datetime) -> str:
        """Format time with UTC comparison."""
        utc_offset = now.strftime("%z")
        return f"""Time in {city.title()}:
Local: {now.strftime('%Y-%m-%d %H:%M:%S')} ({utc_offset})
UTC: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}"""

# Global instance
time_service = TimeService()
