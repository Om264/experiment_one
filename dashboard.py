# Dashboard Module
"""
Streamlit-based dashboard for displaying rainfall data and alerts.
"""

import streamlit as st
from datetime import datetime
import time
from typing import Dict, Optional

class RainfallDashboard:
    """Handles the Streamlit dashboard for rainfall monitoring."""
    
    def __init__(self, city: str = "Beijing"):
        """
        Initialize the dashboard.
        
        Args:
            city (str): City name to display in title
        """
        self.city = city
        self.refresh_interval = 300  # 5 minutes in seconds
    
    def set_city(self, city: str):
        """Update the city for display."""
        self.city = city
    
    def display_header(self):
        """Display the dashboard header."""
        st.title(f'Rainfall Monitor - {self.city}')
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def display_rainfall_metric(self, rainfall: float):
        """
        Display current rainfall as a large metric.
        
        Args:
            rainfall (float): Rainfall intensity in mm/h
        """
        st.metric(
            label="Current Rainfall Intensity",
            value=f"{rainfall:.2f} mm/h",
            delta=None
        )
    
    def display_alert_status(self, alert_level: str, rainfall: float):
        """
        Display alert status with color coding.
        
        Args:
            alert_level (str): Alert level ('Green', 'Yellow', or 'Red')
            rainfall (float): Current rainfall intensity
        """
        if alert_level == "Green":
            st.success("🟢 Normal Conditions")
        elif alert_level == "Yellow":
            st.warning("🟡 Moderate Rainfall")
        else:  # Red alert
            st.error("🔴 HEAVY RAINFALL ALERT!")
            if rainfall >= 20.0:
                st.warning("⚠️ Alert has been triggered and logged!")
    
    def display_weather_details(self, weather_data: Dict):
        """
        Display additional weather information.
        
        Args:
            weather_data (dict): Weather data from API
        """
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Temperature:** {weather_data.get('temperature', 0):.1f}°C")
            st.info(f"**Humidity:** {weather_data.get('humidity', 0)}%")
            st.info(f"**Pressure:** {weather_data.get('pressure', 0)} hPa")
        
        with col2:
            st.info(f"**Condition:** {weather_data.get('description', 'N/A')}")
            st.info(f"**Location:** {weather_data.get('city', 'N/A')}, {weather_data.get('country', 'N/A')}")
            
            # Display sunrise/sunset times if available
            if 'sunrise' in weather_data and weather_data['sunrise']:
                sunrise_time = weather_data['sunrise'].strftime("%H:%M")
                st.info(f"**Sunrise:** {sunrise_time}")
            if 'sunset' in weather_data and weather_data['sunset']:
                sunset_time = weather_data['sunset'].strftime("%H:%M")
                st.info(f"**Sunset:** {sunset_time}")
    
    def display_historical_chart(self, rainfall_values: list = None):
        """
        Display historical rainfall chart (placeholder implementation).
        
        Args:
            rainfall_values (list): List of historical rainfall values
        """
        st.subheader("Rainfall Trends")
        
        if rainfall_values and len(rainfall_values) > 1:
            # In a real implementation, this would show actual historical data
            st.line_chart(rainfall_values)
        else:
            # Placeholder - would need actual historical data collection
            st.line_chart([0])  # Simple placeholder
            st.caption("*Historical data chart - requires data collection over time*")
    
    def handle_auto_refresh(self):
        """Handle automatic refresh of the dashboard."""
        # Initialize last_refresh in session state if not present
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = 0
        
        # Check if it's time to refresh
        current_time = time.time()
        if current_time - st.session_state.last_refresh > self.refresh_interval:
            st.session_state.last_refresh = current_time
            st.experimental_rerun()
    
    def display_error_message(self, message: str):
        """
        Display error message to user.
        
        Args:
            message (str): Error message to display
        """
        st.error(f"Unable to fetch weather data: {message}")
        st.info("Please check your API key and internet connection.")
    
    def render_dashboard(self, weather_data: Optional[Dict] = None):
        """
        Render the complete dashboard.
        
        Args:
            weather_data (dict): Weather data from API, or None if unavailable
        """
        # Handle auto-refresh
        self.handle_auto_refresh()
        
        # Display header
        self.display_header()
        
        if weather_data:
            # Extract data
            rainfall = weather_data.get('rainfall', 0)
            
            # Determine alert level
            # Note: In a real implementation, this would come from AlertSystem
            if rainfall < 10.0:
                alert_level = "Green"
            elif rainfall < 20.0:
                alert_level = "Yellow"
            else:
                alert_level = "Red"
            
            # Display components
            self.display_rainfall_metric(rainfall)
            self.display_alert_status(alert_level, rainfall)
            self.display_weather_details(weather_data)
            self.display_historical_chart()
        else:
            # Display error state
            self.display_error_message("Unable to fetch weather data")
            
            # Still show header and allow manual refresh
            if st.button("Refresh Data"):
                st.experimental_rerun()

# Example usage (for testing outside Streamlit context)
if __name__ == "__main__":
    print("Dashboard Module")
    print("This module is designed to be used with Streamlit")
    print("Example usage in Streamlit app:")
    print("""
    import streamlit as st
    from dashboard import RainfallDashboard
    
    # Initialize dashboard
    dashboard = RainfallDashboard("Beijing")
    
    # Get weather data (from your API module)
    # weather_data = api.fetch_weather("Beijing")
    
    # Render dashboard
    # dashboard.render_dashboard(weather_data)
    """)