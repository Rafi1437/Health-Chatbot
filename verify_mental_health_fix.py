"""
Verify the mental health admin KeyError fix
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def verify_mental_health_fix():
    """Verify the mental health admin KeyError fix"""
    
    print("🔧 Verifying Mental Health Admin Fix")
    print("=" * 40)
    
    try:
        from admin.mental_health_admin import get_mental_health_data, get_user_mental_health_stats
        
        # Get mental health data
        mh_data = get_mental_health_data()
        print(f"✅ Mental health data: {len(mh_data)} entries")
        
        if mh_data.empty:
            print("ℹ️  No mental health data available for testing")
            return True
        
        # Get user statistics
        user_stats = get_user_mental_health_stats(mh_data)
        print(f"✅ User statistics: {len(user_stats)} users")
        
        if user_stats.empty:
            print("ℹ️  No user statistics available for testing")
            return True
        
        # Test the specific functionality that was causing the KeyError
        print("\n🧪 Testing User Breakdown Section:")
        print("-" * 35)
        
        top_users = user_stats.head(3)
        
        for index, user_stat in top_users.iterrows():
            # This is the exact code that was causing the KeyError
            user_display = f"👤 {user_stat['user_name']} ({user_stat['user_email']})"
            print(f"✅ User display: {user_display}")
            
            # Test accessing all the fields
            total_entries = user_stat['total_entries']
            avg_confidence = user_stat['avg_confidence']
            positive_entries = user_stat['positive_entries']
            neutral_entries = user_stat['neutral_entries']
            negative_entries = user_stat['negative_entries']
            
            print(f"   Total Entries: {total_entries}")
            print(f"   Avg Confidence: {avg_confidence:.1%}")
            print(f"   Sentiments: 😊{positive_entries} 😐{neutral_entries} 😔{negative_entries}")
            
            # Test getting recent entries for this user
            user_entries = mh_data[mh_data['user_id'] == user_stat['user_id']].head(3)
            print(f"   Recent entries: {len(user_entries)}")
        
        print("\n🎉 Mental Health Admin KeyError is FIXED!")
        print("✅ All user statistics are accessible correctly")
        print("✅ User breakdown section will work properly")
        
        return True
        
    except KeyError as e:
        print(f"❌ KeyError still exists: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verify_mental_health_fix()
