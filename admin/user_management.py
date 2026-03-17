"""
User Management Module for Admin Portal
Handles user viewing, activation, deactivation, and deletion
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import sys

# Import database functions
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.db_setup import log_admin_action
from admin.admin_login import check_admin_session

def show_user_management():
    """Display user management interface"""
    
    # Check admin authentication
    if not check_admin_session():
        return
    
    # Custom CSS
    st.markdown("""
    <style>
    .user-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .active-user {
        border-left: 5px solid #28a745;
    }
    .inactive-user {
        border-left: 5px solid #dc3545;
    }
    .stButton > button {
        margin: 5px;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 14px;
    }
    .activate-btn {
        background-color: #28a745 !important;
        color: white !important;
    }
    .deactivate-btn {
        background-color: #ffc107 !important;
        color: black !important;
    }
    .delete-btn {
        background-color: #dc3545 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 👥 User Management")
    st.markdown("Manage all registered users in the system")
    
    # Filters
    st.markdown("### 🔍 Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "User Status",
            ["All", "Active", "Inactive"],
            key="user_status_filter"
        )
    
    with col2:
        age_filter = st.selectbox(
            "Age Group",
            ["All", "60-70", "71-80", "81+"],
            key="age_filter"
        )
    
    with col3:
        search_term = st.text_input(
            "Search Users",
            placeholder="Search by name or email...",
            key="user_search"
        )
    
    # Get users data
    users_df = get_users_data(status_filter, age_filter, search_term)
    
    if users_df.empty:
        st.info("No users found matching the criteria.")
        return
    
    # Display users
    st.markdown(f"### 📋 Registered Users ({len(users_df)} found)")
    
    for _, user in users_df.iterrows():
        status_class = "active-user" if user['is_active'] == 1 else "inactive-user"
        status_text = "🟢 Active" if user['is_active'] == 1 else "🔴 Inactive"
        
        st.markdown(f'<div class="user-card {status_class}">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{user['name']}**")
            st.write(f"📧 {user['email']}")
            st.write(f"🎂 Age: {user['age']} years")
            st.write(f"📅 Registered: {user['created_at']}")
            st.write(f"📊 Status: {status_text}")
        
        with col2:
            # User statistics
            user_stats = get_user_statistics(user['id'])
            st.markdown("**User Activity:**")
            st.write(f"🧠 Mental Health: {user_stats['mental_health_entries']}")
            st.write(f"🤖 Chatbot: {user_stats['chatbot_interactions']}")
            st.write(f"💧 Hydration: {user_stats['hydration_logs']}")
        
        with col3:
            # Action buttons
            if user['is_active'] == 1:
                if st.button("🔒 Deactivate", key=f"deactivate_{user['id']}", help="Deactivate user account"):
                    if toggle_user_status(user['id'], 0):
                        st.success(f"User {user['name']} deactivated successfully!")
                        log_admin_action(
                            st.session_state.admin_id,
                            "USER_DEACTIVATED",
                            f"Deactivated user: {user['name']} ({user['email']})"
                        )
                        st.rerun()
            else:
                if st.button("✅ Activate", key=f"activate_{user['id']}", help="Activate user account"):
                    if toggle_user_status(user['id'], 1):
                        st.success(f"User {user['name']} activated successfully!")
                        log_admin_action(
                            st.session_state.admin_id,
                            "USER_ACTIVATED",
                            f"Activated user: {user['name']} ({user['email']})"
                        )
                        st.rerun()
            
            # Delete button with confirmation
            if st.button("🗑️ Delete", key=f"delete_{user['id']}", help="Delete user account permanently"):
                st.session_state[f"confirm_delete_{user['id']}"] = True
            
            # Confirmation dialog
            if st.session_state.get(f"confirm_delete_{user['id']}", False):
                st.warning(f"⚠️ Are you sure you want to delete {user['name']}? This action cannot be undone!")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, Delete", key=f"confirm_yes_{user['id']}", type="primary"):
                        if delete_user(user['id']):
                            st.success(f"User {user['name']} deleted successfully!")
                            log_admin_action(
                                st.session_state.admin_id,
                                "USER_DELETED",
                                f"Deleted user: {user['name']} ({user['email']})"
                            )
                            st.rerun()
                with col2:
                    if st.button("❌ Cancel", key=f"confirm_no_{user['id']}"):
                        st.session_state[f"confirm_delete_{user['id']}"] = False
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export functionality
    st.markdown("### 📤 Export User Data")
    
    if st.button("📥 Export Users to CSV", help="Export all users data to CSV file"):
        csv_data = export_users_to_csv(users_df)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def get_users_data(status_filter="All", age_filter="All", search_term=""):
    """Get filtered users data"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT id, name, email, age, is_active, created_at
        FROM users
        WHERE 1=1
        """
        params = []
        
        # Status filter
        if status_filter == "Active":
            query += " AND is_active = 1"
        elif status_filter == "Inactive":
            query += " AND is_active = 0"
        
        # Age filter
        if age_filter == "60-70":
            query += " AND age BETWEEN 60 AND 70"
        elif age_filter == "71-80":
            query += " AND age BETWEEN 71 AND 80"
        elif age_filter == "81+":
            query += " AND age >= 81"
        
        # Search filter
        if search_term:
            query += " AND (name LIKE ? OR email LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        query += " ORDER BY created_at DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching users data: {e}")
        return pd.DataFrame()

def get_user_statistics(user_id):
    """Get statistics for a specific user"""
    
    stats = {
        'mental_health_entries': 0,
        'chatbot_interactions': 0,
        'hydration_logs': 0
    }
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Mental health entries
        cursor.execute("SELECT COUNT(*) FROM mental_health WHERE user_id = ?", (user_id,))
        stats['mental_health_entries'] = cursor.fetchone()[0]
        
        # Chatbot interactions
        cursor.execute("SELECT COUNT(*) FROM chatbot_logs WHERE user_id = ?", (user_id,))
        stats['chatbot_interactions'] = cursor.fetchone()[0]
        
        # Hydration logs
        cursor.execute("SELECT COUNT(*) FROM hydration WHERE user_id = ?", (user_id,))
        stats['hydration_logs'] = cursor.fetchone()[0]
        
        conn.close()
        
    except Exception as e:
        print(f"Error fetching user statistics: {e}")
    
    return stats

def toggle_user_status(user_id, status):
    """Toggle user active status"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE users SET is_active = ? WHERE id = ?", (status, user_id))
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        st.error(f"Error updating user status: {e}")
        return False

def delete_user(user_id):
    """Delete user and all related data"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete user data in order (respecting foreign keys)
        cursor.execute("DELETE FROM mental_health WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM chatbot_logs WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM hydration WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        st.error(f"Error deleting user: {e}")
        return False

def export_users_to_csv(users_df):
    """Export users data to CSV format"""
    
    # Add user statistics to each user
    export_data = []
    
    for _, user in users_df.iterrows():
        stats = get_user_statistics(user['id'])
        
        export_data.append({
            'ID': user['id'],
            'Name': user['name'],
            'Email': user['email'],
            'Age': user['age'],
            'Status': 'Active' if user['is_active'] == 1 else 'Inactive',
            'Registration Date': user['created_at'],
            'Mental Health Entries': stats['mental_health_entries'],
            'Chatbot Interactions': stats['chatbot_interactions'],
            'Hydration Logs': stats['hydration_logs']
        })
    
    export_df = pd.DataFrame(export_data)
    return export_df.to_csv(index=False)
