"""
Signup module for Healthcare App
Handles user registration with validation
"""

import streamlit as st
import sqlite3
import re
import os
from database.db_setup import hash_password, create_database

def show_signup():
    """Display signup page"""
    
    st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .stButton > button {
        background-color: #4CAF50;
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
    
    st.markdown("# 🏥 Create Your Account")
    st.markdown("## Join our Senior Healthcare Community")
    
    # Create database if not exists
    create_database()
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            age = st.number_input("🎂 Age", min_value=60, max_value=120, value=65)
        
        with col2:
            email = st.text_input("📧 Email", placeholder="Enter your email address")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
        
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
        
        submitted = st.form_submit_button("🚀 Sign Up", use_container_width=True)
        
        if submitted:
            if not name or not email or not password or not confirm_password:
                st.error("❌ Please fill in all fields")
                return
            
            if password != confirm_password:
                st.error("❌ Passwords do not match")
                return
            
            if len(password) < 6:
                st.error("❌ Password must be at least 6 characters long")
                return
            
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("❌ Please enter a valid email address")
                return
            
            if age < 60:
                st.error("❌ This app is designed for senior citizens (60+ years)")
                return
            
            # Check if user already exists
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                st.error("❌ An account with this email already exists")
                conn.close()
                return
            
            # Create new user
            hashed_password = hash_password(password)
            cursor.execute(
                "INSERT INTO users (name, email, password, age) VALUES (?, ?, ?, ?)",
                (name, email, hashed_password, age)
            )
            
            conn.commit()
            conn.close()
            
            st.success("✅ Account created successfully! Please login to continue.")
            st.balloons()
            
            # Redirect to login after 2 seconds
            import time
            time.sleep(2)
            st.session_state.page = "login"
            st.rerun()
    
    # Login link
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔑 Already have an account? Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
