"""
Script to create admin account manually
"""

import sqlite3
import bcrypt
import os

def create_admin_account():
    """Create admin account in database"""
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db')
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if admins table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admins'")
        table_exists = cursor.fetchone()
        
        print(f"Admins table exists: {table_exists}")
        
        if not table_exists:
            # Create admins table
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
            print("Admins table created")
        
        # Check if admin already exists
        cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'admin'")
        admin_exists = cursor.fetchone()[0]
        
        print(f"Admin exists: {admin_exists}")
        
        if admin_exists == 0:
            # Create admin account
            hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute('''
                INSERT INTO admins (username, email, password, full_name)
                VALUES (?, ?, ?, ?)
            ''', ('admin', 'admin@healthcare.com', hashed_password, 'System Administrator'))
            
            conn.commit()
            print("Admin account created successfully!")
        else:
            print("Admin account already exists")
        
        # Verify admin account
        cursor.execute('SELECT id, username, email, full_name, is_active FROM admins WHERE username = ?', ('admin',))
        admin = cursor.fetchone()
        
        if admin:
            print(f"Admin verification successful:")
            print(f"  ID: {admin[0]}")
            print(f"  Username: {admin[1]}")
            print(f"  Email: {admin[2]}")
            print(f"  Full Name: {admin[3]}")
            print(f"  Active: {admin[4]}")
            
            # Test password verification
            cursor.execute('SELECT password FROM admins WHERE username = ?', ('admin',))
            stored_password = cursor.fetchone()[0]
            
            if bcrypt.checkpw('admin123'.encode('utf-8'), stored_password.encode('utf-8')):
                print("Password verification: SUCCESS")
            else:
                print("Password verification: FAILED")
        else:
            print("Admin verification: FAILED")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_admin_account()
