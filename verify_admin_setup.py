"""
Verify admin portal setup is working correctly
"""

import sqlite3
import bcrypt
import os

def verify_admin_setup():
    """Verify admin portal setup"""
    
    print("🔍 Admin Portal Setup Verification")
    print("=" * 50)
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check admin table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admins'")
        admin_table = cursor.fetchone()
        
        if admin_table:
            print("✅ Admins table exists")
        else:
            print("❌ Admins table missing")
            return False
        
        # Check admin account
        cursor.execute("SELECT id, username, email, full_name, is_active FROM admins WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if admin:
            print(f"✅ Admin account found: {admin[1]} ({admin[2]})")
            print(f"   Full Name: {admin[3]}")
            print(f"   Active: {admin[4]}")
            
            # Test password
            cursor.execute("SELECT password FROM admins WHERE username = 'admin'")
            stored_password = cursor.fetchone()[0]
            
            if bcrypt.checkpw('admin123'.encode('utf-8'), stored_password.encode('utf-8')):
                print("✅ Password verification works")
            else:
                print("❌ Password verification failed")
                return False
        else:
            print("❌ Admin account not found")
            return False
        
        # Check settings table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'")
        settings_table = cursor.fetchone()
        
        if settings_table:
            print("✅ Settings table exists")
            
            # Check some default settings
            cursor.execute("SELECT setting_key, setting_value FROM settings WHERE setting_key IN ('app_name', 'mental_health_enabled', 'chatbot_enabled', 'hydration_enabled')")
            settings = cursor.fetchall()
            
            print("✅ Default settings:")
            for setting in settings:
                print(f"   {setting[0]}: {setting[1]}")
        else:
            print("❌ Settings table missing")
            return False
        
        # Check admin logs table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin_logs'")
        logs_table = cursor.fetchone()
        
        if logs_table:
            print("✅ Admin logs table exists")
        else:
            print("❌ Admin logs table missing")
            return False
        
        conn.close()
        print("\n🎉 Admin portal setup is COMPLETE and WORKING!")
        print("\n📋 Login Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🌐 Access the admin portal at: http://localhost:8501")
        print("   Click '👨‍💼 Go to Admin Login' button")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    verify_admin_setup()
