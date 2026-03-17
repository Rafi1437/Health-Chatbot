"""
Integrated Mental Health, Medical Chatbot Assistance & Hydration Monitoring App for Senior Citizens
Main application entry point with navigation and session management
"""

import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

# Import modules
from auth.login import show_login, logout
from auth.signup import show_signup
from modules.mental_health import show_mental_health
from modules.chatbot import show_chatbot
from modules.hydration import show_hydration
from modules.reports import show_reports
from database.db_setup import create_database

# Import admin modules
from admin.admin_login import show_admin_login
from admin.admin_dashboard import show_admin_dashboard

def download_nltk_data():
    """Download required NLTK data for cloud deployment"""
    try:
        import nltk
        # Check if NLTK data exists
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger', quiet=True)
            
    except Exception as e:
        st.warning(f"NLTK data download issue: {e}")
        st.info("Please ensure internet connection for first-time setup")

def main():
    """Main application function"""
    
    # Configure page settings
    st.set_page_config(
        page_title="Senior Healthcare Assistant",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for senior-friendly UI
    st.markdown("""
    <style>
        .main {
            font-size: 18px;
        }
        .stButton > button {
            font-size: 18px;
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: bold;
        }
        .stSelectbox > div > div > select {
            font-size: 16px;
        }
        .stTextInput > div > input {
            font-size: 16px;
        }
        .stTextArea > div > textarea {
            font-size: 16px;
        }
        .metric-card {
            background-color: #f0f8ff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .sidebar-content {
            font-size: 16px;
        }
        h1 {
            font-size: 2.5rem;
            color: #2c3e50;
        }
        h2 {
            font-size: 2rem;
            color: #34495e;
        }
        h3 {
            font-size: 1.5rem;
            color: #34495e;
        }
        .admin-link {
            background-color: #dc3545;
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            margin: 10px 0;
            display: inline-block;
        }
        .admin-link:hover {
            background-color: #c82333;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Download NLTK data for cloud deployment
    download_nltk_data()
    
    # Create database if not exists
    create_database()
    
    # Navigation logic
    if st.session_state.get('admin_logged_in', False):
        # Admin is logged in
        show_admin_dashboard()
    elif st.session_state.get('logged_in', False):
        # Regular user is logged in
        show_main_app()
    else:
        # Show authentication pages
        show_auth_pages()

def initialize_session_state():
    """Initialize session state variables"""
    
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    
    if 'user_age' not in st.session_state:
        st.session_state.user_age = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'report_period' not in st.session_state:
        st.session_state.report_period = 30
    
    # Admin session state
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if 'admin_id' not in st.session_state:
        st.session_state.admin_id = None
    
    if 'admin_username' not in st.session_state:
        st.session_state.admin_username = None
    
    if 'admin_email' not in st.session_state:
        st.session_state.admin_email = None
    
    if 'admin_full_name' not in st.session_state:
        st.session_state.admin_full_name = None
    
    if 'admin_login_time' not in st.session_state:
        st.session_state.admin_login_time = None
    
    if 'admin_page' not in st.session_state:
        st.session_state.admin_page = 'dashboard'

def show_auth_pages():
    """Show authentication pages (login/signup)"""
    
    if st.session_state.page == 'login':
        # Add admin login link
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                '<div class="admin-link">🔐 Admin Login</div>',
                unsafe_allow_html=True
            )
            if st.button("👨‍💼 Go to Admin Login", key="admin_login_button", use_container_width=True):
                st.session_state.page = 'admin_login'
                st.rerun()
        
        show_login()
    elif st.session_state.page == 'signup':
        show_signup()
    elif st.session_state.page == 'admin_login':
        show_admin_login()
    else:
        st.session_state.page = 'login'
        show_login()

def show_main_app():
    """Show main application with navigation"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("# 🏥 Healthcare App")
        st.markdown("---")
        
        # User info
        st.markdown("### 👤 User Info")
        st.success(f"Welcome, {st.session_state.user_name}!")
        st.info(f"Age: {st.session_state.user_age}")
        st.markdown("---")
        
        # Navigation menu
        st.markdown("### 🧭 Navigation")
        
        if st.button("🏠 Home Dashboard", use_container_width=True, key="nav_dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        
        if st.button("🧠 Mental Health", use_container_width=True, key="nav_mental"):
            st.session_state.page = "mental_health"
            st.rerun()
        
        if st.button("🤖 Medical Chatbot", use_container_width=True, key="nav_chatbot"):
            st.session_state.page = "chatbot"
            st.rerun()
        
        if st.button("💧 Hydration Tracker", use_container_width=True, key="nav_hydration"):
            st.session_state.page = "hydration"
            st.rerun()
        
        if st.button("📊 Reports", use_container_width=True, key="nav_reports"):
            st.session_state.page = "reports"
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True, key="nav_logout"):
            logout()
    
    # Main content area
    if st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "mental_health":
        show_mental_health()
    elif st.session_state.page == "chatbot":
        show_chatbot()
    elif st.session_state.page == "hydration":
        show_hydration()
    elif st.session_state.page == "reports":
        show_reports()
    else:
        st.session_state.page = "dashboard"
        show_dashboard()

def show_dashboard():
    """Show home dashboard"""
    
    st.markdown("# 🏠 Welcome to Your Healthcare Dashboard")
    st.markdown(f"## Hello, {st.session_state.user_name}! 👋")
    
    # Welcome message
    st.markdown("""
    <div style="background-color: #e8f5e8; padding: 20px; border-radius: 15px; border-left: 5px solid #4caf50;">
        <h3>🌟 Welcome to your personal healthcare companion!</h3>
        <p>This app is designed to help you monitor your mental health, track your hydration, 
        and get medical assistance - all in one easy-to-use place.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    st.markdown("### 📊 Your Health at a Glance")
    
    # Get quick statistics
    stats = get_dashboard_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🧠 Mood Check-ins",
            stats['mental_health_entries'],
            "Last 7 days"
        )
    
    with col2:
        st.metric(
            "💧 Hydration Logs",
            stats['hydration_entries'],
            "Last 7 days"
        )
    
    with col3:
        st.metric(
            "🤖 Chat Sessions",
            stats['chatbot_entries'],
            "Last 7 days"
        )
    
    with col4:
        st.metric(
            "⭐ Wellness Score",
            f"{stats['wellness_score']}/100",
            "Overall health"
        )
    
    # Quick access cards
    st.markdown("### 🚀 Quick Access")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 15px; text-align: center;">
            <h3>🧠 Mental Health</h3>
            <p>Track your mood and emotional well-being</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Check In Now", use_container_width=True, key="dashboard_mental"):
            st.session_state.page = "mental_health"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background-color: #e6f3ff; padding: 20px; border-radius: 15px; text-align: center;">
            <h3>💧 Hydration</h3>
            <p>Monitor your daily water intake</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💧 Log Water", use_container_width=True, key="dashboard_hydration"):
            st.session_state.page = "hydration"
            st.rerun()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div style="background-color: #f8f0ff; padding: 20px; border-radius: 15px; text-align: center;">
            <h3>🤖 Medical Assistant</h3>
            <p>Get health advice and information</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💬 Ask Question", use_container_width=True, key="dashboard_chatbot"):
            st.session_state.page = "chatbot"
            st.rerun()
    
    with col4:
        st.markdown("""
        <div style="background-color: #fff0f5; padding: 20px; border-radius: 15px; text-align: center;">
            <h3>📊 Reports</h3>
            <p>View your health trends and progress</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📈 View Reports", use_container_width=True, key="dashboard_reports"):
            st.session_state.page = "reports"
            st.rerun()
    
    # Health tips
    st.markdown("### 💡 Daily Health Tips")
    
    tips = [
        "💧 Drink a glass of water when you wake up to start your day hydrated",
        "🚶 Take a short walk after meals to aid digestion",
        "😊 Practice gratitude by thinking of 3 things you're thankful for",
        "🥣 Include colorful fruits and vegetables in your meals",
        "😴 Aim for 7-8 hours of quality sleep each night",
        "📞 Stay connected with family and friends regularly"
    ]
    
    # Show random tips
    import random
    selected_tips = random.sample(tips, 3)
    
    for tip in selected_tips:
        st.info(tip)
    
    # Recent activity
    st.markdown("### 📋 Recent Activity")
    
    recent_activity = get_recent_activity()
    
    if recent_activity:
        for activity in recent_activity:
            st.write(f"• {activity}")
    else:
        st.info("No recent activity. Start using the app to see your health journey!")

def get_dashboard_stats():
    """Get dashboard statistics"""
    
    import sqlite3
    from datetime import datetime, timedelta
    
    stats = {
        'mental_health_entries': 0,
        'hydration_entries': 0,
        'chatbot_entries': 0,
        'wellness_score': 75  # Default score
    }
    
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get mental health entries (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM mental_health 
            WHERE user_id = ? AND timestamp >= date('now', '-7 days')
        """, (st.session_state.user_id,))
        stats['mental_health_entries'] = cursor.fetchone()[0]
        
        # Get hydration entries (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM hydration 
            WHERE user_id = ? AND timestamp >= date('now', '-7 days')
        """, (st.session_state.user_id,))
        stats['hydration_entries'] = cursor.fetchone()[0]
        
        # Get chatbot entries (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM chatbot_logs 
            WHERE user_id = ? AND timestamp >= date('now', '-7 days')
        """, (st.session_state.user_id,))
        stats['chatbot_entries'] = cursor.fetchone()[0]
        
        # Calculate wellness score
        if stats['mental_health_entries'] > 0:
            cursor.execute("""
                SELECT AVG(CASE WHEN sentiment = 'positive' THEN 100 
                          WHEN sentiment = 'neutral' THEN 50 
                          ELSE 0 END) as avg_sentiment
                FROM mental_health 
                WHERE user_id = ? AND timestamp >= date('now', '-7 days')
            """, (st.session_state.user_id,))
            
            result = cursor.fetchone()
            if result[0]:
                stats['wellness_score'] = int(result[0])
        
        conn.close()
        
    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
    
    return stats

def get_recent_activity():
    """Get recent user activity"""
    
    import sqlite3
    from datetime import datetime
    
    activities = []
    
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get recent mental health entries
        cursor.execute("""
            SELECT timestamp, sentiment FROM mental_health 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 2
        """, (st.session_state.user_id,))
        
        for row in cursor.fetchall():
            timestamp = datetime.fromisoformat(row[0])
            activities.append(f"🧠 Mood check-in ({row[1]}) - {timestamp.strftime('%b %d, %I:%M %p')}")
        
        # Get recent hydration entries
        cursor.execute("""
            SELECT timestamp, water_ml FROM hydration 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 2
        """, (st.session_state.user_id,))
        
        for row in cursor.fetchall():
            timestamp = datetime.fromisoformat(row[0])
            activities.append(f"💧 Logged {row[1]}ml water - {timestamp.strftime('%b %d, %I:%M %p')}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error getting recent activity: {e}")
    
    return activities[:5]  # Return only 5 most recent activities

if __name__ == "__main__":
    main()
