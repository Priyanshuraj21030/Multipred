from datetime import datetime
import json

class UserSettings:
    def __init__(self, user_id):
        self.user_id = user_id
        self.settings = self.load_settings()
        
    def load_settings(self):
        # In production, this would load from database
        default_settings = {
            "notifications": {
                "email": True,
                "push": True,
                "sms": False,
                "reminder_time": "09:00",
                "types": ["medication", "appointments", "measurements"]
            },
            "privacy": {
                "data_sharing": False,
                "anonymous_analytics": True,
                "third_party_access": False
            },
            "display": {
                "theme": "dark",
                "language": "en",
                "units": "metric",
                "dashboard_widgets": ["bmi", "predictions", "reminders", "goals"]
            },
            "health_goals": {
                "target_bmi": 22,
                "daily_steps": 10000,
                "sleep_hours": 8,
                "water_intake": 8
            },
            "integrations": {
                "fitbit": False,
                "google_fit": False,
                "apple_health": False
            }
        }
        return default_settings
        
    def update_settings(self, category, setting, value):
        if category in self.settings and setting in self.settings[category]:
            self.settings[category][setting] = value
            self.save_settings()
            return True
        return False
        
    def save_settings(self):
        # In production, this would save to database
        pass
        
    def get_setting(self, category, setting):
        return self.settings.get(category, {}).get(setting)
        
    def get_all_settings(self):
        return self.settings

class UserPreferences:
    def __init__(self, user_id):
        self.user_id = user_id
        self.preferences = self.load_preferences()
        
    def load_preferences(self):
        default_preferences = {
            "dashboard_layout": [
                {"widget": "health_metrics", "position": 1},
                {"widget": "predictions", "position": 2},
                {"widget": "goals", "position": 3},
                {"widget": "reminders", "position": 4}
            ],
            "chart_preferences": {
                "default_view": "weekly",
                "chart_type": "line",
                "show_targets": True
            },
            "notification_preferences": {
                "frequency": "daily",
                "quiet_hours": {"start": "22:00", "end": "07:00"},
                "channels": ["email", "app"]
            }
        }
        return default_preferences
        
    def update_preference(self, category, preference, value):
        if category in self.preferences:
            self.preferences[category][preference] = value
            self.save_preferences()
            return True
        return False
        
    def save_preferences(self):
        # In production, this would save to database
        pass

class HealthGoals:
    def __init__(self, user_id):
        self.user_id = user_id
        self.goals = self.load_goals()
        
    def load_goals(self):
        default_goals = {
            "weight": {
                "target": 70,
                "deadline": "2024-12-31",
                "progress": 0
            },
            "bmi": {
                "target": 22,
                "deadline": "2024-12-31",
                "progress": 0
            },
            "activity": {
                "daily_steps": 10000,
                "weekly_exercise": 150,
                "progress": 0
            }
        }
        return default_goals
        
    def update_goal(self, category, goal_data):
        if category in self.goals:
            self.goals[category].update(goal_data)
            self.save_goals()
            return True
        return False
        
    def calculate_progress(self, category):
        # Calculate progress for specific goal
        pass
        
    def save_goals(self):
        # In production, this would save to database
        pass 