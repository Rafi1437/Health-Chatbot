"""
Test script for hydration tracker functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from modules.hydration import calculate_recommended_water

def test_hydration_calculations():
    """Test hydration calculations with different age inputs"""
    
    print("💧 HYDRATION TRACKER TEST")
    print("=" * 40)
    
    # Test cases with different age formats
    test_cases = [
        (65, "Integer age (65)"),
        ("70", "String age ('70')"),
        (80, "Integer age (80)"),
        ("85", "String age ('85')"),
        (45, "Younger age (45)"),
        ("invalid", "Invalid age string"),
        (None, "None age"),
    ]
    
    for age_input, description in test_cases:
        try:
            recommended = calculate_recommended_water(age_input)
            print(f"✅ {description}: {recommended} ml")
        except Exception as e:
            print(f"❌ {description}: ERROR - {e}")
    
    print("\n🎯 Testing specific senior cases:")
    
    # Test typical senior ages
    senior_ages = [60, 65, 70, 75, 80, 85, 90]
    
    for age in senior_ages:
        recommended = calculate_recommended_water(age)
        print(f"Age {age}: {recommended} ml/day")
    
    print("\n✅ Hydration calculation tests completed!")

if __name__ == "__main__":
    test_hydration_calculations()
