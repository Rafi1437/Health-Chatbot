"""
Test mental health admin functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_mental_health_admin():
    """Test mental health admin functionality"""
    
    print("🧪 Testing Mental Health Admin")
    print("=" * 40)
    
    try:
        from admin.mental_health_admin import get_mental_health_data, get_user_mental_health_stats
        
        # Test getting mental health data
        mh_data = get_mental_health_data()
        print(f"✅ Mental health data fetched: {len(mh_data)} entries")
        
        if not mh_data.empty:
            print("✅ Sample mental health data columns:")
            print(f"   Columns: {list(mh_data.columns)}")
            
            # Test user statistics
            user_stats = get_user_mental_health_stats(mh_data)
            print(f"✅ User statistics fetched: {len(user_stats)} users")
            
            if not user_stats.empty:
                print("✅ User statistics columns:")
                print(f"   Columns: {list(user_stats.columns)}")
                
                # Test accessing user data
                for index, user_stat in user_stats.head(3).iterrows():
                    print(f"   User {index}: {user_stat['user_name']} ({user_stat['user_email']})")
                    print(f"     Total Entries: {user_stat['total_entries']}")
                    print(f"     Avg Confidence: {user_stat['avg_confidence']:.1%}")
                    print(f"     Positive: {user_stat['positive_entries']}, Neutral: {user_stat['neutral_entries']}, Negative: {user_stat['negative_entries']}")
            else:
                print("ℹ️  No user statistics available")
        else:
            print("ℹ️  No mental health data available")
        
        print("\n✅ Mental health admin test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Mental health admin error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_mental_health_admin()
