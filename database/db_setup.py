"""
Database setup for Healthcare App
Creates SQLite database and required tables for both users and admin portal
"""

import sqlite3
import bcrypt
import os

def create_database():
    """Create SQLite database and required tables"""
    
    # Get database path
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
    
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Mental health records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mental_health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            feeling TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Hydration records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hydration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            water_ml INTEGER NOT NULL,
            recommended_ml INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Chatbot conversation table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatbot_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Settings table for admin configuration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT NOT NULL,
            setting_type TEXT DEFAULT 'text',
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Admin activity logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES admins (id)
        )
    ''')
    
    conn.commit()
    
    # Create default admin if not exists
    create_default_admin(cursor)
    
    # Insert default settings
    create_default_settings(cursor)
    
    conn.close()
    print("Database and tables created successfully!")

def create_default_admin(cursor):
    """Create default admin account"""
    
    # Check if admin already exists
    cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        # Create default admin
        hashed_password = hash_password('admin123')
        cursor.execute('''
            INSERT INTO admins (username, email, password, full_name)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@healthcare.com', hashed_password, 'System Administrator'))
        print("Default admin account created (username: admin, password: admin123)")

def create_default_settings(cursor):
    """Create default application settings"""
    
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
            INSERT OR IGNORE INTO settings (setting_key, setting_value, setting_type, description)
            VALUES (?, ?, ?, ?)
        ''', (setting_key, setting_value, setting_type, description))

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def log_admin_action(admin_id, action, details=None, ip_address=None):
    """Log admin activity"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO admin_logs (admin_id, action, details, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (admin_id, action, details, ip_address))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging admin action: {e}")

def get_setting(setting_key, default_value=None):
    """Get setting value from database"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT setting_value FROM settings WHERE setting_key = ?", (setting_key,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result[0]
        return default_value
    except Exception as e:
        print(f"Error getting setting {setting_key}: {e}")
        return default_value

def update_setting(setting_key, setting_value):
    """Update setting value in database"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE settings SET setting_value = ?, updated_at = CURRENT_TIMESTAMP
            WHERE setting_key = ?
        ''', (setting_value, setting_key))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating setting {setting_key}: {e}")
        return False

if __name__ == "__main__":
    create_database()
