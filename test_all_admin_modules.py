"""
Test all admin portal modules for errors
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_all_admin_modules():
    """Test all admin portal modules"""
    
    print("🔬 Comprehensive Admin Portal Testing")
    print("=" * 50)
    
    tests = []
    
    # Test 1: Admin Dashboard
    print("\n🧪 Testing Admin Dashboard")
    print("-" * 30)
    try:
        from admin.admin_dashboard import get_dashboard_statistics
        stats = get_dashboard_statistics()
        print(f"✅ Dashboard statistics: {stats}")
        tests.append(("Dashboard", True, None))
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        tests.append(("Dashboard", False, str(e)))
    
    # Test 2: User Management
    print("\n🧪 Testing User Management")
    print("-" * 30)
    try:
        from admin.user_management import get_users_data
        users_df = get_users_data()
        print(f"✅ Users data: {len(users_df)} users")
        if not users_df.empty:
            print(f"   Columns: {list(users_df.columns)}")
        tests.append(("User Management", True, None))
    except Exception as e:
        print(f"❌ User management error: {e}")
        tests.append(("User Management", False, str(e)))
    
    # Test 3: Mental Health Admin
    print("\n🧪 Testing Mental Health Admin")
    print("-" * 30)
    try:
        from admin.mental_health_admin import get_mental_health_data, get_user_mental_health_stats
        mh_data = get_mental_health_data()
        print(f"✅ Mental health data: {len(mh_data)} entries")
        
        if not mh_data.empty:
            user_stats = get_user_mental_health_stats(mh_data)
            print(f"✅ User stats: {len(user_stats)} users")
            if not user_stats.empty:
                print(f"   User stats columns: {list(user_stats.columns)}")
        
        tests.append(("Mental Health", True, None))
    except Exception as e:
        print(f"❌ Mental health error: {e}")
        tests.append(("Mental Health", False, str(e)))
    
    # Test 4: Chatbot Admin
    print("\n🧪 Testing Chatbot Admin")
    print("-" * 30)
    try:
        from admin.chatbot_admin import get_chatbot_statistics, get_chat_logs
        stats = get_chatbot_statistics()
        print(f"✅ Chatbot statistics: {stats}")
        
        chat_logs = get_chat_logs()
        print(f"✅ Chat logs: {len(chat_logs)} entries")
        
        tests.append(("Chatbot", True, None))
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        tests.append(("Chatbot", False, str(e)))
    
    # Test 5: Hydration Admin
    print("\n🧪 Testing Hydration Admin")
    print("-" * 30)
    try:
        from admin.hydration_admin import get_hydration_statistics, get_low_hydration_users
        stats = get_hydration_statistics()
        print(f"✅ Hydration statistics: {stats}")
        
        low_users = get_low_hydration_users()
        print(f"✅ Low hydration users: {len(low_users)} users")
        
        tests.append(("Hydration", True, None))
    except Exception as e:
        print(f"❌ Hydration error: {e}")
        tests.append(("Hydration", False, str(e)))
    
    # Test 6: Settings
    print("\n🧪 Testing Settings")
    print("-" * 30)
    try:
        from database.db_setup import get_setting, update_setting
        app_name = get_setting('app_name')
        print(f"✅ App name: {app_name}")
        
        # Test setting update
        test_value = f"test_{os.urandom(4).hex()}"
        if update_setting('test_setting', test_value):
            retrieved = get_setting('test_setting')
            if retrieved == test_value:
                print("✅ Settings update/retrieve working")
                # Clean up
                import sqlite3
                conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db'))
                cursor = conn.cursor()
                cursor.execute("DELETE FROM settings WHERE setting_key = ?", ('test_setting',))
                conn.commit()
                conn.close()
            else:
                raise Exception("Settings update/retrieve failed")
        else:
            raise Exception("Settings update failed")
        
        tests.append(("Settings", True, None))
    except Exception as e:
        print(f"❌ Settings error: {e}")
        tests.append(("Settings", False, str(e)))
    
    # Results
    print(f"\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, success, _ in tests if success)
    failed = len(tests) - passed
    
    for module, success, error in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:8} {module}")
        if error:
            print(f"         Error: {error}")
    
    print(f"\n📈 Overall Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {(passed/len(tests)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL ADMIN PORTAL MODULES ARE WORKING!")
        print("\n🔑 Login Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🌐 Access: http://localhost:8501")
        print("   Click '👨‍💼 Go to Admin Login'")
    else:
        print(f"\n⚠️  {failed} modules have issues. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    test_all_admin_modules()
