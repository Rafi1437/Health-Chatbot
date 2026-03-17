"""
Verify deployment readiness for Senior Healthcare App
"""

import os
import sys

def check_deployment_readiness():
    """Check if project is ready for deployment"""
    
    print("🔍 Deployment Readiness Check")
    print("=" * 40)
    
    checks = []
    
    # Check 1: Required files
    print("📁 Checking required files...")
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
            checks.append(True)
        else:
            print(f"❌ {file} missing")
            checks.append(False)
    
    # Check 2: Required directories
    print("\n📁 Checking required directories...")
    required_dirs = [
        'auth',
        'modules',
        'ml',
        'database',
        'admin',
        'assets'
    ]
    
    for dir in required_dirs:
        if os.path.exists(dir):
            print(f"✅ {dir}/ directory exists")
            checks.append(True)
        else:
            print(f"❌ {dir}/ directory missing")
            checks.append(False)
    
    # Check 3: Requirements.txt content
    print("\n📦 Checking requirements.txt...")
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            required_packages = ['streamlit', 'pandas', 'numpy', 'scikit-learn', 'nltk', 'plotly', 'joblib', 'Pillow', 'bcrypt']
            
            for package in required_packages:
                if package.replace('-', '_').replace('_', '') in content.lower():
                    print(f"✅ {package} found in requirements")
                    checks.append(True)
                else:
                    print(f"❌ {package} missing from requirements")
                    checks.append(False)
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        checks.append(False)
    
    # Check 4: Streamlit config
    print("\n⚙️ Checking Streamlit configuration...")
    if os.path.exists('.streamlit/config.toml'):
        print("✅ .streamlit/config.toml exists")
        checks.append(True)
    else:
        print("❌ .streamlit/config.toml missing")
        checks.append(False)
    
    # Check 5: Git repository
    print("\n📝 Checking Git repository...")
    if os.path.exists('.git'):
        print("✅ Git repository initialized")
        checks.append(True)
    else:
        print("❌ Git repository not initialized")
        checks.append(False)
    
    # Results
    passed = sum(checks)
    total = len(checks)
    success_rate = (passed / total) * 100
    
    print(f"\n📊 Deployment Readiness Results:")
    print(f"   ✅ Passed: {passed}/{total}")
    print(f"   📈 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("\n🎉 Project is READY for deployment!")
        print("\n🚀 Next Steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Deploy to Streamlit Cloud: https://share.streamlit.io/")
        print("3. Select repository: senior-healthcare-app")
        print("4. Main file: app.py")
        print("5. Click Deploy!")
    elif success_rate >= 70:
        print("\n⚠️  Project is mostly ready. Fix the issues above.")
    else:
        print("\n❌ Project is NOT ready. Fix the issues above.")
    
    return success_rate >= 90

if __name__ == "__main__":
    check_deployment_readiness()
