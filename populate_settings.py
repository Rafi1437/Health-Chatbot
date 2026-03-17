"""
Populate settings table with default values
"""

import sqlite3
import os

def populate_settings():
    """Populate settings table with default values"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Clear existing settings
        cursor.execute('DELETE FROM settings')
        
        # Insert default settings
        default_settings = [
            ('app_name', 'Senior Healthcare App', 'text', 'Application name'),
            ('medical_disclaimer', 'This chatbot provides general health information and does not replace professional medical advice. Always consult with qualified healthcare providers for medical concerns.', 'textarea', 'Medical disclaimer message'),
            ('mental_health_enabled', '1', 'boolean', 'Enable mental health module'),
            ('chatbot_enabled', '1', 'boolean', 'Enable chatbot module'),
            ('hydration_enabled', '1', 'boolean', 'Enable hydration module'),
            ('health_tips', 'Drink a glass of water when you wake up to start your day hydrated.|Take a short walk after meals to aid digestion.|Practice gratitude by thinking of 3 things you are thankful for.', 'textarea', 'Daily health tips (one per line)'),
            ('reminder_messages', 'Time for your mental health check-in!|Don\'t forget to drink water throughout the day.|How are you feeling today?', 'textarea', 'Reminder messages (one per line)'),
            ('min_water_intake', '2000', 'number', 'Minimum daily water intake in ml'),
            ('session_timeout', '30', 'number', 'Session timeout in minutes'),
        ]
        
        for setting_key, setting_value, setting_type, description in default_settings:
            cursor.execute('''
                INSERT INTO settings (setting_key, setting_value, setting_type, description)
                VALUES (?, ?, ?, ?)
            ''', (setting_key, setting_value, setting_type, description))
        
        conn.commit()
        
        # Verify settings
        cursor.execute('SELECT setting_key, setting_value FROM settings')
        settings = cursor.fetchall()
        
        print('✅ Default settings populated successfully:')
        for setting in settings:
            print(f'   {setting[0]}: {setting[1]}')
        
        conn.close()
        return True
        
    except Exception as e:
        print(f'❌ Error populating settings: {e}')
        return False

if __name__ == "__main__":
    populate_settings()
