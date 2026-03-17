"""
Test all admin portal modules for potential errors
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_admin_dashboard():
    """Test admin dashboard statistics"""
    
    print("🧪 Testing Admin Dashboard")
    print("-" * 30)
    
    try:
        from admin.admin_dashboard import get_dashboard_statistics
        
        stats = get_dashboard_statistics()
        print("✅ Dashboard statistics fetched successfully:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard statistics error: {e}")
        return False

def test_user_management():
    """Test user management functionality"""
    
    print("\n🧪 Testing User Management")
    print("-" * 30)
    
    try:
        from admin.user_management import get_users_data
        
        users_df = get_users_data()
        print(f"✅ Users data fetched: {len(users_df)} users")
        
        if not users_df.empty:
            print("✅ Sample user data:")
            print(users_df.head(1).to_string())
        
        return True
        
    except Exception as e:
        print(f"❌ User management error: {e}")
        return False

def test_mental_health_admin():
    """Test mental health admin functionality"""
    
    print("\n🧪 Testing Mental Health Admin")
    print("-" * 30)
    
    try:
        from admin.mental_health_admin import get_mental_health_data
        
        mh_data = get_mental_health_data()
        print(f"✅ Mental health data fetched: {len(mh_data)} entries")
        
        if not mh_data.empty:
            print("✅ Sample mental health data:")
            print(mh_data.head(1).to_string())
        
        return True
        
    except Exception as e:
        print(f"❌ Mental health admin error: {e}")
        return False

def test_chatbot_admin():
    """Test chatbot admin functionality"""
    
    print("\n🧪 Testing Chatbot Admin")
    print("-" * 30)
    
    try:
        from admin.chatbot_admin import get_chatbot_statistics
        
        stats = get_chatbot_statistics()
        print("✅ Chatbot statistics fetched successfully:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chatbot admin error: {e}")
        return False

def test_hydration_admin():
    """Test hydration admin functionality"""
    
    print("\n🧪 Testing Hydration Admin")
    print("-" * 30)
    
    try:
        from admin.hydration_admin import get_hydration_statistics
        
        stats = get_hydration_statistics()
        print("✅ Hydration statistics fetched successfully:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hydration admin error: {e}")
        return False

def test_settings():
    """Test settings functionality"""
    
    print("\n🧪 Testing Settings")
    print("-" * 30)
    
    try:
        from database.db_setup import get_setting, update_setting
        
        # Test getting settings
        app_name = get_setting('app_name', 'Default App')
        print(f"✅ App name setting: {app_name}")
        
        # Test updating settings
        test_value = f"Test Value {os.urandom(4).hex()}"
        if update_setting('test_setting', test_value):
            retrieved_value = get_setting('test_setting')
            if retrieved_value == test_value:
                print("✅ Settings update/retrieve working")
                # Clean up test setting
                import sqlite3
                conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db'))
                cursor = conn.cursor()
                cursor.execute("DELETE FROM settings WHERE setting_key = ?", ('test_setting',))
                conn.commit()
                conn.close()
            else:
                print(f"❌ Settings update/retrieve failed. Expected: {test_value}, Got: {retrieved_value}")
                return False
        else:
            print("❌ Settings update failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Settings error: {e}")
        return False

def run_all_tests():
    """Run all admin portal tests"""
    
    print("🔬 Admin Portal Comprehensive Testing")
    print("=" * 50)
    
    tests = [
        test_admin_dashboard,
        test_user_management,
        test_mental_health_admin,
        test_chatbot_admin,
        test_hydration_admin,
        test_settings
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            failed += 1
    
    print(f"\n📊 Test Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All admin portal tests passed!")
    else:
        print(f"\n⚠️  {failed} tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    run_all_tests()
