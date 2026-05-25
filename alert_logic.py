# Alert Logic Module
"""
Implements threshold-based alerting logic for rainfall intensity.
"""

from datetime import datetime
from typing import Tuple

class AlertSystem:
    """Handles rainfall alert logic and logging."""
    
    def __init__(self, log_file: str = "alert_log.txt"):
        """
        Initialize the AlertSystem.
        
        Args:
            log_file (str): Path to the alert log file
        """
        self.log_file = log_file
        # Initialize log file with header if it doesn't exist
        self._initialize_log_file()
    
    def _initialize_log_file(self):
        """Create log file with header if it doesn't exist."""
        try:
            with open(self.log_file, "x", encoding="utf-8") as f:
                f.write("# Alert Log for Rainfall Monitoring System\n")
                f.write("# Format: TIMESTAMP - Rainfall: X.XX mm/h - Alert Level: COLOR\n")
                f.write("# This file is populated when alerts are triggered\n\n")
        except FileExistsError:
            # File already exists, which is fine
            pass
        except Exception as e:
            print(f"Warning: Could not initialize log file: {str(e)}")
    
    def check_alert(self, rainfall: float) -> str:
        """
        Determine alert level based on rainfall intensity.
        
        Args:
            rainfall (float): Rainfall intensity in mm/h
            
        Returns:
            str: Alert level ('Green', 'Yellow', or 'Red')
        """
        if rainfall < 10.0:
            return "Green"  # Normal
        elif rainfall < 20.0:
            return "Yellow"  # Moderate
        else:
            return "Red"  # Heavy - ALERT
    
    def should_trigger_alert(self, rainfall: float) -> bool:
        """
        Check if rainfall intensity triggers an alert (Red level).
        
        Args:
            rainfall (float): Rainfall intensity in mm/h
            
        Returns:
            bool: True if alert should be triggered, False otherwise
        """
        return rainfall >= 20.0
    
    def log_alert(self, rainfall: float, level: str) -> bool:
        """
        Log alert event to file with timestamp.
        
        Args:
            rainfall (float): Rainfall intensity that triggered alert
            level (str): Alert level
            
        Returns:
            bool: True if logging successful, False otherwise
        """
        try:
            with open(self.log_file, "a", encoding="utf-8") as log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"{timestamp} - Rainfall: {rainfall:.2f} mm/h - Alert Level: {level}\n")
            return True
        except Exception as e:
            print(f"Failed to write to log file: {str(e)}")
            return False
    
    def get_alert_description(self, level: str) -> str:
        """
        Get human-readable description for alert level.
        
        Args:
            level (str): Alert level ('Green', 'Yellow', or 'Red')
            
        Returns:
            str: Description of the alert level
        """
        descriptions = {
            "Green": "Normal Conditions",
            "Yellow": "Moderate Rainfall",
            "Red": "HEAVY RAINFALL ALERT!"
        }
        return descriptions.get(level, "Unknown Alert Level")
    
    def get_alert_color(self, level: str) -> str:
        """
        Get color associated with alert level for UI display.
        
        Args:
            level (str): Alert level ('Green', 'Yellow', or 'Red')
            
        Returns:
            str: Color name for UI
        """
        colors = {
            "Green": "green",
            "Yellow": "orange", 
            "Red": "red"
        }
        return colors.get(level, "gray")
    
    def read_recent_alerts(self, lines: int = 10) -> list:
        """
        Read recent alert entries from the log file.
        
        Args:
            lines (int): Number of recent lines to read
            
        Returns:
            list: List of recent alert entries
        """
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                all_lines = f.readlines()
                # Skip header lines (starting with #)
                data_lines = [line.strip() for line in all_lines if not line.startswith("#") and line.strip()]
                # Return the last 'lines' entries
                return data_lines[-lines:] if len(data_lines) >= lines else data_lines
        except FileNotFoundError:
            return ["Log file not found"]
        except Exception as e:
            return [f"Error reading log file: {str(e)}"]

# Example usage and testing
if __name__ == "__main__":
    # Test the alert system
    alert_system = AlertSystem()
    
    print("Testing Alert System")
    print("=" * 30)
    
    # Test different rainfall values
    test_values = [5.0, 9.9, 10.0, 15.0, 19.9, 20.0, 25.0, 50.0]
    
    for rainfall in test_values:
        level = alert_system.check_alert(rainfall)
        description = alert_system.get_alert_description(level)
        should_trigger = alert_system.should_trigger_alert(rainfall)
        
        print(f"Rainfall: {rainfall:5.1f} mm/h -> Level: {level:>5} ({description})")
        if should_trigger:
            print(f"  -> ALERT TRIGGERED (would log to file)")
            # Actually log one test alert for demonstration
            if rainfall == 25.0:  # Log only one test alert
                alert_system.log_alert(rainfall, level)
                print(f"  -> Test alert logged to {alert_system.log_file}")
        print()
    
    # Show recent alerts from log
    print("Recent alerts from log:")
    print("-" * 30)
    recent = alert_system.read_recent_alerts()
    for entry in recent:
        print(entry)