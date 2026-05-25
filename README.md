# Rainfall Alert System - Experiment 1

## Short-term Rainfall Forecasting & Alert System

This repository contains the implementation of a real-time rainfall monitoring system developed as part of the AI-Augmented Software Engineering course Experiment 1.

### Overview

The system integrates external weather APIs, implements threshold-based alerting logic, and displays results through a web dashboard built with Streamlit. It's designed for urban flood management applications.

### Features

- **Real-time Weather Data**: Fetches current rainfall data from OpenWeatherMap API
- **Threshold-based Alerting**: Three-level alert system (Green/Normal, Yellow/Moderate, Red/Heavy)
- **Event Logging**: Logs all alert events to a file with timestamps
- **Interactive Dashboard**: Streamlit-based UI displaying current conditions and alert status
- **Auto-refresh**: Automatically updates every 5 minutes
- **Error Handling**: Graceful handling of API and network errors
- **Modular Design**: Separate modules for API integration, alert logic, and dashboard components
- **Comprehensive Testing**: Scripts for validating functionality across different locations
- **Detailed Documentation**: Complete logs of AI interactions and development process

### Files

#### Core Application
- `weather_monitor.py`: Main application code containing API integration, alert logic, and Streamlit dashboard (monolithic version)
- `weather_monitor_modular.py`: Modular version using separate modules for better organization

#### Modules (in experiment_one_codes directory)
- `api_integration.py`: Handles all interactions with OpenWeatherMap API
- `alert_logic.py`: Implements threshold-based alerting logic and logging
- `dashboard.py`: Streamlit-based dashboard for displaying data and alerts
- `test_different_locations.py`: Script for testing system across multiple geographical locations

#### Supporting Files
- `alert_log.txt`: Log file that records all triggered alerts (initially empty)
- `prompt_log.md`: Detailed documentation of AI interactions during development
- `README.md`: This file
- `EXPERIMENT_SUMMARY.md`: Summary of experiment implementation
- `FINAL_SUMMARY.md`: Final summary of all files and organization
- `requirements.txt`: Python package dependencies

### Setup Instructions

1. **Prerequisites**:
   - Python 3.10+
   - OpenWeatherMap API key (free tier available at [openweathermap.org/api](https://openweathermap.org/api))
   - Required Python packages: `requests`, `pandas`, `streamlit`

2. **Installation**:
   ```bash
   pip install requests pandas streamlit
   ```

3. **Configuration**:
   - For monolithic version: Open `weather_monitor.py`
   - For modular version: Open `weather_monitor_modular.py`
   - Replace `'your_api_key_here'` with your actual OpenWeatherMap API key
   - Optionally change the `CITY` variable to monitor a different location

4. **Run the Application**:
   - Monolithic version:
     ```bash
     streamlit run weather_monitor.py
     ```
   - Modular version:
     ```bash
     streamlit run weather_monitor_modular.py
     ```

### Usage

1. Launch the application using one of the commands above
2. The dashboard will display:
   - Current rainfall intensity in mm/h
   - Color-coded alert status (Green/Yellow/Red)
   - Additional weather information (temperature, humidity, conditions, pressure)
   - Location information (city, country)
   - Sunrise/sunset times (when available)
   - Auto-refresh indicator
3. When rainfall reaches or exceeds 20 mm/h (Red alert):
   - A warning message will appear
   - The event will be logged to `alert_log.txt` with timestamp
   - A confirmation notification will show in the dashboard
4. To test with different locations:
   - Run `python test_different_locations.py` (after inserting your API key)

### Alert Levels

- **Green** (< 10 mm/h): Normal conditions
- **Yellow** (10-20 mm/h): Moderate rainfall
- **Red** (≥ 20 mm/h): Heavy rainfall - ALERT TRIGGERED

### Validation

To verify the system is working correctly:
1. Test with different locations by changing the `CITY` variable in the main files
2. Verify alert triggers at the correct threshold (20 mm/h)
3. Check that `alert_log.txt` contains properly formatted timestamp entries
4. Validate that rainfall values are physically reasonable for your location (typically 0-100 mm/h)
5. Use the `test_different_locations.py` script to validate across multiple geographical locations
6. Check that all modules work together correctly in both monolithic and modular versions

### Optional Extensions (Documented but Not Implemented)

- Multiple city monitoring with comparative dashboard
- Email/SMS notifications for alerts using Twilio or SMTP
- Rainfall prediction using historical trends and machine learning
- Map visualization with Folium showing rainfall distribution
- Historical data storage and analysis capabilities
- Mobile-responsive dashboard design
- User-configurable alert thresholds via UI
- Data export capabilities (CSV, JSON)

### Implementation Approaches

**Monolithic Approach** (`weather_monitor.py`):
- All functionality in a single file
- Good for simple applications and learning
- Easier to understand flow for beginners

**Modular Approach** (`weather_monitor_modular.py` + module files):
- Separation of concerns
- Better maintainability and testability
- Each module has single responsibility
- Easier to extend and modify individual components
- Reusable components for other projects

### Acknowledgments

This experiment was completed using AI-assisted development techniques, with AI helping to generate initial code structures and implementations that were then refined through human oversight and testing. The detailed AI interaction log in `prompt_log.md` documents the collaborative development process.

---
*Developed for AI-Augmented Software Engineering Course - Experiment 1*