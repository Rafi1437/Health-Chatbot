"""
Test admin login functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from admin.admin_login import authenticate_admin

def test_admin_login():
    """Test admin login functionality"""
    
    print("🔐 Testing Admin Login")
    print("=" * 40)
    
    # Test correct credentials
    print("Testing correct credentials...")
    result = authenticate_admin('admin', 'admin123')
    print(f"Login result: {result}")
    
    if result:
        print("✅ Admin login successful!")
    else:
        print("❌ Admin login failed!")
    
    # Test incorrect credentials
    print("\nTesting incorrect credentials...")
    result = authenticate_admin('admin', 'wrongpassword')
    print(f"Login result: {result}")
    
    if result:
        print("❌ Should have failed!")
    else:
        print("✅ Correctly rejected wrong password")
    
    # Test wrong username
    print("\nTesting wrong username...")
    result = authenticate_admin('wronguser', 'admin123')
    print(f"Login result: {result}")
    
    if result:
        print("❌ Should have failed!")
    else:
        print("✅ Correctly rejected wrong username")

if __name__ == "__main__":
    test_admin_login()
