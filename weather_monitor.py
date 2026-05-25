# weather_monitor.py - Main application code for Rainfall Alert System
import requests
import streamlit as st
from datetime import datetime
import time

# Configuration
API_KEY = 'your_api_key_here'  # Replace with your OpenWeatherMap API key
CITY = 'Beijing'
ALERT_THRESHOLD = 20.0  # mm/h - threshold for heavy rainfall alert

def fetch_weather(city, api_key):
    """
    Fetch current weather data for a specified city using OpenWeatherMap API.
    
    Args:
        city (str): City name for weather data
        api_key (str): OpenWeatherMap API key
        
    Returns:
        dict: Weather data or None if error occurs
    """
    try:
        # AI-generated: API call implementation
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Extract rainfall intensity (if available)
            rainfall = data.get('rain', {}).get('1h', 0)  # Rainfall in last hour (mm/h)
            if rainfall is None:
                rainfall = 0
                
            weather_data = {
                'rainfall': rainfall,
                'temperature': data.get('main', {}).get('temp'),
                'humidity': data.get('main', {}).get('humidity'),
                'description': data.get('weather', [{}])[0].get('description'),
                'city': data.get('name'),
                'country': data.get('sys', {}).get('country'),
                'timestamp': datetime.fromtimestamp(data.get('dt', 0))
            }
            return weather_data
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch weather data: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def check_alert(rainfall):
    """
    Determine alert level based on rainfall intensity.
    
    Args:
        rainfall (float): Rainfall intensity in mm/h
        
    Returns:
        str: Alert level ('Green', 'Yellow', or 'Red')
    """
    # Your implementation: threshold logic
    if rainfall < 10.0:
        return "Green"  # Normal
    elif rainfall < 20.0:
        return "Yellow"  # Moderate
    else:
        return "Red"  # Heavy - ALERT

def log_alert(rainfall, level):
    """
    Log alert event to file with timestamp.
    
    Args:
        rainfall (float): Rainfall intensity that triggered alert
        level (str): Alert level
    """
    # Your implementation: logging
    try:
        with open("alert_log.txt", "a", encoding="utf-8") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - Rainfall: {rainfall:.2f} mm/h - Alert Level: {level}\n")
    except Exception as e:
        st.error(f"Failed to write to log file: {str(e)}")

def main():
    """Main Streamlit dashboard application."""
    # Streamlit dashboard
    st.title('Rainfall Monitor - ' + CITY)
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Auto-refresh every 5 minutes
    refresh_interval = 300  # 5 minutes in seconds
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = 0
    
    # Check if it's time to refresh
    if time.time() - st.session_state.last_refresh > refresh_interval:
        st.session_state.last_refresh = time.time()
        st.experimental_rerun()
    
    # Fetch weather data
    weather_data = fetch_weather(CITY, API_KEY)
    
    if weather_data:
        rainfall = weather_data['rainfall']
        alert_level = check_alert(rainfall)
        
        # Display current rainfall
        st.metric(
            label="Current Rainfall Intensity",
            value=f"{rainfall:.2f} mm/h",
            delta=None
        )
        
        # Display alert status with color coding
        if alert_level == "Green":
            st.success("🟢 Normal Conditions")
        elif alert_level == "Yellow":
            st.warning("🟡 Moderate Rainfall")
        else:  # Red alert
            st.error("🔴 HEAVY RAINFALL ALERT!")
            # Log the alert when threshold is reached
            log_alert(rainfall, alert_level)
            st.warning("⚠️ Alert has been logged!")
        
        # Display additional weather information
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Temperature:** {weather_data['temperature']:.1f}°C")
            st.info(f"**Humidity:** {weather_data['humidity']}%")
        with col2:
            st.info(f"**Condition:** {weather_data['description'].title()}")
            st.info(f"**Location:** {weather_data['city']}, {weather_data['country']}")
        
        # Historical data placeholder (if time permits)
        st.subheader("Rainfall Trends")
        st.line_chart([rainfall])  # Simple placeholder - would need historical data for real chart
        
    else:
        st.error("Unable to fetch weather data. Please check your API key and internet connection.")

if __name__ == "__main__":
    main()