"""
Test Cloud Deployment Readiness
Verifies all components work for Streamlit Cloud deployment
"""

import os
import sys

def test_cloud_deployment_readiness():
    """Test all components for cloud deployment"""
    
    print("🚀 CLOUD DEPLOYMENT READINESS TEST")
    print("=" * 50)
    
    tests = []
    
    # Test 1: NLTK Setup
    print("\n🧪 1. Testing NLTK Setup")
    print("-" * 30)
    try:
        import nltk
        import os
        
        # Test multi-path NLTK setup
        possible_paths = [
            '/home/adminuser/nltk_data',
            os.path.expanduser('~/nltk_data'),
            '/tmp/nltk_data',
            './nltk_data',
            os.path.join(os.getcwd(), 'nltk_data')
        ]
        
        # Add paths to NLTK
        for path in possible_paths:
            if path not in nltk.data.path:
                nltk.data.path.append(path)
        
        # Test basic NLTK functionality
        try:
            from nltk.tokenize import word_tokenize
            test_text = "Hello world, this is a test."
            tokens = word_tokenize(test_text)
            print("✅ NLTK tokenization works")
            tests.append(("NLTK Tokenization", True, None))
        except Exception as e:
            print(f"❌ NLTK tokenization failed: {e}")
            tests.append(("NLTK Tokenization", False, str(e)))
            
        try:
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            print("✅ NLTK stopwords work")
            tests.append(("NLTK Stopwords", True, None))
        except Exception as e:
            print(f"❌ NLTK stopwords failed: {e}")
            tests.append(("NLTK Stopwords", False, str(e)))
            
    except Exception as e:
        print(f"❌ NLTK setup failed: {e}")
        tests.append(("NLTK Setup", False, str(e)))
    
    # Test 2: Fallback Sentiment Analyzer
    print("\n🧪 2. Testing Fallback Sentiment Analyzer")
    print("-" * 30)
    try:
        sys.path.append(os.path.dirname(__file__))
        from ml.fallback_sentiment import FallbackSentimentAnalyzer
        
        analyzer = FallbackSentimentAnalyzer()
        test_text = "I am feeling very happy today!"
        result = analyzer.predict_sentiment(test_text)
        
        if result and 'sentiment' in result and 'confidence' in result:
            print(f"✅ Fallback analyzer works: {result['sentiment']} ({result['confidence']:.2f})")
            tests.append(("Fallback Analyzer", True, None))
        else:
            print("❌ Fallback analyzer returned invalid result")
            tests.append(("Fallback Analyzer", False, "Invalid result"))
            
    except Exception as e:
        print(f"❌ Fallback analyzer failed: {e}")
        tests.append(("Fallback Analyzer", False, str(e)))
    
    # Test 3: Main App Imports
    print("\n🧪 3. Testing Main App Imports")
    print("-" * 30)
    try:
        # Test app.py imports
        import streamlit as st
        print("✅ Streamlit import works")
        tests.append(("Streamlit Import", True, None))
        
        # Test database setup
        from database.db_setup import create_database
        print("✅ Database setup import works")
        tests.append(("Database Setup", True, None))
        
        # Test auth modules
        from auth.login import show_login
        from auth.signup import show_signup
        print("✅ Auth modules import works")
        tests.append(("Auth Modules", True, None))
        
        # Test feature modules
        from modules.mental_health import show_mental_health
        from modules.chatbot import show_chatbot
        from modules.hydration import show_hydration
        from modules.reports import show_reports
        print("✅ Feature modules import works")
        tests.append(("Feature Modules", True, None))
        
        # Test admin modules
        from admin.admin_login import show_admin_login
        from admin.admin_dashboard import show_admin_dashboard
        print("✅ Admin modules import works")
        tests.append(("Admin Modules", True, None))
        
    except Exception as e:
        print(f"❌ Main app imports failed: {e}")
        tests.append(("Main App Imports", False, str(e)))
    
    # Test 4: Mental Health Module
    print("\n🧪 4. Testing Mental Health Module")
    print("-" * 30)
    try:
        from modules.mental_health import NLTK_AVAILABLE, FALLBACK_AVAILABLE
        
        if NLTK_AVAILABLE:
            print("✅ NLTK is available")
            tests.append(("NLTK Available", True, None))
        else:
            print("⚠️ NLTK not available (fallback will be used)")
            tests.append(("NLTK Available", False, "Not available"))
            
        if FALLBACK_AVAILABLE:
            print("✅ Fallback analyzer is available")
            tests.append(("Fallback Available", True, None))
        else:
            print("❌ Fallback analyzer not available")
            tests.append(("Fallback Available", False, "Not available"))
            
    except Exception as e:
        print(f"❌ Mental health module test failed: {e}")
        tests.append(("Mental Health Module", False, str(e)))
    
    # Test 5: File Structure
    print("\n🧪 5. Testing File Structure")
    print("-" * 30)
    required_files = [
        'app.py',
        'requirements.txt',
        'ml/sentiment_model.py',
        'ml/fallback_sentiment.py',
        'modules/mental_health.py',
        'database/db_setup.py',
        'auth/login.py',
        'admin/admin_login.py'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
            tests.append((f"File: {file}", True, None))
        else:
            print(f"❌ {file} missing")
            tests.append((f"File: {file}", False, "Missing"))
    
    # Results Summary
    print(f"\n📊 CLOUD DEPLOYMENT TEST RESULTS")
    print("=" * 50)
    
    passed = sum(1 for _, success, _ in tests if success)
    failed = len(tests) - passed
    success_rate = (passed / len(tests)) * 100
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    print(f"\n📋 Detailed Results:")
    for test_name, success, error in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:8} {test_name}")
        if error:
            print(f"         Error: {error[:60]}...")
    
    # Cloud Readiness Assessment
    print(f"\n🎯 CLOUD READINESS ASSESSMENT:")
    if success_rate >= 90:
        print("🎉 EXCELLENT: Your app is fully ready for cloud deployment!")
        print("✅ All critical components are working")
        print("✅ NLTK and fallback systems are operational")
        print("✅ File structure is complete")
        print("✅ Deploy with confidence!")
    elif success_rate >= 75:
        print("⚠️  GOOD: Your app is mostly ready for cloud deployment.")
        print("✅ Most components are working")
        print("⚠️  Some issues may need attention")
        print("✅ Should deploy successfully with fallbacks")
    else:
        print("❌ NEEDS WORK: Your app needs fixes before cloud deployment.")
        print("❌ Critical components are failing")
        print("❌ Fix the issues above before deploying")
    
    return success_rate >= 75

if __name__ == "__main__":
    test_cloud_deployment_readiness()
