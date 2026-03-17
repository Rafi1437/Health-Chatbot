"""
Login module for Healthcare App
Handles user authentication
"""

import streamlit as st
import sqlite3
import os
from database.db_setup import verify_password

def show_login():
    """Display login page"""
    
    st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .stButton > button {
        background-color: #2196F3;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
    }
    .stTextInput > div > input {
        font-size: 16px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 🔐 Welcome Back")
    st.markdown("## Login to Your Healthcare Dashboard")
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="Enter your email address")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("🚀 Login", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("❌ Please enter both email and password")
                return
            
            # Check credentials
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, name, email, password, age FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()
            
            if user and verify_password(password, user[3]):
                # Set session state with proper data types
                st.session_state.user_id = int(user[0])
                st.session_state.user_name = user[1]
                st.session_state.user_email = user[2]
                st.session_state.user_age = int(user[4])  # Age is at index 4 (id, name, email, password, age)
                st.session_state.logged_in = True
                st.session_state.page = "dashboard"
                
                st.success(f"✅ Welcome back, {user[1]}!")
                st.balloons()
                
                # Redirect to dashboard
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid email or password")
    
    # Signup link
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("👤 Don't have an account? Sign Up", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()

def logout():
    """Logout user and clear session"""
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state.page = "login"
    st.rerun()
