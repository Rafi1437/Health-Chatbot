"""
Hydration Admin Module
Manages hydration monitoring data and analytics
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
from database.db_setup import log_admin_action, get_setting, update_setting
from admin.admin_login import check_admin_session

def show_hydration_admin():
    """Display hydration admin interface"""
    
    # Check admin authentication
    if not check_admin_session():
        return
    
    # Custom CSS
    st.markdown("""
    <style>
    .hydration-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .good-hydration {
        border-left: 5px solid #28a745;
    }
    .poor-hydration {
        border-left: 5px solid #dc3545;
    }
    .moderate-hydration {
        border-left: 5px solid #ffc107;
    }
    .stButton > button {
        margin: 5px;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 💧 Hydration Management")
    st.markdown("Monitor and analyze hydration data across all users")
    
    # Hydration Settings
    st.markdown("### ⚙️ Hydration Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hydration_enabled = get_setting('hydration_enabled', '1') == '1'
        
        if hydration_enabled:
            st.success("🟢 Hydration tracking is currently **ENABLED**")
            if st.button("🔴 Disable Hydration", key="disable_hydration", help="Temporarily disable hydration tracking"):
                if update_setting('hydration_enabled', '0'):
                    log_admin_action(
                        st.session_state.admin_id,
                        "HYDRATION_DISABLED",
                        "Hydration tracking disabled by admin"
                    )
                    st.success("Hydration tracking disabled successfully!")
                    st.rerun()
        else:
            st.error("🔴 Hydration tracking is currently **DISABLED**")
            if st.button("🟢 Enable Hydration", key="enable_hydration", help="Enable hydration tracking"):
                if update_setting('hydration_enabled', '1'):
                    log_admin_action(
                        st.session_state.admin_id,
                        "HYDRATION_ENABLED",
                        "Hydration tracking enabled by admin"
                    )
                    st.success("Hydration tracking enabled successfully!")
                    st.rerun()
    
    with col2:
        # Minimum water intake setting
        current_min_intake = get_setting('min_water_intake', '2000')
        
        st.markdown("**Minimum Daily Water Intake (ml):**")
        new_min_intake = st.number_input(
            "Update minimum intake",
            min_value=1000,
            max_value=5000,
            value=int(current_min_intake),
            step=100,
            key="min_water_intake"
        )
        
        if st.button("💾 Update Minimum", key="update_min_intake"):
            if update_setting('min_water_intake', str(new_min_intake)):
                log_admin_action(
                    st.session_state.admin_id,
                    "MIN_WATER_INTAKE_UPDATED",
                    f"Minimum water intake updated to {new_min_intake}ml"
                )
                st.success("Minimum water intake updated successfully!")
            else:
                st.error("Failed to update minimum water intake")
    
    # Hydration Statistics
    st.markdown("### 📊 Hydration Statistics")
    
    hydration_stats = get_hydration_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💧 Total Logs", hydration_stats['total_logs'])
    
    with col2:
        st.metric("👥 Active Users", hydration_stats['active_users'])
    
    with col3:
        st.metric("📅 Today's Logs", hydration_stats['today_logs'])
    
    with col4:
        st.metric("📈 Avg Daily Intake", f"{hydration_stats['avg_daily_intake']:.0f}ml")
    
    # Hydration Analytics
    st.markdown("### 📈 Hydration Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily intake trend
        st.markdown("#### 📊 Daily Intake Trend")
        intake_chart = get_daily_intake_chart()
        if intake_chart:
            st.plotly_chart(intake_chart, use_container_width=True)
    
    with col2:
        # Goal achievement rate
        st.markdown("#### 🎯 Goal Achievement Rate")
        achievement_chart = get_goal_achievement_chart()
        if achievement_chart:
            st.plotly_chart(achievement_chart, use_container_width=True)
    
    # Low Hydration Users Alert
    st.markdown("### ⚠️ Low Hydration Alert")
    
    low_hydration_users = get_low_hydration_users()
    
    if not low_hydration_users.empty:
        st.warning(f"Found {len(low_hydration_users)} users with consistently low water intake")
        
        for _, user in low_hydration_users.iterrows():
            with st.expander(f"👤 {user['name']} ({user['email']}) - Avg: {user['avg_intake']:.0f}ml/day"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("💧 Avg Daily Intake", f"{user['avg_intake']:.0f}ml")
                
                with col2:
                    st.metric("🎯 Goal Achievement", f"{user['achievement_rate']:.1f}%")
                
                with col3:
                    st.metric("📅 Total Logs", user['total_logs'])
                
                # Recent hydration logs
                st.markdown("**Recent Activity:**")
                recent_logs = get_user_hydration_logs(user['user_id'], limit=5)
                
                for _, log in recent_logs.iterrows():
                    achievement = (log['water_ml'] / log['recommended_ml']) * 100
                    status = "🟢" if achievement >= 100 else "🟡" if achievement >= 75 else "🔴"
                    
                    # Handle timestamp formatting safely
                    try:
                        timestamp_str = log['timestamp'].strftime('%Y-%m-%d %H:%M')
                    except (AttributeError, ValueError):
                        # If timestamp is not a datetime object, convert it first
                        if isinstance(log['timestamp'], str):
                            timestamp_str = log['timestamp']  # Use as-is if it's a string
                        else:
                            timestamp_str = str(log['timestamp'])  # Convert to string as fallback
                    
                    st.write(f"{status} {timestamp_str}: {log['water_ml']}ml ({achievement:.0f}% of goal)")
    else:
        st.success("🎉 All users are maintaining good hydration levels!")
    
    # Detailed Hydration Logs
    st.markdown("### 📋 Detailed Hydration Logs")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_filter = st.selectbox(
            "Date Range",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days"],
            key="hydration_date_filter"
        )
    
    with col2:
        achievement_filter = st.selectbox(
            "Goal Achievement",
            ["All", "Met Goal", "Below Goal"],
            key="hydration_achievement_filter"
        )
    
    with col3:
        user_filter = st.text_input(
            "Search by User Email",
            placeholder="Enter user email...",
            key="hydration_user_filter"
        )
    
    if st.button("🔄 Apply Filters", key="hydration_apply_filters"):
        st.rerun()
    
    # Get hydration logs
    hydration_logs = get_hydration_logs(date_filter, achievement_filter, user_filter)
    
    if hydration_logs.empty:
        st.info("No hydration logs found matching the criteria.")
        return
    
    st.markdown(f"#### 📋 Hydration Logs ({len(hydration_logs)} found)")
    
    # Pagination
    page_size = 20
    total_pages = (len(hydration_logs) + page_size - 1) // page_size
    
    if total_pages > 1:
        page = st.selectbox("Page", range(1, total_pages + 1), key="hydration_page")
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_logs = hydration_logs.iloc[start_idx:end_idx]
    else:
        paginated_logs = hydration_logs
    
    # Display logs
    for _, log in paginated_logs.iterrows():
        achievement = (log['water_ml'] / log['recommended_ml']) * 100
        
        if achievement >= 100:
            card_class = "hydration-card good-hydration"
            status = "🟢 Goal Met"
        elif achievement >= 75:
            card_class = "hydration-card moderate-hydration"
            status = "🟡 Close to Goal"
        else:
            card_class = "hydration-card poor-hydration"
            status = "🔴 Below Goal"
        
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown(f"**{log['user_name']}**")
            st.write(f"📧 {log['user_email']}")
            
            # Handle timestamp formatting safely
            try:
                timestamp_str = log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            except (AttributeError, ValueError):
                # If timestamp is not a datetime object, convert it first
                if isinstance(log['timestamp'], str):
                    timestamp_str = log['timestamp']  # Use as-is if it's a string
                else:
                    timestamp_str = str(log['timestamp'])  # Convert to string as fallback
            
            st.write(f"🕒 {timestamp_str}")
        
        with col2:
            st.metric("💧 Water Intake", f"{log['water_ml']}ml")
        
        with col3:
            st.metric("🎯 Recommended", f"{log['recommended_ml']}ml")
        
        with col4:
            st.metric("📊 Achievement", f"{achievement:.0f}%")
            st.write(status)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export functionality
    st.markdown("### 📤 Export Hydration Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export to CSV", help="Export filtered hydration data"):
            csv_data = export_hydration_to_csv(hydration_logs)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"hydration_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Generate Hydration Report", help="Generate comprehensive hydration report"):
            log_admin_action(
                st.session_state.admin_id,
                "HYDRATION_REPORT_GENERATED",
                f"Generated hydration report with {len(hydration_logs)} entries"
            )
            st.success("Hydration report generated! Check downloads for the CSV file.")

def get_hydration_statistics():
    """Get hydration statistics"""
    
    stats = {
        'total_logs': 0,
        'active_users': 0,
        'today_logs': 0,
        'avg_daily_intake': 0.0
    }
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Total logs
        cursor.execute("SELECT COUNT(*) FROM hydration")
        stats['total_logs'] = cursor.fetchone()[0]
        
        # Active users (users with hydration logs in last 7 days)
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM hydration 
            WHERE timestamp >= date('now', '-7 days')
        """)
        stats['active_users'] = cursor.fetchone()[0]
        
        # Today's logs
        cursor.execute("SELECT COUNT(*) FROM hydration WHERE date(timestamp) = date('now')")
        stats['today_logs'] = cursor.fetchone()[0]
        
        # Average daily intake
        cursor.execute("""
            SELECT AVG(water_ml) 
            FROM hydration 
            WHERE timestamp >= date('now', '-7 days')
        """)
        result = cursor.fetchone()
        stats['avg_daily_intake'] = result[0] if result[0] else 0
        
        conn.close()
        
    except Exception as e:
        st.error(f"Error fetching hydration statistics: {e}")
    
    return stats

def get_daily_intake_chart():
    """Create daily intake trend chart"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT DATE(timestamp) as date, AVG(water_ml) as avg_intake, AVG(recommended_ml) as avg_recommended
        FROM hydration
        WHERE timestamp >= date('now', '-30 days')
        GROUP BY DATE(timestamp)
        ORDER BY date
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['avg_intake'],
                mode='lines+markers',
                name='Average Intake',
                line=dict(color='blue', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['avg_recommended'],
                mode='lines',
                name='Recommended',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title='Average Daily Water Intake (Last 30 Days)',
                xaxis_title='Date',
                yaxis_title='Water Intake (ml)',
                height=300
            )
            
            return fig
        
    except Exception as e:
        print(f"Error creating daily intake chart: {e}")
    
    return None

def get_goal_achievement_chart():
    """Create goal achievement rate chart"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT DATE(timestamp) as date,
               AVG(CASE WHEN water_ml >= recommended_ml THEN 100.0 
                    ELSE (water_ml * 100.0 / recommended_ml) END) as achievement_rate
        FROM hydration
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
                y='achievement_rate',
                title='Daily Goal Achievement Rate',
                labels={'date': 'Date', 'achievement_rate': 'Achievement Rate (%)'},
                markers=True
            )
            
            fig.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="100% Goal")
            fig.add_hline(y=75, line_dash="dash", line_color="orange", annotation_text="75% Warning")
            
            fig.update_layout(height=300)
            return fig
        
    except Exception as e:
        print(f"Error creating goal achievement chart: {e}")
    
    return None

def get_low_hydration_users():
    """Get users with consistently low hydration"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT 
            u.id as user_id,
            u.name,
            u.email,
            AVG(h.water_ml) as avg_intake,
            AVG(h.recommended_ml) as avg_recommended,
            COUNT(h.id) as total_logs,
            AVG(CASE WHEN h.water_ml >= h.recommended_ml THEN 100.0 
                 ELSE (h.water_ml * 100.0 / h.recommended_ml) END) as achievement_rate
        FROM users u
        JOIN hydration h ON u.id = h.user_id
        WHERE h.timestamp >= date('now', '-7 days')
        GROUP BY u.id, u.name, u.email
        HAVING achievement_rate < 75
        ORDER BY achievement_rate ASC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
        
    except Exception as e:
        print(f"Error fetching low hydration users: {e}")
        return pd.DataFrame()

def get_user_hydration_logs(user_id, limit=10):
    """Get hydration logs for a specific user"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT timestamp, water_ml, recommended_ml
        FROM hydration
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """
        
        df = pd.read_sql_query(query, conn, params=(user_id, limit))
        conn.close()
        
        # Convert timestamp to datetime
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
        
    except Exception as e:
        print(f"Error fetching user hydration logs: {e}")
        return pd.DataFrame()

def get_hydration_logs(date_filter="Last 7 Days", achievement_filter="All", user_filter=""):
    """Get filtered hydration logs"""
    
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
        
        # Achievement filter
        achievement_filter_sql = ""
        if achievement_filter == "Met Goal":
            achievement_filter_sql = "AND h.water_ml >= h.recommended_ml"
        elif achievement_filter == "Below Goal":
            achievement_filter_sql = "AND h.water_ml < h.recommended_ml"
        
        # User filter
        user_filter_sql = ""
        params = []
        if user_filter:
            user_filter_sql = "AND u.email LIKE ?"
            params.append(f"%{user_filter}%")
        
        query = f"""
        SELECT 
            h.id,
            h.user_id,
            h.water_ml,
            h.recommended_ml,
            h.timestamp,
            u.name as user_name,
            u.email as user_email
        FROM hydration h
        JOIN users u ON h.user_id = u.id
        WHERE 1=1
        {date_filter_sql}
        {achievement_filter_sql}
        {user_filter_sql}
        ORDER BY h.timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        # Convert timestamp to datetime
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching hydration logs: {e}")
        return pd.DataFrame()

def export_hydration_to_csv(data):
    """Export hydration data to CSV"""
    
    if data.empty:
        return "No data to export"
    
    # Select relevant columns
    export_data = data[[
        'timestamp', 'user_name', 'user_email',
        'water_ml', 'recommended_ml'
    ]].copy()
    
    # Calculate achievement percentage
    export_data['achievement_percentage'] = (export_data['water_ml'] / export_data['recommended_ml']) * 100
    
    # Rename columns for better readability
    export_data.columns = [
        'Timestamp', 'User Name', 'User Email',
        'Water Intake (ml)', 'Recommended Intake (ml)', 'Achievement (%)'
    ]
    
    return export_data.to_csv(index=False)
