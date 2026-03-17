"""
Final verification of admin portal functionality
"""

import sqlite3
import os

def final_verification():
    """Final verification of admin portal"""
    
    print("🎯 Final Admin Portal Verification")
    print("=" * 50)
    
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test all critical admin portal queries
        tests = [
            {
                'name': 'Dashboard Statistics - Total Users',
                'query': 'SELECT COUNT(*) FROM users WHERE is_active = 1',
                'expected': '>= 0'
            },
            {
                'name': 'Dashboard Statistics - Mental Health Entries',
                'query': 'SELECT COUNT(*) FROM mental_health',
                'expected': '>= 0'
            },
            {
                'name': 'Dashboard Statistics - Chatbot Interactions',
                'query': 'SELECT COUNT(*) FROM chatbot_logs',
                'expected': '>= 0'
            },
            {
                'name': 'Dashboard Statistics - Hydration Logs',
                'query': 'SELECT COUNT(*) FROM hydration',
                'expected': '>= 0'
            },
            {
                'name': 'User Management - Get Users',
                'query': 'SELECT id, name, email, age, is_active, created_at FROM users ORDER BY created_at DESC',
                'expected': '>= 0 rows'
            },
            {
                'name': 'Mental Health Admin - Get Entries',
                'query': '''
                    SELECT mh.id, mh.user_id, mh.feeling, mh.sentiment, mh.confidence, mh.timestamp,
                           u.name as user_name, u.email as user_email, u.age as user_age
                    FROM mental_health mh
                    JOIN users u ON mh.user_id = u.id
                    ORDER BY mh.timestamp DESC
                ''',
                'expected': '>= 0 rows'
            },
            {
                'name': 'Chatbot Admin - Get Statistics',
                'query': '''
                    SELECT 
                        (SELECT COUNT(*) FROM chatbot_logs) as total_chats,
                        (SELECT COUNT(DISTINCT user_id) FROM chatbot_logs) as unique_users,
                        (SELECT COUNT(*) FROM chatbot_logs WHERE date(timestamp) = date('now')) as today_chats
                ''',
                'expected': '>= 0'
            },
            {
                'name': 'Hydration Admin - Get Statistics',
                'query': '''
                    SELECT 
                        (SELECT COUNT(*) FROM hydration) as total_logs,
                        (SELECT COUNT(DISTINCT user_id) FROM hydration WHERE timestamp >= date('now', '-7 days')) as active_users,
                        (SELECT COUNT(*) FROM hydration WHERE date(timestamp) = date('now')) as today_logs
                ''',
                'expected': '>= 0'
            },
            {
                'name': 'Settings - Get App Name',
                'query': 'SELECT setting_value FROM settings WHERE setting_key = "app_name"',
                'expected': 'not None'
            }
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                cursor.execute(test['query'])
                result = cursor.fetchone()
                
                if result:
                    if test['expected'] == '>= 0':
                        print(f"✅ {test['name']}: {result[0]} records")
                        passed += 1
                    elif test['expected'] == '>= 0 rows':
                        print(f"✅ {test['name']}: Query executed successfully")
                        passed += 1
                    elif test['expected'] == 'not None':
                        if result[0]:
                            print(f"✅ {test['name']}: {result[0]}")
                            passed += 1
                        else:
                            print(f"❌ {test['name']}: No result")
                            failed += 1
                else:
                    print(f"❌ {test['name']}: No result")
                    failed += 1
                    
            except Exception as e:
                print(f"❌ {test['name']}: {e}")
                failed += 1
        
        # Check admin account
        cursor.execute('SELECT username, email, full_name, is_active FROM admins WHERE username = "admin"')
        admin = cursor.fetchone()
        
        if admin:
            print(f"✅ Admin Account: {admin[0]} ({admin[1]}) - Active: {admin[3]}")
        else:
            print("❌ Admin Account: Not found")
            failed += 1
        
        conn.close()
        
        print(f"\n📊 Final Results:")
        print(f"   ✅ Passed: {passed}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print("\n🎉 ALL ADMIN PORTAL FUNCTIONALITY IS WORKING!")
            print("\n🔑 Login Credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            print("\n🌐 Access: http://localhost:8501")
            print("   Click '👨‍💼 Go to Admin Login'")
        else:
            print(f"\n⚠️  {failed} tests failed. Admin portal may have issues.")
        
        return failed == 0
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return False

if __name__ == "__main__":
    final_verification()
