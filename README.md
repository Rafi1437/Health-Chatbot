# Integrated Mental Health, Medical Chatbot Assistance & Hydration Monitoring App for Senior Citizens

A comprehensive healthcare application designed specifically for senior citizens, featuring mental health monitoring, medical chatbot assistance, hydration tracking, and a complete admin portal for management.

## 🏥 Features

### 🔐 Authentication System
- **Secure Login/Signup**: User authentication with password hashing
- **Session Management**: Secure session handling with Streamlit
- **Age Verification**: Designed for users 60+ years old

### 🧠 Mental Health Monitoring
- **Sentiment Analysis**: ML-powered mood analysis using NLTK and Scikit-learn
- **Daily Check-ins**: Track emotional well-being with confidence scores
- **Trend Visualization**: Interactive charts showing mood patterns over time
- **Personalized Feedback**: Tailored advice based on sentiment analysis

### 🤖 Medical Chatbot
- **Rule-based Assistant**: Provides information on common health concerns
- **Topics Covered**: Headache, fever, cold, diabetes, blood pressure, diet, exercise, sleep
- **Emergency Guidance**: Important medical emergency information
- **Conversation History**: Tracks all chatbot interactions

### 💧 Hydration Monitoring
- **Daily Tracking**: Log water intake with progress visualization
- **Personalized Goals**: Age-appropriate hydration recommendations
- **Progress Bars**: Visual feedback on daily hydration goals
- **Historical Analysis**: 7-day and 30-day hydration trends

### 📊 Comprehensive Reports
- **Health Dashboard**: Overview of all health metrics
- **Trend Analysis**: Visual representations of health patterns
- **Export Options**: Download health data in CSV format
- **Wellness Score**: Overall health assessment

### 👨‍💼 Admin Portal
- **Complete Management System**: Full administrative control
- **User Management**: View, activate, deactivate, and delete users
- **Mental Health Analytics**: Advanced sentiment analysis and user breakdown
- **Chatbot Management**: Monitor interactions and update settings
- **Hydration Monitoring**: Track user hydration patterns and alerts
- **Settings Management**: Configure application settings and content
- **Security Features**: Activity logging and access control

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.29.0
- **Machine Learning**: Scikit-learn 1.3.2
- **Natural Language Processing**: NLTK 3.8.1
- **Database**: SQLite
- **Data Processing**: Pandas 2.1.4, NumPy 1.24.4
- **Model Storage**: Joblib 1.3.2
- **Visualization**: Plotly 5.17.0
- **Image Processing**: Pillow 10.1.0
- **Security**: bcrypt 4.1.2

## 📁 Project Structure

```
/project_root
 ├── app.py                    # Main application entry point
 ├── requirements.txt          # Python dependencies
 ├── auth/                     # Authentication modules
 │    ├── login.py            # Login functionality
 │    └── signup.py           # User registration
 ├── modules/                  # Feature modules
 │    ├── mental_health.py    # Mental health monitoring
 │    ├── chatbot.py          # Medical chatbot
 │    ├── hydration.py        # Hydration tracking
 │    └── reports.py          # Health reports
 ├── ml/                       # Machine learning components
 │    ├── sentiment_model.py  # Sentiment analysis model
 │    └── model.pkl          # Trained model file
 ├── database/                 # Database components
 │    ├── db_setup.py        # Database initialization
 │    └── healthcare.db      # SQLite database
 ├── admin/                    # Admin portal modules
 │    ├── admin_login.py     # Admin authentication
 │    ├── admin_dashboard.py # Admin dashboard
 │    ├── user_management.py # User management
 │    ├── mental_health_admin.py # Mental health admin
 │    ├── chatbot_admin.py   # Chatbot management
 │    ├── hydration_admin.py # Hydration monitoring
 │    └── settings.py        # Settings management
 ├── assets/                   # Static assets
 │    ├── images/            # Application images
 │    └── icons/              # UI icons
 └── README.md                 # This file
```

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd senior-healthcare-app

# Or download and extract the project folder
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize the Database
```bash
cd database
python db_setup.py
```

### Step 4: Train the Sentiment Analysis Model
```bash
cd ml
python sentiment_model.py
```

### Step 5: Run the Application
```bash
# From the project root directory
streamlit run app.py
```

The application will open in your web browser at `http://localhost:8501`

## 📱 How to Use

### 1. Create an Account
- Click "Don't have an account? Sign Up"
- Enter your details (must be 60+ years old)
- Create a secure password

### 2. Login and Explore
- Use your credentials to login
- Navigate through the sidebar menu
- Access all features from the dashboard

### 3. Mental Health Tracking
- Go to "Mental Health" section
- Share how you're feeling
- View sentiment analysis and trends
- Get personalized feedback

### 4. Medical Chatbot
- Access the "Medical Chatbot"
- Ask health-related questions
- Get general medical information
- Remember: This doesn't replace professional medical advice

### 5. Hydration Tracking
- Log your daily water intake
- Monitor progress toward goals
- View hydration history and trends
- Get hydration reminders and tips

### 6. View Reports
- Check comprehensive health reports
- Analyze trends over different time periods
- Export your health data
- Monitor your wellness score

## 👨‍💼 Admin Portal Access

### Admin Login
1. Go to `http://localhost:8501`
2. Click "👨‍💼 Go to Admin Login"
3. Enter admin credentials
4. Access complete admin dashboard

### Admin Features
- **📊 Dashboard**: Real-time statistics and analytics
- **👥 User Management**: View, activate, deactivate, delete users
- **🧠 Mental Health Admin**: Sentiment analysis and user breakdown
- **🤖 Chatbot Admin**: Monitor interactions and update settings
- **💧 Hydration Admin**: Track user hydration and set alerts
- **⚙️ Settings**: Configure application settings and content

## 🎨 UI/UX Features

### Senior-Friendly Design
- **Large Fonts**: Easy-to-read text throughout the app
- **High Contrast**: Clear visual distinction between elements
- **Simple Navigation**: Intuitive sidebar menu
- **Large Buttons**: Easy-to-click interface elements
- **Visual Feedback**: Emojis and icons for better understanding
- **Minimal Text**: Concise, clear communication

### Accessibility Features
- **Color Coding**: Consistent color scheme for different sentiments
- **Progress Indicators**: Visual progress bars for goals
- **Clear Labels**: Descriptive button and section labels
- **Responsive Design**: Works on different screen sizes

## 🔒 Security Features

- **Password Hashing**: bcrypt encryption for user passwords
- **Session Management**: Secure session handling
- **Input Validation**: Form validation for all user inputs
- **Data Privacy**: Local database storage
- **SQL Injection Protection**: Parameterized queries
- **Admin Authentication**: Separate secure admin login
- **Activity Logging**: Complete audit trail for admin actions

## 📊 Data Storage

### Database Tables
- **users**: User account information
- **mental_health**: Mental health check-in records
- **hydration**: Water intake logs
- **chatbot_logs**: Chatbot conversation history
- **admins**: Admin account information
- **settings**: Application configuration
- **admin_logs**: Admin activity audit trail

### Data Privacy
- All data stored locally in SQLite database
- No external data transmission
- User data remains on the local machine

## 🧠 Machine Learning Model

### Sentiment Analysis
- **Algorithm**: Naive Bayes with TF-IDF vectorization
- **Training Data**: Curated dataset for senior mental health
- **Features**: Unigrams and bigrams
- **Performance**: Optimized for mental health text analysis

### Model Training
- Automated training on first run
- Model persistence with joblib
- Confidence scoring for predictions
- Real-time sentiment classification

## 🚨 Important Disclaimer

**This application is designed for general health monitoring and educational purposes only. It does not replace professional medical advice, diagnosis, or treatment.**

- Always consult with qualified healthcare providers for medical concerns
- In case of medical emergencies, call emergency services immediately
- The chatbot provides general information, not personalized medical advice
- Users should follow their healthcare provider's recommendations

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Error**: Run database setup
   ```bash
   cd database && python db_setup.py
   ```

3. **Model Not Found**: Train the sentiment model
   ```bash
   cd ml && python sentiment_model.py
   ```

4. **Port Already in Use**: Change Streamlit port
   ```bash
   streamlit run app.py --server.port 8502
   ```

5. **Admin Login Issues**: Check admin account exists
   ```bash
   python create_admin.py
   ```

6. **NLTK Data Missing**: Download required NLTK data
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

### Complete Setup Verification

If you encounter any issues, run this complete setup script:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
cd database
python db_setup.py
cd ..

# 3. Train ML model
cd ml
python sentiment_model.py
cd ..

# 4. Create admin account (if needed)
python create_admin.py

# 5. Run the application
streamlit run app.py
```

### Performance Tips
- Close unused browser tabs
- Restart the application if it becomes slow
- Clear browser cache if needed
- Ensure sufficient disk space for database

## 🤝 Contributing

This project is designed as a comprehensive healthcare solution for senior citizens. When contributing:

1. Maintain senior-friendly UI/UX principles
2. Ensure accessibility features are preserved
3. Test thoroughly with senior users in mind
4. Follow the existing code structure and style
5. Update documentation for any new features

## 📄 License

This project is open-source and available under the MIT License.

## 📞 Support

For technical support or questions:
- Check the troubleshooting section above
- Review the code comments for detailed explanations
- Ensure all dependencies are properly installed
- Verify database and model setup

---

**Built with ❤️ for senior citizens' health and well-being**
