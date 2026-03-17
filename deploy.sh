#!/bin/bash

echo "🚀 Senior Healthcare App - Streamlit Cloud Deployment Script"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Senior Healthcare App with Admin Portal"
fi

# Check if remote is set
if ! git remote get-url origin &>/dev/null; then
    echo "⚠️  Please set up GitHub repository first:"
    echo "   1. Go to https://github.com"
    echo "   2. Create new repository: senior-healthcare-app"
    echo "   3. Run: git remote add origin https://github.com/YOUR_USERNAME/senior-healthcare-app.git"
    echo "   4. Run this script again"
    exit 1
fi

echo "📦 Verifying requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo "✅ requirements.txt found"

echo "📝 Committing latest changes..."
git add .
git commit -m "Update for Streamlit Cloud deployment - $(date)"

echo "📤 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "❌ Failed to push to GitHub. Please check your credentials."
    exit 1
fi

echo ""
echo "🌐 Next Steps for Streamlit Cloud Deployment:"
echo "1. Go to: https://share.streamlit.io/"
echo "2. Click 'Deploy an app'"
echo "3. Select your GitHub repository"
echo "4. Main file path: app.py"
echo "5. Click 'Deploy!'"
echo ""
echo "📋 Deployment Configuration:"
echo "- Repository: senior-healthcare-app"
echo "- Main file: app.py"
echo "- Python version: 3.9"
echo "- Public repository: Yes"
echo ""
echo "🔧 Optional: Add environment variables in Streamlit Cloud:"
echo "- NLTK_DATA = /home/adminuser/.nltk"
echo ""
echo "✅ Your app is ready for deployment!"
echo "🎉 After deployment, your app will be available at:"
echo "   https://your-username.streamlit.app/"
