"""
Mental Health Admin Module
Manages mental health data, analytics, and insights
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
from database.db_setup import log_admin_action
from admin.admin_login import check_admin_session

def show_mental_health_admin():
    """Display mental health admin interface"""
    
    # Check admin authentication
    if not check_admin_session():
        return
    
    # Custom CSS
    st.markdown("""
    <style>
    .sentiment-positive {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
    .sentiment-neutral {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
    .sentiment-negative {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin: 10px 0;
    }
    .stButton > button {
        margin: 5px;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 🧠 Mental Health Management")
    st.markdown("Monitor and analyze mental health data across all users")
    
    # Filters
    st.markdown("### 🔍 Filters")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sentiment_filter = st.selectbox(
            "Sentiment",
            ["All", "Positive", "Neutral", "Negative"],
            key="mh_sentiment_filter"
        )
    
    with col2:
        date_range = st.selectbox(
            "Date Range",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
            key="mh_date_filter"
        )
    
    with col3:
        user_filter = st.selectbox(
            "User Filter",
            ["All Users", "Active Only", "Inactive Only"],
            key="mh_user_filter"
        )
    
    with col4:
        if st.button("🔄 Apply Filters", key="mh_apply_filters"):
            st.rerun()
    
    # Get mental health data
    mh_data = get_mental_health_data(sentiment_filter, date_range, user_filter)
    
    if mh_data.empty:
        st.info("No mental health records found matching the criteria.")
        return
    
    # Summary Statistics
    st.markdown("### 📊 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_entries = len(mh_data)
        st.metric("📝 Total Entries", total_entries)
    
    with col2:
        if not mh_data.empty:
            avg_confidence = mh_data['confidence'].mean()
            st.metric("📈 Avg Confidence", f"{avg_confidence:.1%}")
    
    with col3:
        unique_users = mh_data['user_id'].nunique()
        st.metric("👥 Unique Users", unique_users)
    
    with col4:
        if not mh_data.empty:
            today_entries = mh_data[mh_data['timestamp'].dt.date == datetime.now().date()]
            st.metric("📅 Today's Entries", len(today_entries))
    
    # Charts
    st.markdown("### 📈 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment distribution pie chart
        st.markdown("#### 🥧 Sentiment Distribution")
        sentiment_chart = get_sentiment_distribution_chart(mh_data)
        if sentiment_chart:
            st.plotly_chart(sentiment_chart, use_container_width=True)
    
    with col2:
        # Daily trend chart
        st.markdown("#### 📈 Daily Sentiment Trend")
        trend_chart = get_daily_sentiment_trend(mh_data)
        if trend_chart:
            st.plotly_chart(trend_chart, use_container_width=True)
    
    # User breakdown
    st.markdown("### 👥 User Breakdown")
    
    user_stats = get_user_mental_health_stats(mh_data)
    
    if not user_stats.empty:
        # Top 10 most active users
        st.markdown("#### 🏆 Most Active Users (by entries)")
        
        top_users = user_stats.head(10)
        
        for index, user_stat in top_users.iterrows():
            with st.expander(f"👤 {user_stat['user_name']} ({user_stat['user_email']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📝 Total Entries", user_stat['total_entries'])
                
                with col2:
                    st.metric("📊 Avg Confidence", f"{user_stat['avg_confidence']:.1%}")
                
                with col3:
                    # Display sentiment breakdown
                    sentiments = []
                    if user_stat['positive_entries'] > 0:
                        sentiments.append(f"😊 {user_stat['positive_entries']}")
                    if user_stat['neutral_entries'] > 0:
                        sentiments.append(f"😐 {user_stat['neutral_entries']}")
                    if user_stat['negative_entries'] > 0:
                        sentiments.append(f"😔 {user_stat['negative_entries']}")
                    
                    st.metric("🧠 Sentiments", " | ".join(sentiments))
                
                # Recent entries for this user
                user_entries = mh_data[mh_data['user_id'] == user_stat['user_id']].head(3)
                
                st.markdown("**Recent Entries:**")
                for _, entry in user_entries.iterrows():
                    sentiment_emoji = {'positive': '😊', 'neutral': '😐', 'negative': '😔'}[entry['sentiment']]
                    st.write(f"{sentiment_emoji} {entry['timestamp'].strftime('%Y-%m-%d %H:%M')}: {entry['feeling'][:100]}...")
    
    # Detailed Records Table
    st.markdown("### 📋 Detailed Records")
    
    # Pagination
    page_size = 20
    total_pages = (len(mh_data) + page_size - 1) // page_size
    
    if total_pages > 1:
        page = st.selectbox("Page", range(1, total_pages + 1), key="mh_page")
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_data = mh_data.iloc[start_idx:end_idx]
    else:
        paginated_data = mh_data
    
    # Display records
    for _, record in paginated_data.iterrows():
        sentiment_class = f"sentiment-{record['sentiment']}"
        sentiment_emoji = {'positive': '😊', 'neutral': '😐', 'negative': '😔'}[record['sentiment']]
        
        st.markdown(f'<div class="{sentiment_class}">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{sentiment_emoji} {record['user_name']}**")
            st.write(f"📝 {record['feeling']}")
            st.write(f"🕒 {record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        with col2:
            st.metric("📊 Confidence", f"{record['confidence']:.1%}")
        
        with col3:
            st.metric("👤 Age", f"{record['user_age']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export functionality
    st.markdown("### 📤 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export to CSV", help="Export filtered mental health data"):
            csv_data = export_mental_health_to_csv(mh_data)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"mental_health_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Generate Report", help="Generate comprehensive report"):
            # Log admin action
            log_admin_action(
                st.session_state.admin_id,
                "MENTAL_HEALTH_REPORT_GENERATED",
                f"Generated mental health report with {len(mh_data)} entries"
            )
            st.success("Report generation started! Check downloads for the CSV file.")

def get_mental_health_data(sentiment_filter="All", date_range="Last 30 Days", user_filter="All Users"):
    """Get filtered mental health data"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        # Calculate date filter
        date_filter_sql = ""
        if date_range == "Last 7 Days":
            date_filter_sql = "AND mh.timestamp >= date('now', '-7 days')"
        elif date_range == "Last 30 Days":
            date_filter_sql = "AND mh.timestamp >= date('now', '-30 days')"
        elif date_range == "Last 90 Days":
            date_filter_sql = "AND mh.timestamp >= date('now', '-90 days')"
        
        # User filter
        user_filter_sql = ""
        if user_filter == "Active Only":
            user_filter_sql = "AND u.is_active = 1"
        elif user_filter == "Inactive Only":
            user_filter_sql = "AND u.is_active = 0"
        
        # Sentiment filter
        sentiment_filter_sql = ""
        if sentiment_filter != "All":
            sentiment_filter_sql = f"AND mh.sentiment = '{sentiment_filter.lower()}'"
        
        query = f"""
        SELECT 
            mh.id,
            mh.user_id,
            mh.feeling,
            mh.sentiment,
            mh.confidence,
            mh.timestamp,
            u.name as user_name,
            u.email as user_email,
            u.age as user_age
        FROM mental_health mh
        JOIN users u ON mh.user_id = u.id
        WHERE 1=1
        {date_filter_sql}
        {user_filter_sql}
        {sentiment_filter_sql}
        ORDER BY mh.timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert timestamp to datetime
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching mental health data: {e}")
        return pd.DataFrame()

def get_sentiment_distribution_chart(data):
    """Create sentiment distribution pie chart"""
    
    if data.empty:
        return None
    
    sentiment_counts = data['sentiment'].value_counts()
    
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title="Sentiment Distribution",
        color_discrete_map={
            'positive': '#28a745',
            'neutral': '#ffc107',
            'negative': '#dc3545'
        }
    )
    
    fig.update_layout(height=400)
    return fig

def get_daily_sentiment_trend(data):
    """Create daily sentiment trend chart"""
    
    if data.empty:
        return None
    
    # Group by date and sentiment
    daily_data = data.groupby([data['timestamp'].dt.date, 'sentiment']).size().reset_index(name='count')
    daily_data.columns = ['date', 'sentiment', 'count']
    
    fig = px.line(
        daily_data,
        x='date',
        y='count',
        color='sentiment',
        title="Daily Sentiment Trend",
        labels={'date': 'Date', 'count': 'Number of Entries', 'sentiment': 'Sentiment'},
        color_discrete_map={
            'positive': '#28a745',
            'neutral': '#ffc107',
            'negative': '#dc3545'
        }
    )
    
    fig.update_layout(height=400)
    return fig

def get_user_mental_health_stats(data):
    """Get mental health statistics per user"""
    
    if data.empty:
        return pd.DataFrame()
    
    # Group by user
    user_stats = data.groupby('user_id').agg({
        'sentiment': ['count', lambda x: (x == 'positive').sum(), 
                      lambda x: (x == 'neutral').sum(), lambda x: (x == 'negative').sum()],
        'confidence': 'mean',
        'user_name': 'first',
        'user_email': 'first'
    }).reset_index()
    
    # Flatten column names
    user_stats.columns = ['user_id', 'total_entries', 'positive_entries', 
                         'neutral_entries', 'negative_entries', 'avg_confidence', 'user_name', 'user_email']
    
    # Sort by total entries
    user_stats = user_stats.sort_values('total_entries', ascending=False)
    
    return user_stats

def export_mental_health_to_csv(data):
    """Export mental health data to CSV"""
    
    if data.empty:
        return "No data to export"
    
    # Select relevant columns
    export_data = data[[
        'timestamp', 'user_name', 'user_email', 'user_age',
        'feeling', 'sentiment', 'confidence'
    ]].copy()
    
    # Rename columns for better readability
    export_data.columns = [
        'Timestamp', 'User Name', 'User Email', 'User Age',
        'Feeling', 'Sentiment', 'Confidence'
    ]
    
    return export_data.to_csv(index=False)
