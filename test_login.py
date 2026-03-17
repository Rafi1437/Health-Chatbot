"""
Test script for login functionality
"""

import sqlite3
import os

def test_database_structure():
    """Test database structure and user data"""
    
    print("🔐 LOGIN SYSTEM TEST")
    print("=" * 40)
    
    # Connect to database
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check table structure
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("📋 Users Table Structure:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Check if there are any users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"\n👥 Total Users: {user_count}")
        
        if user_count > 0:
            # Show sample user data (without passwords)
            cursor.execute("SELECT id, name, email, password, age FROM users LIMIT 3")
            users = cursor.fetchall()
            
            print("\n📝 Sample Users:")
            for user in users:
                print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Age: {user[4]}")
                
                # Test the correct index positions
                print(f"    → user[0] (id): {user[0]}")
                print(f"    → user[1] (name): {user[1]}")
                print(f"    → user[2] (email): {user[2]}")
                print(f"    → user[3] (password): [HIDDEN]")
                print(f"    → user[4] (age): {user[4]}")
                print()
        else:
            print("ℹ️ No users found. You need to create an account first.")
        
        print("✅ Database structure test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_database_structure()
