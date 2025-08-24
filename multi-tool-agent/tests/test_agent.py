#!/usr/bin/env python3
"""
Test script for the enhanced multi-tool agent.

This script demonstrates the new capabilities of the weather and time agent.
Run this script to test the functionality with or without an API key.
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import (
    get_weather,
    get_weather_forecast,
    get_current_time,
    get_time_difference,
    get_world_clock,
    get_city_info,
    root_agent
)

def print_separator(title=""):
    """Print a separator line with optional title."""
    print("\n" + "="*60)
    if title:
        print(f" {title} ")
        print("="*60)
    print()

def test_weather():
    """Test weather functionality."""
    print_separator("WEATHER TESTING")
    
    # Test current weather
    print("Testing current weather for London...")
    result = get_weather("London", "metric")
    print(f"Status: {result['status']}")
    print(f"Report: {result['report']}")
    
    print("\n" + "-"*40)
    
    # Test weather forecast
    print("Testing 3-day forecast for Lagos...")
    result = get_weather_forecast("Lagos", days=3, units="metric")
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Report: {result['report']}")
    else:
        print(f"Error: {result.get('error_message', 'Unknown error')}")

def test_time():
    """Test time functionality."""
    print_separator("TIME TESTING")
    
    # Test current time
    print("Testing current time for Lagos (detailed format)...")
    result = get_current_time("Lagos", "detailed")
    print(f"Status: {result['status']}")
    print(f"Report: {result['report']}")
    
    print("\n" + "-"*40)
    
    # Test time difference
    print("Testing time difference between Lagos and New York...")
    result = get_time_difference("Lagos", "New York")
    print(f"Status: {result['status']}")
    print(f"Report: {result['report']}")
    
    print("\n" + "-"*40)
    
    # Test world clock
    print("Testing world clock for multiple cities...")
    cities = ["New York", "London", "Lagos", "Nairobi", "Paris"]
    result = get_world_clock(cities)
    print(f"Status: {result['status']}")
    print(f"Report: {result['report']}")

def test_location():
    """Test location functionality."""
    print_separator("LOCATION TESTING")
    
    # Test city info
    print("Testing city information for Lagos...")
    result = get_city_info("Lagos")
    print(f"Status: {result['status']}")
    print(f"Report: {result['report']}")

def test_error_handling():
    """Test error handling with invalid inputs."""
    print_separator("ERROR HANDLING TESTING")
    
    # Test invalid city
    print("Testing with invalid city name...")
    result = get_weather("IyanaMortuary")
    print(f"Status: {result['status']}")
    print(f"Error: {result.get('error_message', 'No error message')}")
    
    print("\n" + "-"*40)
    
    # Test invalid time
    print("Testing time for invalid city...")
    result = get_current_time("IyanaMortuary")
    print(f"Status: {result['status']}")
    print(f"Error: {result.get('error_message', 'No error message')}")

def main():
    """Main test function."""
    print("Enhanced Multi-Tool Agent Testing")
    print("=" * 60)
    print("This script tests the enhanced weather and time agent capabilities.")
    print("The agent works with or without an OpenWeatherMap API key.")
    
    # Check if API key is configured
    from config import Config
    if Config.OPENWEATHER_API_KEY:
        print("OpenWeatherMap API key is configured - using real-time data")
    else:
        print("OpenWeatherMap API key not found - using demo data")
        print("   Set OPENWEATHER_API_KEY environment variable for real-time weather data")
    
    try:
        # Run all tests
        test_weather()
        test_time()
        test_location()
        test_error_handling()
        
        print_separator("AGENT INFORMATION")
        print(f"Agent Name: {root_agent.name}")
        print(f"Model: {root_agent.model}")
        print(f"Description: {root_agent.description}")
        print(f"Number of Tools: {len(root_agent.tools)}")
        print("Available Tools:")
        for i, tool in enumerate(root_agent.tools, 1):
            print(f"  {i}. {tool.__name__}")
        
        print_separator("TESTING COMPLETED")
        print("All tests completed successfully!")
        print("The enhanced multi-tool agent is ready to use.")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
