"""
Update database schema to fix admin portal issues
"""

import sqlite3
import os

def update_database_schema():
    """Update database schema with missing columns"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Updating Database Schema")
        print("=" * 40)
        
        # Check and add is_active column to users table
        cursor.execute('PRAGMA table_info(users)')
        users_columns = [col[1] for col in cursor.fetchall()]
        
        if 'is_active' not in users_columns:
            print("✅ Adding is_active column to users table")
            cursor.execute('ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1')
            print("   - Added is_active column with default value 1")
        else:
            print("✅ is_active column already exists in users table")
        
        # Check and update existing users to be active
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_active IS NULL')
        null_active_users = cursor.fetchone()[0]
        
        if null_active_users > 0:
            print(f"✅ Updating {null_active_users} users to active status")
            cursor.execute('UPDATE users SET is_active = 1 WHERE is_active IS NULL')
        else:
            print("✅ All users have active status set")
        
        # Verify the update
        cursor.execute('SELECT id, name, email, is_active FROM users LIMIT 5')
        users = cursor.fetchall()
        
        print("\n📋 Sample Users:")
        for user in users:
            status = "Active" if user[3] == 1 else "Inactive"
            print(f"   ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Status: {status}")
        
        # Check other required tables and columns
        required_tables = {
            'admins': ['id', 'username', 'email', 'password', 'full_name', 'is_active'],
            'mental_health': ['id', 'user_id', 'feeling', 'sentiment', 'confidence', 'timestamp'],
            'chatbot_logs': ['id', 'user_id', 'user_message', 'bot_response', 'timestamp'],
            'hydration': ['id', 'user_id', 'water_ml', 'recommended_ml', 'timestamp'],
            'settings': ['id', 'setting_key', 'setting_value', 'setting_type', 'description'],
            'admin_logs': ['id', 'admin_id', 'action', 'details', 'timestamp']
        }
        
        print("\n🔍 Verifying All Tables:")
        
        for table_name, required_columns in required_tables.items():
            cursor.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}"')
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.execute(f'PRAGMA table_info({table_name})')
                existing_columns = [col[1] for col in cursor.fetchall()]
                
                missing_columns = [col for col in required_columns if col not in existing_columns]
                
                if missing_columns:
                    print(f"⚠️  {table_name}: Missing columns {missing_columns}")
                else:
                    print(f"✅ {table_name}: All required columns present")
            else:
                print(f"❌ {table_name}: Table missing")
        
        # Check sample data counts
        print("\n📊 Database Statistics:")
        
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        print(f"   Users: {user_count}")
        
        cursor.execute('SELECT COUNT(*) FROM admins')
        admin_count = cursor.fetchone()[0]
        print(f"   Admins: {admin_count}")
        
        cursor.execute('SELECT COUNT(*) FROM mental_health')
        mh_count = cursor.fetchone()[0]
        print(f"   Mental Health Entries: {mh_count}")
        
        cursor.execute('SELECT COUNT(*) FROM chatbot_logs')
        chat_count = cursor.fetchone()[0]
        print(f"   Chatbot Logs: {chat_count}")
        
        cursor.execute('SELECT COUNT(*) FROM hydration')
        hydration_count = cursor.fetchone()[0]
        print(f"   Hydration Logs: {hydration_count}")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Database schema update completed successfully!")
        
    except Exception as e:
        print(f"❌ Error updating database schema: {e}")
        return False
    
    return True

if __name__ == "__main__":
    update_database_schema()
