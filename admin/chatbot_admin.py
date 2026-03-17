"""
Chatbot Admin Module
Manages chatbot interactions, responses, and settings
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import sys

# Import database functions
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.db_setup import log_admin_action, get_setting, update_setting
from admin.admin_login import check_admin_session

def show_chatbot_admin():
    """Display chatbot admin interface"""
    
    # Check admin authentication
    if not check_admin_session():
        return
    
    # Custom CSS
    st.markdown("""
    <style>
    .chat-message {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .user-message {
        border-left: 5px solid #007bff;
    }
    .bot-message {
        border-left: 5px solid #28a745;
    }
    .stButton > button {
        margin: 5px;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 14px;
    }
    .enable-btn {
        background-color: #28a745 !important;
        color: white !important;
    }
    .disable-btn {
        background-color: #dc3545 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 🤖 Chatbot Management")
    st.markdown("Monitor and manage medical chatbot interactions")
    
    # Chatbot Status
    st.markdown("### ⚙️ Chatbot Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chatbot_enabled = get_setting('chatbot_enabled', '1') == '1'
        
        if chatbot_enabled:
            st.success("🟢 Chatbot is currently **ENABLED**")
            if st.button("🔴 Disable Chatbot", key="disable_chatbot", help="Temporarily disable chatbot"):
                if update_setting('chatbot_enabled', '0'):
                    log_admin_action(
                        st.session_state.admin_id,
                        "CHATBOT_DISABLED",
                        "Chatbot module disabled by admin"
                    )
                    st.success("Chatbot disabled successfully!")
                    st.rerun()
        else:
            st.error("🔴 Chatbot is currently **DISABLED**")
            if st.button("🟢 Enable Chatbot", key="enable_chatbot", help="Enable chatbot module"):
                if update_setting('chatbot_enabled', '1'):
                    log_admin_action(
                        st.session_state.admin_id,
                        "CHATBOT_ENABLED",
                        "Chatbot module enabled by admin"
                    )
                    st.success("Chatbot enabled successfully!")
                    st.rerun()
    
    with col2:
        # Medical Disclaimer
        current_disclaimer = get_setting('medical_disclaimer', '')
        
        st.markdown("**Medical Disclaimer:**")
        new_disclaimer = st.text_area(
            "Update medical disclaimer message",
            value=current_disclaimer,
            height=100,
            help="This message will be shown to users in the chatbot"
        )
        
        if st.button("💾 Update Disclaimer", key="update_disclaimer"):
            if update_setting('medical_disclaimer', new_disclaimer):
                log_admin_action(
                    st.session_state.admin_id,
                    "DISCLAIMER_UPDATED",
                    "Medical disclaimer message updated"
                )
                st.success("Disclaimer updated successfully!")
            else:
                st.error("Failed to update disclaimer")
    
    # Chat Statistics
    st.markdown("### 📊 Chat Statistics")
    
    chat_stats = get_chatbot_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💬 Total Chats", chat_stats['total_chats'])
    
    with col2:
        st.metric("👥 Unique Users", chat_stats['unique_users'])
    
    with col3:
        st.metric("📅 Today's Chats", chat_stats['today_chats'])
    
    with col4:
        st.metric("📈 Avg Chats/User", f"{chat_stats['avg_chats_per_user']:.1f}")
    
    # Common Queries Analysis
    st.markdown("### 🔍 Common Queries Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Chat Volume Trend")
        volume_chart = get_chat_volume_chart()
        if volume_chart:
            st.plotly_chart(volume_chart, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔥 Top User Queries")
        top_queries = get_top_user_queries()
        if not top_queries.empty:
            st.dataframe(top_queries, use_container_width=True)
        else:
            st.info("No query data available")
    
    # Recent Chat Logs
    st.markdown("### 💬 Recent Chat Logs")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_filter = st.selectbox(
            "Date Range",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days"],
            key="chat_date_filter"
        )
    
    with col2:
        user_filter = st.text_input(
            "Search by User Email",
            placeholder="Enter user email...",
            key="chat_user_filter"
        )
    
    with col3:
        if st.button("🔄 Apply Filters", key="chat_apply_filters"):
            st.rerun()
    
    # Get chat logs
    chat_logs = get_chat_logs(date_filter, user_filter)
    
    if chat_logs.empty:
        st.info("No chat logs found matching the criteria.")
        return
    
    # Display chat logs
    st.markdown(f"#### 📋 Chat Logs ({len(chat_logs)} found)")
    
    # Pagination
    page_size = 10
    total_pages = (len(chat_logs) + page_size - 1) // page_size
    
    if total_pages > 1:
        page = st.selectbox("Page", range(1, total_pages + 1), key="chat_page")
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_logs = chat_logs.iloc[start_idx:end_idx]
    else:
        paginated_logs = chat_logs
    
    # Display conversations grouped by user and session
    current_user = None
    for _, log in paginated_logs.iterrows():
        if current_user != log['user_email']:
            current_user = log['user_email']
            st.markdown(f"---\n### 👤 {current_user}")
        
        # Display chat message
        st.markdown(f'<div class="chat-message user-message">', unsafe_allow_html=True)
        st.markdown(f"**👤 User ({log['timestamp'].strftime('%H:%M')}):** {log['user_message']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="chat-message bot-message">', unsafe_allow_html=True)
        st.markdown(f"**🤖 Bot ({log['timestamp'].strftime('%H:%M')}):** {log['bot_response']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export functionality
    st.markdown("### 📤 Export Chat Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Chat Logs", help="Export filtered chat logs to CSV"):
            csv_data = export_chat_logs_to_csv(chat_logs)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"chatbot_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Generate Analytics Report", help="Generate comprehensive chat analytics"):
            log_admin_action(
                st.session_state.admin_id,
                "CHATBOT_REPORT_GENERATED",
                f"Generated chatbot report with {len(chat_logs)} interactions"
            )
            st.success("Analytics report generated! Check downloads for the CSV file.")

def get_chatbot_statistics():
    """Get chatbot statistics"""
    
    stats = {
        'total_chats': 0,
        'unique_users': 0,
        'today_chats': 0,
        'avg_chats_per_user': 0.0
    }
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Total chats
        cursor.execute("SELECT COUNT(*) FROM chatbot_logs")
        stats['total_chats'] = cursor.fetchone()[0]
        
        # Unique users
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM chatbot_logs")
        stats['unique_users'] = cursor.fetchone()[0]
        
        # Today's chats
        cursor.execute("SELECT COUNT(*) FROM chatbot_logs WHERE date(timestamp) = date('now')")
        stats['today_chats'] = cursor.fetchone()[0]
        
        # Average chats per user
        if stats['unique_users'] > 0:
            stats['avg_chats_per_user'] = stats['total_chats'] / stats['unique_users']
        
        conn.close()
        
    except Exception as e:
        st.error(f"Error fetching chatbot statistics: {e}")
    
    return stats

def get_chat_volume_chart():
    """Create chat volume trend chart"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT DATE(timestamp) as date, COUNT(*) as chats
        FROM chatbot_logs
        WHERE timestamp >= date('now', '-30 days')
        GROUP BY DATE(timestamp)
        ORDER BY date
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            fig = px.line(
                df,
                x='date',
                y='chats',
                title='Daily Chat Volume (Last 30 Days)',
                labels={'date': 'Date', 'chats': 'Number of Chats'},
                markers=True
            )
            fig.update_layout(height=300)
            return fig
        
    except Exception as e:
        print(f"Error creating chat volume chart: {e}")
    
    return None

def get_top_user_queries():
    """Get top user queries"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT user_message, COUNT(*) as frequency
        FROM chatbot_logs
        WHERE timestamp >= date('now', '-30 days')
        GROUP BY user_message
        ORDER BY frequency DESC
        LIMIT 10
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df.columns = ['Query', 'Frequency']
            return df
        
    except Exception as e:
        print(f"Error fetching top queries: {e}")
    
    return pd.DataFrame()

def get_chat_logs(date_filter="Last 7 Days", user_filter=""):
    """Get filtered chat logs"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        # Date filter
        date_filter_sql = ""
        if date_filter == "Last 24 Hours":
            date_filter_sql = "AND timestamp >= datetime('now', '-24 hours')"
        elif date_filter == "Last 7 Days":
            date_filter_sql = "AND timestamp >= date('now', '-7 days')"
        elif date_filter == "Last 30 Days":
            date_filter_sql = "AND timestamp >= date('now', '-30 days')"
        
        # User filter
        user_filter_sql = ""
        params = []
        if user_filter:
            user_filter_sql = "AND u.email LIKE ?"
            params.append(f"%{user_filter}%")
        
        query = f"""
        SELECT 
            cl.id,
            cl.user_id,
            cl.user_message,
            cl.bot_response,
            cl.timestamp,
            u.name as user_name,
            u.email as user_email
        FROM chatbot_logs cl
        JOIN users u ON cl.user_id = u.id
        WHERE 1=1
        {date_filter_sql}
        {user_filter_sql}
        ORDER BY cl.timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        # Convert timestamp to datetime
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching chat logs: {e}")
        return pd.DataFrame()

def export_chat_logs_to_csv(data):
    """Export chat logs to CSV"""
    
    if data.empty:
        return "No data to export"
    
    # Select relevant columns
    export_data = data[[
        'timestamp', 'user_name', 'user_email',
        'user_message', 'bot_response'
    ]].copy()
    
    # Rename columns for better readability
    export_data.columns = [
        'Timestamp', 'User Name', 'User Email',
        'User Message', 'Bot Response'
    ]
    
    return export_data.to_csv(index=False)
