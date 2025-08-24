"""Enhanced Multi-Tool Agent Package

A robust Google AI agent that provides real-time weather data and comprehensive 
time information for any city worldwide.
"""

# Import modules without executing them immediately
from . import config
from . import services

# Only import the main agent and functions when needed
def get_agent():
    """Get the main agent instance."""
    from .agent import root_agent
    return root_agent

def get_functions():
    """Get all agent functions."""
    from .agent import (
        get_weather,
        get_weather_forecast,
        get_current_time,
        get_time_difference,
        get_world_clock,
        get_city_info
    )
    return {
        'get_weather': get_weather,
        'get_weather_forecast': get_weather_forecast,
        'get_current_time': get_current_time,
        'get_time_difference': get_time_difference,
        'get_world_clock': get_world_clock,
        'get_city_info': get_city_info
    }

__version__ = "2.0.0"
__author__ = "AI Engineering Study Group"
__description__ = "Enhanced multi-tool agent with real-time weather and global time support"

__all__ = [
    'config', 
    'services',
    'get_agent',
    'get_functions'
]