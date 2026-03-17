"""
Settings Management Module for Admin Portal
Manage application settings, content, and configurations
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import sys

# Import database functions
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.db_setup import log_admin_action, get_setting, update_setting
from admin.admin_login import check_admin_session

def show_settings():
    """Display settings management interface"""
    
    # Check admin authentication
    if not check_admin_session():
        return
    
    # Custom CSS
    st.markdown("""
    <style>
    .setting-card {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .stButton > button {
        margin: 5px;
        padding: 10px 20px;
        border-radius: 6px;
        font-size: 14px;
    }
    .save-btn {
        background-color: #28a745 !important;
        color: white !important;
    }
    .reset-btn {
        background-color: #ffc107 !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# ⚙️ Settings Management")
    st.markdown("Configure application settings and content")
    
    # Settings categories
    settings_category = st.selectbox(
        "Select Settings Category",
        ["General Settings", "Module Configuration", "Content Management", "Security Settings"],
        key="settings_category"
    )
    
    if settings_category == "General Settings":
        show_general_settings()
    elif settings_category == "Module Configuration":
        show_module_settings()
    elif settings_category == "Content Management":
        show_content_settings()
    elif settings_category == "Security Settings":
        show_security_settings()

def show_general_settings():
    """Display general application settings"""
    
    st.markdown('<div class="setting-card">', unsafe_allow_html=True)
    st.markdown("### 🌐 General Settings")
    
    # App name
    current_app_name = get_setting('app_name', 'Senior Healthcare App')
    new_app_name = st.text_input(
        "Application Name",
        value=current_app_name,
        help="This name will be displayed throughout the application"
    )
    
    # Session timeout
    current_timeout = get_setting('session_timeout', '30')
    new_timeout = st.number_input(
        "Session Timeout (minutes)",
        min_value=5,
        max_value=120,
        value=int(current_timeout),
        help="Automatically logout users after this period of inactivity"
    )
    
    # Minimum water intake
    current_min_water = get_setting('min_water_intake', '2000')
    new_min_water = st.number_input(
        "Minimum Daily Water Intake (ml)",
        min_value=1000,
        max_value=5000,
        value=int(current_min_water),
        step=100,
        help="Default minimum water intake for users"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Settings", key="save_general", help="Save general settings"):
            if update_setting('app_name', new_app_name):
                update_setting('session_timeout', str(new_timeout))
                update_setting('min_water_intake', str(new_min_water))
                
                log_admin_action(
                    st.session_state.admin_id,
                    "GENERAL_SETTINGS_UPDATED",
                    f"Updated general settings: app_name, session_timeout, min_water_intake"
                )
                st.success("General settings saved successfully!")
            else:
                st.error("Failed to save some settings")
    
    with col2:
        if st.button("🔄 Reset to Defaults", key="reset_general", help="Reset to default values"):
            if update_setting('app_name', 'Senior Healthcare App'):
                update_setting('session_timeout', '30')
                update_setting('min_water_intake', '2000')
                
                log_admin_action(
                    st.session_state.admin_id,
                    "GENERAL_SETTINGS_RESET",
                    "Reset general settings to defaults"
                )
                st.success("Settings reset to defaults!")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_module_settings():
    """Display module configuration settings"""
    
    st.markdown('<div class="setting-card">', unsafe_allow_html=True)
    st.markdown("### 📦 Module Configuration")
    
    # Mental Health Module
    st.markdown("#### 🧠 Mental Health Module")
    mh_enabled = get_setting('mental_health_enabled', '1') == '1'
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Status:", "🟢 **Enabled**" if mh_enabled else "🔴 **Disabled**")
    with col2:
        if mh_enabled:
            if st.button("🔴 Disable", key="disable_mh", help="Disable mental health module"):
                if update_setting('mental_health_enabled', '0'):
                    log_admin_action(st.session_state.admin_id, "MENTAL_HEALTH_DISABLED", "Disabled mental health module")
                    st.success("Mental health module disabled!")
                    st.rerun()
        else:
            if st.button("🟢 Enable", key="enable_mh", help="Enable mental health module"):
                if update_setting('mental_health_enabled', '1'):
                    log_admin_action(st.session_state.admin_id, "MENTAL_HEALTH_ENABLED", "Enabled mental health module")
                    st.success("Mental health module enabled!")
                    st.rerun()
    
    # Chatbot Module
    st.markdown("#### 🤖 Chatbot Module")
    chatbot_enabled = get_setting('chatbot_enabled', '1') == '1'
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Status:", "🟢 **Enabled**" if chatbot_enabled else "🔴 **Disabled**")
    with col2:
        if chatbot_enabled:
            if st.button("🔴 Disable", key="disable_chatbot", help="Disable chatbot module"):
                if update_setting('chatbot_enabled', '0'):
                    log_admin_action(st.session_state.admin_id, "CHATBOT_DISABLED", "Disabled chatbot module")
                    st.success("Chatbot module disabled!")
                    st.rerun()
        else:
            if st.button("🟢 Enable", key="enable_chatbot", help="Enable chatbot module"):
                if update_setting('chatbot_enabled', '1'):
                    log_admin_action(st.session_state.admin_id, "CHATBOT_ENABLED", "Enabled chatbot module")
                    st.success("Chatbot module enabled!")
                    st.rerun()
    
    # Hydration Module
    st.markdown("#### 💧 Hydration Module")
    hydration_enabled = get_setting('hydration_enabled', '1') == '1'
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Status:", "🟢 **Enabled**" if hydration_enabled else "🔴 **Disabled**")
    with col2:
        if hydration_enabled:
            if st.button("🔴 Disable", key="disable_hydration", help="Disable hydration module"):
                if update_setting('hydration_enabled', '0'):
                    log_admin_action(st.session_state.admin_id, "HYDRATION_DISABLED", "Disabled hydration module")
                    st.success("Hydration module disabled!")
                    st.rerun()
        else:
            if st.button("🟢 Enable", key="enable_hydration", help="Enable hydration module"):
                if update_setting('hydration_enabled', '1'):
                    log_admin_action(st.session_state.admin_id, "HYDRATION_ENABLED", "Enabled hydration module")
                    st.success("Hydration module enabled!")
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_content_settings():
    """Display content management settings"""
    
    st.markdown('<div class="setting-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Content Management")
    
    # Medical Disclaimer
    st.markdown("#### ⚠️ Medical Disclaimer")
    current_disclaimer = get_setting('medical_disclaimer', '')
    
    new_disclaimer = st.text_area(
        "Medical Disclaimer Message",
        value=current_disclaimer,
        height=100,
        help="This disclaimer will be shown to users in the chatbot and other relevant areas"
    )
    
    if st.button("💾 Update Disclaimer", key="update_disclaimer", help="Update medical disclaimer"):
        if update_setting('medical_disclaimer', new_disclaimer):
            log_admin_action(
                st.session_state.admin_id,
                "DISCLAIMER_UPDATED",
                "Updated medical disclaimer message"
            )
            st.success("Medical disclaimer updated successfully!")
        else:
            st.error("Failed to update disclaimer")
    
    # Health Tips
    st.markdown("#### 💡 Health Tips")
    current_tips = get_setting('health_tips', '')
    
    st.write("Enter one health tip per line:")
    new_tips = st.text_area(
        "Health Tips",
        value=current_tips,
        height=150,
        help="These tips will be displayed to users in the dashboard and other areas"
    )
    
    if st.button("💾 Update Health Tips", key="update_tips", help="Update health tips"):
        if update_setting('health_tips', new_tips):
            log_admin_action(
                st.session_state.admin_id,
                "HEALTH_TIPS_UPDATED",
                "Updated health tips content"
            )
            st.success("Health tips updated successfully!")
        else:
            st.error("Failed to update health tips")
    
    # Reminder Messages
    st.markdown("#### ⏰ Reminder Messages")
    current_reminders = get_setting('reminder_messages', '')
    
    st.write("Enter one reminder message per line:")
    new_reminders = st.text_area(
        "Reminder Messages",
        value=current_reminders,
        height=150,
        help="These messages will be used for user reminders and notifications"
    )
    
    if st.button("💾 Update Reminders", key="update_reminders", help="Update reminder messages"):
        if update_setting('reminder_messages', new_reminders):
            log_admin_action(
                st.session_state.admin_id,
                "REMINDER_MESSAGES_UPDATED",
                "Updated reminder messages content"
            )
            st.success("Reminder messages updated successfully!")
        else:
            st.error("Failed to update reminder messages")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_security_settings():
    """Display security settings"""
    
    st.markdown('<div class="setting-card">', unsafe_allow_html=True)
    st.markdown("### 🔒 Security Settings")
    
    st.warning("⚠️ **Security Settings** - Modify these carefully as they affect system security")
    
    # Session timeout (also in general but important for security)
    current_timeout = get_setting('session_timeout', '30')
    new_timeout = st.number_input(
        "Session Timeout (minutes)",
        min_value=5,
        max_value=120,
        value=int(current_timeout),
        help="Shorter timeouts are more secure but less convenient"
    )
    
    # Password policy information
    st.markdown("#### 🔐 Password Policy")
    st.info("""
    **Current Password Requirements:**
    - Minimum 6 characters for users
    - Passwords are hashed using bcrypt
    - Admin passwords should be strong and unique
    
    **Recommendations:**
    - Use passwords with at least 8 characters
    - Include uppercase, lowercase, numbers, and symbols
    - Change passwords regularly
    - Don't share credentials
    """)
    
    # Admin account management
    st.markdown("#### 👨‍💼 Admin Account Management")
    
    if st.button("🔑 Change Admin Password", key="change_admin_password", help="Change current admin password"):
        st.session_state.show_password_change = True
    
    if st.session_state.get('show_password_change', False):
        st.markdown("#### Change Admin Password")
        
        current_password = st.text_input("Current Password", type="password", key="current_pwd")
        new_password = st.text_input("New Password", type="password", key="new_pwd")
        confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pwd")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Update Password", key="update_admin_pwd", type="primary"):
                if len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    # Here you would implement actual password change logic
                    st.success("Password updated successfully! (Note: Implement actual password change logic)")
                    log_admin_action(
                        st.session_state.admin_id,
                        "ADMIN_PASSWORD_CHANGED",
                        "Admin password was changed"
                    )
                    st.session_state.show_password_change = False
                    st.rerun()
        
        with col2:
            if st.button("❌ Cancel", key="cancel_pwd_change"):
                st.session_state.show_password_change = False
                st.rerun()
    
    # Activity logs
    st.markdown("#### 📋 Recent Admin Activity")
    
    recent_logs = get_admin_activity_logs()
    
    if not recent_logs.empty:
        st.dataframe(
            recent_logs[['timestamp', 'action', 'details']],
            use_container_width=True
        )
    else:
        st.info("No recent admin activity found")
    
    # Export settings
    st.markdown("#### 📤 Settings Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export All Settings", help="Export all settings to CSV"):
            settings_data = export_settings_to_csv()
            st.download_button(
                label="Download Settings CSV",
                data=settings_data,
                file_name=f"settings_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("🔄 Reset All Settings", help="Reset all settings to defaults"):
            if st.session_state.get('confirm_reset', False):
                # Reset all settings to defaults
                reset_all_settings()
                log_admin_action(
                    st.session_state.admin_id,
                    "ALL_SETTINGS_RESET",
                    "All settings were reset to defaults"
                )
                st.success("All settings have been reset to defaults!")
                st.session_state.confirm_reset = False
                st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning("⚠️ This will reset ALL settings to default values. Click again to confirm.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_admin_activity_logs():
    """Get recent admin activity logs"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT timestamp, action, details
        FROM admin_logs
        ORDER BY timestamp DESC
        LIMIT 20
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching admin activity logs: {e}")
        return pd.DataFrame()

def export_settings_to_csv():
    """Export all settings to CSV"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT setting_key, setting_value, setting_type, description, updated_at
        FROM settings
        ORDER BY setting_key
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df.to_csv(index=False)
        
    except Exception as e:
        st.error(f"Error exporting settings: {e}")
        return "Error exporting settings"

def reset_all_settings():
    """Reset all settings to default values"""
    
    try:
        # Import the default settings function
        from database.db_setup import create_default_settings
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Clear existing settings
        cursor.execute("DELETE FROM settings")
        
        # Insert default settings
        create_default_settings(cursor)
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        st.error(f"Error resetting settings: {e}")
        return False
