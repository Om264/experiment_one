# API Integration Module
"""
Handles all interactions with the OpenWeatherMap API for weather data retrieval.
"""

import requests
from datetime import datetime
from typing import Dict, Optional

class WeatherAPI:
    """Handles OpenWeatherMap API interactions."""
    
    def __init__(self, api_key: str):
        """
        Initialize the WeatherAPI with an API key.
        
        Args:
            api_key (str): OpenWeatherMap API key
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def fetch_weather(self, city: str) -> Optional[Dict]:
        """
        Fetch current weather data for a specified city.
        
        Args:
            city (str): City name for weather data
            
        Returns:
            dict: Weather data containing rainfall, temperature, etc. or None if error
        """
        try:
            # Make API call
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # Get metric units directly
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # Handle HTTP errors
            if response.status_code != 200:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
            
            # Parse response
            data = response.json()
            
            # Extract rainfall intensity (if available)
            rainfall = data.get('rain', {}).get('1h', 0)  # Rainfall in last hour (mm/h)
            if rainfall is None:
                rainfall = 0
            
            # Extract other relevant weather data
            weather_data = {
                'rainfall': rainfall,
                'temperature': data.get('main', {}).get('temp'),
                'humidity': data.get('main', {}).get('humidity'),
                'pressure': data.get('main', {}).get('pressure'),
                'description': data.get('weather', [{}])[0].get('description', '').title(),
                'city': data.get('name'),
                'country': data.get('sys', {}).get('country'),
                'timestamp': datetime.fromtimestamp(data.get('dt', 0)),
                'sunrise': datetime.fromtimestamp(data.get('sys', {}).get('sunrise', 0)),
                'sunset': datetime.fromtimestamp(data.get('sys', {}).get('sunset', 0))
            }
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching weather data: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error in API integration: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test if the API connection is working.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Use a simple city for testing
            test_data = self.fetch_weather("London")
            return test_data is not None
        except:
            return False

# Example usage (for testing)
if __name__ == "__main__":
    # This would normally be imported and used with a real API key
    print("API Integration Module")
    print("To use: create WeatherAPI instance with your API key")
    print("Example: api = WeatherAPI('your_api_key')")
    print("         data = api.fetch_weather('Beijing')")