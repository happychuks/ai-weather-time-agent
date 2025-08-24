"""Enhanced Multi-Tool Agent Package

A robust Google AI agent that provides real-time weather data and comprehensive 
time information for any city worldwide.
"""

from . import agent
from . import config
from . import weather
from . import time_service
from . import utils

# Import the main agent for easy access
from .agent import root_agent

# Import main functions for direct use
from .agent import (
    get_weather,
    get_weather_forecast,
    get_current_time,
    get_time_difference,
    get_world_clock,
    get_city_info
)

__version__ = "2.0.0"
__author__ = "AI Engineering Study Group"
__description__ = "Enhanced multi-tool agent with real-time weather and global time support"

__all__ = [
    'agent',
    'config', 
    'weather',
    'time_service',
    'utils',
    'root_agent',
    'get_weather',
    'get_weather_forecast', 
    'get_current_time',
    'get_time_difference',
    'get_world_clock',
    'get_city_info'
]