"""
Admin Login Module for Senior Healthcare App
Handles admin authentication and session management
"""

import streamlit as st
import sqlite3
import re
import os
import sys
from datetime import datetime

# Import database functions
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.db_setup import verify_password, log_admin_action

def show_admin_login():
    """Display admin login page"""
    
    # Custom CSS for admin login
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .admin-login {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: 50px auto;
    }
    .stButton > button {
        background-color: #dc3545;
        color: white;
        font-size: 18px;
        padding: 12px 24px;
        border-radius: 8px;
        width: 100%;
        margin-top: 20px;
    }
    .stTextInput > div > input {
        font-size: 16px;
        padding: 12px;
        border: 2px solid #dee2e6;
        border-radius: 8px;
    }
    .admin-header {
        text-align: center;
        color: #dc3545;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if already logged in as admin
    if st.session_state.get('admin_logged_in', False):
        st.warning("You are already logged in as admin.")
        if st.button("Go to Admin Dashboard"):
            st.session_state.page = "admin_dashboard"
            st.rerun()
        return
    
    st.markdown('<div class="admin-login">', unsafe_allow_html=True)
    
    st.markdown('<div class="admin-header">', unsafe_allow_html=True)
    st.markdown("# 🔐 Admin Login")
    st.markdown("## Senior Healthcare App")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form("admin_login_form"):
        username = st.text_input(
            "👤 Username",
            placeholder="Enter admin username",
            help="Enter your administrator username"
        )
        
        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter admin password",
            help="Enter your administrator password"
        )
        
        submitted = st.form_submit_button("🚀 Login to Admin Panel", use_container_width=True)
        
        if submitted:
            if not username or not password:
                st.error("❌ Please enter both username and password")
                return
            
            # Validate input
            if len(username) < 3:
                st.error("❌ Username must be at least 3 characters")
                return
            
            if len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
                return
            
            # Authenticate admin
            if authenticate_admin(username, password):
                st.success("✅ Login successful! Redirecting to admin dashboard...")
                st.balloons()
                
                # Redirect to admin dashboard
                import time
                time.sleep(2)
                st.session_state.page = "admin_dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back to user app
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Back to User App", use_container_width=True):
            st.session_state.page = "login"
            st.session_state.admin_logged_in = False
            st.rerun()

def authenticate_admin(username, password):
    """Authenticate admin credentials"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get admin by username
        cursor.execute("""
            SELECT id, username, email, password, full_name, is_active 
            FROM admins 
            WHERE username = ?
        """, (username,))
        
        admin = cursor.fetchone()
        conn.close()
        
        if admin and admin[5] == 1:  # Check if admin is active
            if verify_password(password, admin[3]):
                # Set admin session state
                st.session_state.admin_logged_in = True
                st.session_state.admin_id = admin[0]
                st.session_state.admin_username = admin[1]
                st.session_state.admin_email = admin[2]
                st.session_state.admin_full_name = admin[4]
                st.session_state.admin_login_time = datetime.now()
                
                # Update last login
                update_admin_last_login(admin[0])
                
                # Log admin action
                log_admin_action(admin[0], "LOGIN", f"Admin {username} logged in")
                
                return True
        
        return False
        
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False

def update_admin_last_login(admin_id):
    """Update admin's last login timestamp"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE admins 
            SET last_login = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id,))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error updating admin last login: {e}")

def check_admin_session():
    """Check if admin session is valid"""
    
    if not st.session_state.get('admin_logged_in', False):
        return False
    
    # Check session timeout (30 minutes default)
    try:
        from database.db_setup import get_setting
        session_timeout = int(get_setting('session_timeout', '30'))
    except:
        session_timeout = 30  # Default fallback
    
    login_time = st.session_state.get('admin_login_time')
    
    if login_time:
        elapsed = (datetime.now() - login_time).total_seconds() / 60
        if elapsed > session_timeout:
            # Session expired
            admin_logout()
            st.error("Session expired. Please login again.")
            return False
    
    return True

def admin_logout():
    """Logout admin and clear session"""
    
    if st.session_state.get('admin_logged_in', False):
        admin_id = st.session_state.get('admin_id')
        username = st.session_state.get('admin_username')
        
        # Log admin action
        if admin_id:
            log_admin_action(admin_id, "LOGOUT", f"Admin {username} logged out")
    
    # Clear admin session state
    admin_keys = [
        'admin_logged_in', 'admin_id', 'admin_username', 
        'admin_email', 'admin_full_name', 'admin_login_time'
    ]
    
    for key in admin_keys:
        if key in st.session_state:
            del st.session_state[key]
    
    # Redirect to admin login
    st.session_state.page = "admin_login"
    st.rerun()

def require_admin_auth():
    """Decorator to require admin authentication"""
    
    if not check_admin_session():
        st.session_state.page = "admin_login"
        st.rerun()
    
    return True
