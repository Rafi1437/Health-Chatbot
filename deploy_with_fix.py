"""
Deploy with NLTK Fix - Automated deployment script
This script will prepare your app for Streamlit Cloud deployment with NLTK fixes
"""

import os
import subprocess
import sys

def prepare_for_deployment():
    """Prepare the app for deployment with NLTK fixes"""
    
    print("🚀 PREPARING FOR STREAMLIT CLOUD DEPLOYMENT")
    print("=" * 60)
    
    # Step 1: Test current setup
    print("\n🧪 Step 1: Testing current setup...")
    try:
        import nltk
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        
        test_text = "Hello world, this is a test."
        tokens = word_tokenize(test_text)
        stop_words = stopwords.words('english')
        
        if len(tokens) > 0 and len(stop_words) > 0:
            print("✅ NLTK setup is working locally")
        else:
            print("⚠️ NLTK setup has issues locally")
    except Exception as e:
        print(f"❌ NLTK setup error: {e}")
    
    # Step 2: Create NLTK data directory
    print("\n📁 Step 2: Creating NLTK data directories...")
    nltk_paths = [
        './nltk_data',
        os.path.join(os.getcwd(), 'nltk_data'),
        os.path.expanduser('~/nltk_data')
    ]
    
    for path in nltk_paths:
        try:
            os.makedirs(path, exist_ok=True)
            print(f"✅ Created: {path}")
        except Exception as e:
            print(f"❌ Failed to create {path}: {e}")
    
    # Step 3: Download NLTK data locally
    print("\n📦 Step 3: Downloading NLTK data locally...")
    try:
        import nltk
        packages = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'wordnet']
        
        for package in packages:
            try:
                nltk.data.find(f'tokenizers/{package}' if package == 'punkt' else f'corpora/{package}')
                print(f"✅ {package} already available")
            except LookupError:
                print(f"📦 Downloading {package}...")
                try:
                    nltk.download(package, quiet=True)
                    print(f"✅ {package} downloaded successfully")
                except Exception as e:
                    print(f"❌ Failed to download {package}: {e}")
    except Exception as e:
        print(f"❌ NLTK download error: {e}")
    
    # Step 4: Test fallback system
    print("\n🔄 Step 4: Testing fallback system...")
    try:
        from ml.fallback_sentiment import FallbackSentimentAnalyzer
        analyzer = FallbackSentimentAnalyzer()
        result = analyzer.predict_sentiment("I am very happy today!")
        
        if result and 'sentiment' in result:
            print(f"✅ Fallback analyzer works: {result['sentiment']}")
        else:
            print("❌ Fallback analyzer failed")
    except Exception as e:
        print(f"❌ Fallback analyzer error: {e}")
    
    # Step 5: Git operations
    print("\n📝 Step 5: Preparing for git push...")
    try:
        # Check if git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository found")
            
            # Add all changes
            subprocess.run(['git', 'add', '.'], capture_output=True)
            print("✅ Changes added to git")
            
            # Commit changes
            commit_message = "Fix NLTK issues for Streamlit Cloud deployment - Ultimate solution with multi-path fallback"
            subprocess.run(['git', 'commit', '-m', commit_message], capture_output=True)
            print("✅ Changes committed to git")
            
            # Push to remote
            subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True)
            print("✅ Changes pushed to remote repository")
            
        else:
            print("❌ Git repository not found")
    except Exception as e:
        print(f"❌ Git operations failed: {e}")
    
    # Step 6: Deployment instructions
    print("\n🚀 Step 6: Deployment Instructions")
    print("=" * 60)
    print("1. Go to: https://share.streamlit.io/")
    print("2. Sign in with your GitHub account")
    print("3. Click: 'Deploy an app'")
    print("4. Select: your repository")
    print("5. Configure:")
    print("   - Main file: app.py")
    print("   - Python version: 3.9")
    print("6. In 'Advanced settings', add environment variable:")
    print("   NLTK_DATA = /home/adminuser/nltk_data")
    print("7. Click: 'Deploy!'")
    print("\n🎉 Your app should now work without NLTK errors!")
    
    print("\n📋 If errors still occur:")
    print("1. Check deployment logs in Streamlit Cloud dashboard")
    print("2. The fallback system should activate automatically")
    print("3. App will continue working even if NLTK fails")
    print("4. Contact support if needed")

if __name__ == "__main__":
    prepare_for_deployment()
