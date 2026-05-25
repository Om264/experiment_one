# Test Script: Different Locations Rainfall Comparison
"""
This script tests the rainfall monitoring system with different locations
to compare rainfall values and verify the system works across various geographies.
"""

import requests
import time

def fetch_weather_for_location(city, api_key):
    """
    Fetch weather data for a specific location.
    
    Args:
        city (str): City name
        api_key (str): OpenWeatherMap API key
        
    Returns:
        dict: Weather data or None if error
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            rainfall = data.get('rain', {}).get('1h', 0)
            if rainfall is None:
                rainfall = 0
                
            return {
                'city': data.get('name'),
                'country': data.get('sys', {}).get('country'),
                'rainfall': rainfall,
                'temperature': data.get('main', {}).get('temp'),
                'humidity': data.get('main', {}).get('humidity'),
                'description': data.get('weather', [{}])[0].get('description')
            }
        else:
            print(f"Error fetching data for {city}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception fetching data for {city}: {str(e)}")
        return None

def test_locations(api_key, locations=None):
    """
    Test rainfall monitoring with different locations.
    
    Args:
        api_key (str): OpenWeatherMap API key
        locations (list): List of city names to test
    """
    if locations is None:
        # Default test locations representing different climate zones
        locations = [
            "Beijing",      # Original test location
            "London",       # Temperate maritime
            "Sydney",       # Temperate (Southern Hemisphere)
            "Cairo",        # Arid desert
            "Singapore",    # Tropical rainforest
            "Rio de Janeiro", # Tropical savanna
            "Moscow",       # Continental
            "Toronto"       # Cold continental
        ]
    
    print("Testing rainfall monitoring across different locations...")
    print("=" * 60)
    
    results = []
    for city in locations:
        print(f"\nTesting {city}...")
        weather_data = fetch_weather_for_location(city, api_key)
        
        if weather_data:
            results.append(weather_data)
            print(f"  Location: {weather_data['city']}, {weather_data['country']}")
            print(f"  Rainfall: {weather_data['rainfall']:.2f} mm/h")
            print(f"  Temperature: {weather_data['temperature']:.1f}°C")
            print(f"  Humidity: {weather_data['humidity']}%")
            print(f"  Conditions: {weather_data['description']}")
        else:
            print(f"  Failed to retrieve data for {city}")
        
        # Small delay to respect API rate limits
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Locations tested: {len([r for r in results if r is not None])}/{len(locations)}")
    
    if results:
        rainfalls = [r['rainfall'] for r in results if r is not None]
        print(f"Rainfall range: {min(rainfalls):.2f} - {max(rainfalls):.2f} mm/h")
        print(f"Average rainfall: {sum(rainfalls)/len(rainfalls):.2f} mm/h")
        
        # Check for reasonable values (0-100 mm/h is typical range for extreme events)
        unreasonable = [r for r in results if r and (r['rainfall'] < 0 or r['rainfall'] > 100)]
        if unreasonable:
            print(f"WARNING: {len(unreasonable)} locations reported unreasonable rainfall values (>100 mm/h or <0)")
        else:
            print("All rainfall values within reasonable range (0-100 mm/h)")
    
    return results

if __name__ == "__main__":
    # For testing, you would insert your API key here
    # In practice, this would be imported from config or passed as argument
    API_KEY = "your_api_key_here"  # Replace with actual key for testing
    
    if API_KEY == "your_api_key_here":
        print("Please insert your OpenWeatherMap API key to run the tests")
        print("Edit this file and replace 'your_api_key_here' with your actual API key")
    else:
        test_locations(API_KEY)