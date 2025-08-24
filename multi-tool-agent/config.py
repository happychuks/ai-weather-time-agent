"""Configuration settings for the multi-tool agent."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Find the .env file relative to this config.py file
config_dir = Path(__file__).parent
env_file = config_dir / '.env'

# Load environment variables from .env file
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()

class Config:
    """Configuration class for API keys and settings."""
    
    # OpenWeatherMap API key - Get a free key from https://openweathermap.org/api
    OPENWEATHER_API_KEY: Optional[str] = os.getenv('OPENWEATHER_API_KEY')
    
    # OpenWeatherMap API base URL
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    # Default settings
    DEFAULT_UNITS = "metric"  # metric, imperial, or kelvin
    DEFAULT_LANGUAGE = "en"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.OPENWEATHER_API_KEY:
            print("Warning: OPENWEATHER_API_KEY not found in environment variables or .env file.")
            print("To get real-time weather data, please:")
            print("1. Sign up for a free API key at https://openweathermap.org/api")
            print("2. Add OPENWEATHER_API_KEY=your_api_key to your .env file")
            print("   or set the environment variable: export OPENWEATHER_API_KEY='your_api_key'")
            return False
        else:
            print(f"OpenWeatherMap API key loaded successfully from .env file")
            return True
