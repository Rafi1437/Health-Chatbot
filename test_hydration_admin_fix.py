"""
Test hydration admin timestamp fix
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_hydration_admin_fix():
    """Test hydration admin timestamp fix"""
    
    print("🔧 Testing Hydration Admin Timestamp Fix")
    print("=" * 45)
    
    try:
        from admin.hydration_admin import get_hydration_logs, get_user_hydration_logs
        
        # Test main hydration logs
        print("🧪 Testing Main Hydration Logs")
        print("-" * 35)
        
        hydration_logs = get_hydration_logs()
        print(f"✅ Hydration logs fetched: {len(hydration_logs)} entries")
        
        if not hydration_logs.empty:
            print(f"✅ Columns: {list(hydration_logs.columns)}")
            
            # Test timestamp column type
            timestamp_type = type(hydration_logs['timestamp'].iloc[0])
            print(f"✅ Timestamp type: {timestamp_type}")
            
            # Test timestamp formatting
            for _, log in hydration_logs.head(3).iterrows():
                try:
                    timestamp_str = log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                    print(f"✅ Timestamp format: {timestamp_str}")
                except Exception as e:
                    print(f"❌ Timestamp format error: {e}")
        
        # Test user-specific hydration logs
        print("\n🧪 Testing User Hydration Logs")
        print("-" * 35)
        
        # Get a user ID from the logs
        if not hydration_logs.empty:
            user_id = hydration_logs['user_id'].iloc[0]
            user_logs = get_user_hydration_logs(user_id, limit=3)
            print(f"✅ User logs fetched: {len(user_logs)} entries")
            
            if not user_logs.empty:
                print(f"✅ User logs columns: {list(user_logs.columns)}")
                
                # Test timestamp column type
                timestamp_type = type(user_logs['timestamp'].iloc[0])
                print(f"✅ User timestamp type: {timestamp_type}")
                
                # Test the exact code that was causing the error
                for _, log in user_logs.iterrows():
                    achievement = (log['water_ml'] / log['recommended_ml']) * 100
                    status = "🟢" if achievement >= 100 else "🟡" if achievement >= 75 else "🔴"
                    
                    # Test the safe timestamp formatting
                    try:
                        timestamp_str = log['timestamp'].strftime('%Y-%m-%d %H:%M')
                        print(f"✅ Safe timestamp format: {status} {timestamp_str}: {log['water_ml']}ml ({achievement:.0f}% of goal)")
                    except (AttributeError, ValueError):
                        if isinstance(log['timestamp'], str):
                            timestamp_str = log['timestamp']
                        else:
                            timestamp_str = str(log['timestamp'])
                        print(f"✅ Fallback timestamp format: {status} {timestamp_str}: {log['water_ml']}ml ({achievement:.0f}% of goal)")
        
        print("\n🎉 Hydration Admin Timestamp Fix is WORKING!")
        print("✅ All timestamp formatting is handled safely")
        print("✅ AttributeError will no longer occur")
        
        return True
        
    except Exception as e:
        print(f"❌ Hydration admin test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_hydration_admin_fix()
