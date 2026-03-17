"""
Reports Module
Provides comprehensive health reports and analytics for senior citizens
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

def show_reports():
    """Display comprehensive health reports page"""
    
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .report-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
    }
    .stButton > button {
        background-color: #6f42c1;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 📊 Health Reports")
    st.markdown("## Your comprehensive health overview")
    
    # Time period selector
    st.markdown("### 📅 Select Time Period")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Last 7 Days", use_container_width=True):
            st.session_state.report_period = 7
            st.rerun()
    
    with col2:
        if st.button("📊 Last 30 Days", use_container_width=True):
            st.session_state.report_period = 30
            st.rerun()
    
    with col3:
        if st.button("📋 Last 90 Days", use_container_width=True):
            st.session_state.report_period = 90
            st.rerun()
    
    # Default to 30 days
    period = st.session_state.get('report_period', 30)
    
    st.info(f"📅 Showing reports for the last **{period} days**")
    
    # Overall health summary
    show_overall_summary(period)
    
    # Mental health report
    show_mental_health_report(period)
    
    # Hydration report
    show_hydration_report(period)
    
    # Chatbot usage report
    show_chatbot_report(period)
    
    # Export options
    show_export_options()

def show_overall_summary(period):
    """Display overall health summary"""
    
    st.markdown("### 🏥 Overall Health Summary")
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        # Get mental health stats
        mh_query = """
        SELECT COUNT(*) as total_entries,
               SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) as positive_days,
               SUM(CASE WHEN sentiment = 'neutral' THEN 1 ELSE 0 END) as neutral_days,
               SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) as negative_days,
               AVG(confidence) as avg_confidence
        FROM mental_health 
        WHERE user_id = ? 
        AND timestamp >= date('now', '-{} days')
        """.format(period)
        
        mh_df = pd.read_sql_query(mh_query, conn, params=(st.session_state.user_id,))
        
        # Get hydration stats
        hyd_query = """
        SELECT COUNT(*) as total_entries,
               SUM(water_ml) as total_water,
               AVG(water_ml) as avg_daily_intake,
               SUM(CASE WHEN water_ml >= recommended_ml THEN 1 ELSE 0 END) as goals_met
        FROM hydration 
        WHERE user_id = ? 
        AND timestamp >= date('now', '-{} days')
        """.format(period)
        
        hyd_df = pd.read_sql_query(hyd_query, conn, params=(st.session_state.user_id,))
        
        # Get chatbot usage
        chat_query = """
        SELECT COUNT(*) as total_conversations
        FROM chatbot_logs 
        WHERE user_id = ? 
        AND timestamp >= date('now', '-{} days')
        """.format(period)
        
        chat_df = pd.read_sql_query(chat_query, conn, params=(st.session_state.user_id,))
        
        conn.close()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            mh_entries = mh_df['total_entries'].iloc[0] if not mh_df.empty else 0
            st.metric("🧠 Mood Check-ins", mh_entries)
        
        with col2:
            hyd_entries = hyd_df['total_entries'].iloc[0] if not hyd_df.empty else 0
            st.metric("💧 Hydration Logs", hyd_entries)
        
        with col3:
            chat_entries = chat_df['total_conversations'].iloc[0] if not chat_df.empty else 0
            st.metric("🤖 Chat Sessions", chat_entries)
        
        with col4:
            # Calculate overall wellness score
            wellness_score = calculate_wellness_score(mh_df, hyd_df, period)
            st.metric("⭐ Wellness Score", f"{wellness_score}/100")
        
        # Health insights
        st.markdown("#### 💡 Health Insights")
        
        insights = generate_health_insights(mh_df, hyd_df, chat_df, period)
        
        for insight in insights:
            st.info(insight)
        
    except Exception as e:
        st.error(f"Error loading overall summary: {e}")

def show_mental_health_report(period):
    """Display detailed mental health report"""
    
    st.markdown("### 🧠 Mental Health Report")
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT sentiment, confidence, timestamp, feeling
        FROM mental_health 
        WHERE user_id = ? 
        AND timestamp >= date('now', '-{} days')
        ORDER BY timestamp DESC
        """.format(period)
        
        df = pd.read_sql_query(query, conn, params=(st.session_state.user_id,))
        conn.close()
        
        if df.empty:
            st.info("📝 No mental health records for this period.")
            return
        
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Sentiment distribution
        st.markdown("#### 😊 Mood Distribution")
        
        sentiment_counts = df['sentiment'].value_counts()
        
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Mood Breakdown",
            color_discrete_map={
                'positive': '#28a745',
                'neutral': '#ffc107',
                'negative': '#dc3545'
            }
        )
        
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Mood trend
        st.markdown("#### 📈 Mood Trend")
        
        # Create sentiment scores
        sentiment_scores = {'positive': 1, 'neutral': 0, 'negative': -1}
        df['sentiment_score'] = df['sentiment'].map(sentiment_scores)
        
        # Daily average sentiment
        daily_sentiment = df.groupby('date')['sentiment_score'].mean().reset_index()
        
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=daily_sentiment['date'],
            y=daily_sentiment['sentiment_score'],
            mode='lines+markers',
            name='Average Mood',
            line=dict(color='purple', width=3),
            marker=dict(size=8)
        ))
        
        fig_trend.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral")
        
        fig_trend.update_layout(
            title="Daily Mood Trend",
            xaxis_title="Date",
            yaxis_title="Mood Score",
            height=400
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Statistics
        st.markdown("#### 📊 Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            positive_days = len(df[df['sentiment'] == 'positive'])
            st.metric("😊 Positive Days", positive_days)
        
        with col2:
            if 'confidence' in df.columns:
                avg_confidence = df['confidence'].mean()
                st.metric("📊 Avg Confidence", f"{avg_confidence:.1%}")
            else:
                st.metric("📊 Avg Confidence", "N/A")
        
        with col3:
            most_common = df['sentiment'].mode().iloc[0] if not df.empty else 'N/A'
            emoji = {'positive': '😊', 'neutral': '😐', 'negative': '😔'}[most_common]
            st.metric("🎯 Most Common", f"{emoji} {most_common.title()}")
        
    except Exception as e:
        st.error(f"Error loading mental health report: {e}")

def show_hydration_report(period):
    """Display detailed hydration report"""
    
    st.markdown("### 💧 Hydration Report")
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT water_ml, recommended_ml, timestamp
        FROM hydration 
        WHERE user_id = ? 
        AND timestamp >= date('now', '-{} days')
        ORDER BY timestamp DESC
        """.format(period)
        
        df = pd.read_sql_query(query, conn, params=(st.session_state.user_id,))
        conn.close()
        
        if df.empty:
            st.info("📝 No hydration records for this period.")
            return
        
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['achievement_percentage'] = (df['water_ml'] / df['recommended_ml']) * 100
        
        # Daily summary
        daily_summary = df.groupby('date').agg({
            'water_ml': 'sum',
            'recommended_ml': 'first',
            'achievement_percentage': 'mean'
        }).reset_index()
        
        # Hydration trend
        st.markdown("#### 📊 Daily Hydration Trend")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=daily_summary['date'],
            y=daily_summary['water_ml'],
            name='Actual Intake',
            marker_color='#03a9f4'
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_summary['date'],
            y=daily_summary['recommended_ml'],
            mode='lines',
            name='Recommended',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Daily Water Intake",
            xaxis_title="Date",
            yaxis_title="Water Intake (ml)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Goal achievement
        st.markdown("#### 🎯 Goal Achievement")
        
        goals_met = len(daily_summary[daily_summary['achievement_percentage'] >= 100])
        total_days = len(daily_summary)
        achievement_rate = (goals_met / total_days) * 100 if total_days > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🎯 Goals Met", f"{goals_met}/{total_days}")
        
        with col2:
            st.metric("📈 Achievement Rate", f"{achievement_rate:.1f}%")
        
        with col3:
            avg_intake = daily_summary['water_ml'].mean()
            st.metric("💧 Avg Daily Intake", f"{avg_intake:.0f} ml")
        
        # Achievement distribution
        st.markdown("#### 📈 Achievement Distribution")
        
        achievement_categories = pd.cut(
            daily_summary['achievement_percentage'],
            bins=[0, 50, 75, 100, 150],
            labels=['< 50%', '50-75%', '75-100%', '> 100%']
        )
        
        achievement_counts = achievement_categories.value_counts()
        
        fig_achievement = px.bar(
            x=achievement_counts.index,
            y=achievement_counts.values,
            title="Goal Achievement Distribution",
            labels={'x': 'Achievement Range', 'y': 'Number of Days'},
            color=achievement_counts.index,
            color_discrete_map={
                '< 50%': '#f44336',
                '50-75%': '#ff9800',
                '75-100%': '#ffc107',
                '> 100%': '#4caf50'
            }
        )
        
        fig_achievement.update_layout(height=400)
        st.plotly_chart(fig_achievement, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading hydration report: {e}")

def show_chatbot_report(period):
    """Display chatbot usage report"""
    
    st.markdown("### 🤖 Chatbot Usage Report")
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT user_message, bot_response, timestamp
        FROM chatbot_logs 
        WHERE user_id = ? 
        AND timestamp >= date('now', '-{} days')
        ORDER BY timestamp DESC
        """.format(period)
        
        df = pd.read_sql_query(query, conn, params=(st.session_state.user_id,))
        conn.close()
        
        if df.empty:
            st.info("📝 No chatbot conversations for this period.")
            return
        
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Daily conversation count
        daily_conversations = df.groupby('date').size().reset_index(name='conversation_count')
        
        # Conversation trend
        st.markdown("#### 📈 Conversation Trend")
        
        fig = px.line(
            daily_conversations,
            x='date',
            y='conversation_count',
            title="Daily Chatbot Interactions",
            markers=True
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        st.markdown("#### 📊 Usage Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_conversations = len(df)
            st.metric("💬 Total Conversations", total_conversations)
        
        with col2:
            avg_daily = daily_conversations['conversation_count'].mean()
            st.metric("📊 Daily Average", f"{avg_daily:.1f}")
        
        with col3:
            most_active_day = daily_conversations.loc[daily_conversations['conversation_count'].idxmax()]
            st.metric("🏆 Most Active Day", f"{most_active_day['conversation_count']} chats")
        
        # Recent conversations
        st.markdown("#### 💬 Recent Conversations")
        
        recent_conversations = df.head(5)
        
        for _, row in recent_conversations.iterrows():
            with st.expander(f"💬 {row['timestamp'].strftime('%B %d, %Y %I:%M %p')}"):
                st.write("**You:**", row['user_message'])
                st.write("**Assistant:**", row['bot_response'])
        
    except Exception as e:
        st.error(f"Error loading chatbot report: {e}")

def calculate_wellness_score(mh_df, hyd_df, period):
    """Calculate overall wellness score"""
    
    score = 50  # Base score
    
    # Mental health component (30 points)
    if not mh_df.empty and mh_df['total_entries'].iloc[0] > 0:
        total_entries = mh_df['total_entries'].iloc[0]
        positive_ratio = mh_df['positive_days'].iloc[0] / total_entries
        
        # Points for positive sentiment ratio
        mh_score = positive_ratio * 30
        score += mh_score
    
    # Hydration component (20 points)
    if not hyd_df.empty and hyd_df['total_entries'].iloc[0] > 0:
        goals_met_ratio = hyd_df['goals_met'].iloc[0] / hyd_df['total_entries'].iloc[0]
        
        # Points for meeting hydration goals
        hyd_score = goals_met_ratio * 20
        score += hyd_score
    
    return min(100, int(score))

def generate_health_insights(mh_df, hyd_df, chat_df, period):
    """Generate personalized health insights"""
    
    insights = []
    
    # Mental health insights
    if not mh_df.empty and mh_df['total_entries'].iloc[0] > 0:
        positive_ratio = mh_df['positive_days'].iloc[0] / mh_df['total_entries'].iloc[0]
        
        if positive_ratio >= 0.7:
            insights.append("🎉 Great job maintaining a positive mood! Keep up the good work!")
        elif positive_ratio >= 0.5:
            insights.append("😊 You're doing well with your mood. Consider activities that boost positivity.")
        else:
            insights.append("💙 Consider reaching out to friends, family, or healthcare providers for support.")
    
    # Hydration insights
    if not hyd_df.empty and hyd_df['total_entries'].iloc[0] > 0:
        goals_met_ratio = hyd_df['goals_met'].iloc[0] / hyd_df['total_entries'].iloc[0]
        
        if goals_met_ratio >= 0.8:
            insights.append("💧 Excellent hydration habits! You're meeting your water intake goals consistently.")
        elif goals_met_ratio >= 0.5:
            insights.append("💦 Good progress on hydration! Try to increase water intake slightly.")
        else:
            insights.append("💧 Focus on increasing your water intake. Set reminders throughout the day.")
    
    # Engagement insights
    if not chat_df.empty and chat_df['total_conversations'].iloc[0] > 0:
        insights.append("🤖 Great engagement with the health assistant! Keep asking questions about your health.")
    
    if not insights:
        insights.append("📊 Start tracking your health regularly to see personalized insights here.")
    
    return insights

def show_export_options():
    """Display data export options"""
    
    st.markdown("### 📤 Export Your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Download Health Summary", use_container_width=True):
            # Generate summary data
            summary_data = generate_health_summary()
            st.download_button(
                label="📥 Download CSV",
                data=summary_data.to_csv(index=False),
                file_name=f"health_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Print Report", use_container_width=True):
            st.info("🖨️ Use your browser's print function (Ctrl+P) to print this report.")

def generate_health_summary():
    """Generate health summary data for export"""
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        # Get summary data
        summary_data = []
        
        # Mental health summary
        mh_query = """
        SELECT date(timestamp) as date, sentiment, confidence
        FROM mental_health 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
        LIMIT 30
        """
        
        mh_df = pd.read_sql_query(mh_query, conn, params=(st.session_state.user_id,))
        
        if not mh_df.empty:
            # Clean confidence data
            if 'confidence' in mh_df.columns:
                mh_df['confidence'] = pd.to_numeric(mh_df['confidence'], errors='coerce')
                mh_df['confidence'] = mh_df['confidence'].fillna(0.5)
            
            for _, row in mh_df.iterrows():
                confidence_value = f"{row['confidence']:.1%}" if 'confidence' in row and pd.notna(row['confidence']) else "N/A"
                summary_data.append({
                    'Date': row['date'],
                    'Category': 'Mental Health',
                    'Metric': f"Sentiment: {row['sentiment']}",
                    'Value': confidence_value
                })
        
        # Hydration summary
        hyd_query = """
        SELECT date(timestamp) as date, water_ml, recommended_ml
        FROM hydration 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
        LIMIT 30
        """
        
        hyd_df = pd.read_sql_query(hyd_query, conn, params=(st.session_state.user_id,))
        
        if not hyd_df.empty:
            for _, row in hyd_df.iterrows():
                achievement = (row['water_ml'] / row['recommended_ml']) * 100
                summary_data.append({
                    'Date': row['date'],
                    'Category': 'Hydration',
                    'Metric': 'Water Intake',
                    'Value': f"{row['water_ml']} ml ({achievement:.0f}% of goal)"
                })
        
        conn.close()
        
        return pd.DataFrame(summary_data)
        
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return pd.DataFrame()
