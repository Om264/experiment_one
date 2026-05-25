# Weather Monitor - Modular Version
"""
Main application that integrates all modules for the rainfall monitoring system.
This version uses separate modules for API integration, alert logic, and dashboard.
"""

import streamlit as st
from api_integration import WeatherAPI
from alert_logic import AlertSystem
from dashboard import RainfallDashboard

def main():
    """Main application function."""
    # Configuration
    API_KEY = 'your_api_key_here'  # Replace with your OpenWeatherMap API key
    CITY = 'Beijing'
    
    # Initialize modules
    weather_api = WeatherAPI(API_KEY)
    alert_system = AlertSystem()
    dashboard = RainfallDashboard(CITY)
    
    # Set page config
    st.set_page_config(
        page_title="Rainfall Monitor",
        page_icon="🌧️",
        layout="centered"
    )
    
    # Fetch weather data
    weather_data = weather_api.fetch_weather(CITY)
    
    # Render dashboard with weather data
    dashboard.render_dashboard(weather_data)
    
    # If we have weather data, check for alerts and log if necessary
    if weather_data:
        rainfall = weather_data.get('rainfall', 0)
        alert_level = alert_system.check_alert(rainfall)
        
        # Log alert if threshold is reached
        if alert_system.should_trigger_alert(rainfall):
            if alert_system.log_alert(rainfall, alert_level):
                # Show success message only once per session to avoid spamming
                if 'alert_logged' not in st.session_state:
                    st.session_state.alert_logged = True
                    st.success("⚠️ Alert has been logged!")

if __name__ == "__main__":
    main()