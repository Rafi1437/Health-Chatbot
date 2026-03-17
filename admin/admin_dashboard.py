"""
Admin Dashboard Module for Senior Healthcare App
Main admin interface with summary cards and navigation
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys

# Import database functions
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.db_setup import log_admin_action, get_setting
from admin.admin_login import check_admin_session, admin_logout

def show_admin_dashboard():
    """Display main admin dashboard"""
    
    # Check admin authentication
    if not check_admin_session():
        return
    
    # Custom CSS for admin dashboard
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    .metric-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .stButton > button {
        background-color: #6f42c1;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }
    .logout-btn {
        background-color: #dc3545 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Dashboard Header
    st.markdown('<div class="dashboard-header">', unsafe_allow_html=True)
    st.markdown(f"# 🏥 Admin Dashboard")
    st.markdown(f"## Welcome, {st.session_state.admin_full_name}!")
    st.markdown(f"**Last Login:** {st.session_state.get('admin_login_time', 'N/A')}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Admin Sidebar Navigation
    with st.sidebar:
        st.markdown("### 🧭 Admin Navigation")
        
        if st.button("📊 Dashboard", use_container_width=True, key="nav_dashboard"):
            st.session_state.admin_page = "dashboard"
            st.rerun()
        
        if st.button("👥 Users", use_container_width=True, key="nav_users"):
            st.session_state.admin_page = "users"
            st.rerun()
        
        if st.button("🧠 Mental Health", use_container_width=True, key="nav_mental"):
            st.session_state.admin_page = "mental_health"
            st.rerun()
        
        if st.button("🤖 Chatbot", use_container_width=True, key="nav_chatbot"):
            st.session_state.admin_page = "chatbot"
            st.rerun()
        
        if st.button("💧 Hydration", use_container_width=True, key="nav_hydration"):
            st.session_state.admin_page = "hydration"
            st.rerun()
        
        if st.button("📈 Reports", use_container_width=True, key="nav_reports"):
            st.session_state.admin_page = "reports"
            st.rerun()
        
        if st.button("⚙️ Settings", use_container_width=True, key="nav_settings"):
            st.session_state.admin_page = "settings"
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True, key="nav_logout", help="Logout from admin panel"):
            admin_logout()
        
        # Admin info
        st.markdown("---")
        st.markdown("### 👤 Admin Info")
        st.info(f"**Username:** {st.session_state.admin_username}\n**Email:** {st.session_state.admin_email}")
    
    # Main Dashboard Content
    if st.session_state.get('admin_page') == 'dashboard':
        show_dashboard_content()
    elif st.session_state.get('admin_page') == 'users':
        from admin.user_management import show_user_management
        show_user_management()
    elif st.session_state.get('admin_page') == 'mental_health':
        from admin.mental_health_admin import show_mental_health_admin
        show_mental_health_admin()
    elif st.session_state.get('admin_page') == 'chatbot':
        from admin.chatbot_admin import show_chatbot_admin
        show_chatbot_admin()
    elif st.session_state.get('admin_page') == 'hydration':
        from admin.hydration_admin import show_hydration_admin
        show_hydration_admin()
    elif st.session_state.get('admin_page') == 'settings':
        from admin.settings import show_settings
        show_settings()
    else:
        show_dashboard_content()

def show_dashboard_content():
    """Display main dashboard content with metrics and charts"""
    
    # Get dashboard statistics
    stats = get_dashboard_statistics()
    
    # Summary Cards
    st.markdown("### 📊 System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("# 👥")
        st.markdown(f"## {stats['total_users']}")
        st.markdown("**Total Users**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("# 🧠")
        st.markdown(f"## {stats['mental_health_entries']}")
        st.markdown("**Mental Health Entries**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("# 🤖")
        st.markdown(f"## {stats['chatbot_interactions']}")
        st.markdown("**Chatbot Interactions**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("# 💧")
        st.markdown(f"## {stats['hydration_logs']}")
        st.markdown("**Hydration Logs**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Section
    st.markdown("### 📈 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # User Registration Trend
        st.markdown("#### 📊 User Registration Trend (Last 30 Days)")
        user_reg_chart = get_user_registration_chart()
        if user_reg_chart:
            st.plotly_chart(user_reg_chart, use_container_width=True)
        else:
            st.info("No user registration data available")
    
    with col2:
        # Mental Health Sentiment Distribution
        st.markdown("#### 🧠 Mental Health Sentiment Distribution")
        sentiment_chart = get_mental_health_sentiment_chart()
        if sentiment_chart:
            st.plotly_chart(sentiment_chart, use_container_width=True)
        else:
            st.info("No mental health data available")
    
    # Recent Activity
    st.markdown("### 📋 Recent Activity")
    
    recent_activity = get_recent_activity()
    
    if recent_activity:
        for activity in recent_activity[:5]:
            st.write(f"• {activity}")
    else:
        st.info("No recent activity found")
    
    # System Status
    st.markdown("### 🔧 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mental_health_enabled = get_setting('mental_health_enabled', '1')
        status = "🟢 Active" if mental_health_enabled == '1' else "🔴 Disabled"
        st.metric("🧠 Mental Health Module", status)
    
    with col2:
        chatbot_enabled = get_setting('chatbot_enabled', '1')
        status = "🟢 Active" if chatbot_enabled == '1' else "🔴 Disabled"
        st.metric("🤖 Chatbot Module", status)
    
    with col3:
        hydration_enabled = get_setting('hydration_enabled', '1')
        status = "🟢 Active" if hydration_enabled == '1' else "🔴 Disabled"
        st.metric("💧 Hydration Module", status)

def get_dashboard_statistics():
    """Get dashboard statistics"""
    
    stats = {
        'total_users': 0,
        'mental_health_entries': 0,
        'chatbot_interactions': 0,
        'hydration_logs': 0
    }
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Total users
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
        stats['total_users'] = cursor.fetchone()[0]
        
        # Mental health entries
        cursor.execute("SELECT COUNT(*) FROM mental_health")
        stats['mental_health_entries'] = cursor.fetchone()[0]
        
        # Chatbot interactions
        cursor.execute("SELECT COUNT(*) FROM chatbot_logs")
        stats['chatbot_interactions'] = cursor.fetchone()[0]
        
        # Hydration logs
        cursor.execute("SELECT COUNT(*) FROM hydration")
        stats['hydration_logs'] = cursor.fetchone()[0]
        
        conn.close()
        
    except Exception as e:
        st.error(f"Error fetching dashboard statistics: {e}")
    
    return stats

def get_user_registration_chart():
    """Get user registration trend chart"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM users 
        WHERE created_at >= date('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            fig = px.line(
                df,
                x='date',
                y='count',
                title='Daily User Registrations',
                labels={'date': 'Date', 'count': 'New Users'},
                markers=True
            )
            fig.update_layout(height=300)
            return fig
        
    except Exception as e:
        print(f"Error creating user registration chart: {e}")
    
    return None

def get_mental_health_sentiment_chart():
    """Get mental health sentiment distribution chart"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT sentiment, COUNT(*) as count
        FROM mental_health
        GROUP BY sentiment
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            fig = px.pie(
                df,
                values='count',
                names='sentiment',
                title='Sentiment Distribution',
                color_discrete_map={
                    'positive': '#28a745',
                    'neutral': '#ffc107',
                    'negative': '#dc3545'
                }
            )
            fig.update_layout(height=300)
            return fig
        
    except Exception as e:
        print(f"Error creating sentiment chart: {e}")
    
    return None

def get_recent_activity():
    """Get recent system activity"""
    
    activities = []
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        # Recent admin actions
        admin_query = """
        SELECT action, details, timestamp
        FROM admin_logs
        ORDER BY timestamp DESC
        LIMIT 5
        """
        
        cursor = conn.cursor()
        cursor.execute(admin_query)
        
        for row in cursor.fetchall():
            activities.append(f"👨‍💼 Admin: {row[0]} - {row[1] or ''} ({row[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"Error fetching recent activity: {e}")
    
    return activities
