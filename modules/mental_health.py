"""
Mental Health Monitoring Module
Provides sentiment analysis and mental health tracking for senior citizens
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path to import ML model
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import with error handling for cloud deployment
try:
    from ml.sentiment_model import SentimentAnalyzer
    NLTK_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ NLTK features may be limited: {e}")
    NLTK_AVAILABLE = False
    SentimentAnalyzer = None

def show_mental_health():
    """Display mental health monitoring page"""
    
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .sentiment-positive {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .sentiment-neutral {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
    }
    .sentiment-negative {
        background-color: #f8d7da;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
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
    
    st.markdown("# 🧠 Mental Health Check")
    st.markdown("## How are you feeling today?")
    
    # Check if NLTK is available
    if not NLTK_AVAILABLE:
        st.warning("⚠️ Sentiment analysis is currently unavailable. NLTK data could not be loaded.")
        st.info("You can still track your feelings, but sentiment analysis will be disabled.")
    
    # Initialize sentiment analyzer only if available
    analyzer = SentimentAnalyzer() if NLTK_AVAILABLE else None
    
    # Check-in form
    with st.form("mental_health_form"):
        feeling = st.text_area(
            "Share your feelings...",
            placeholder="Tell us how you're feeling today... You can talk about your mood, energy level, or anything on your mind.",
            height=100
        )
        
        submitted = st.form_submit_button("🔍 Analyze My Mood", use_container_width=True)
        
        if submitted:
            if not feeling.strip():
                st.error("❌ Please share how you're feeling")
                return
            
            # Analyze sentiment only if NLTK is available
            if analyzer:
                try:
                    result = analyzer.predict_sentiment(feeling)
                    sentiment = result['sentiment']
                    confidence = result['confidence']
                    emoji = analyzer.get_sentiment_emoji(sentiment)
                    
                    # Display result
                    sentiment_class = f"sentiment-{sentiment}"
                    
                    st.markdown(f"""
                    <div class="{sentiment_class}">
                        <h2>{emoji} Your Mood: {sentiment.title()}</h2>
                        <p><strong>Confidence:</strong> {confidence:.1%}</p>
                        <p><strong>Your message:</strong> "{feeling}"</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Save to database
                    save_mental_health_record(
                        st.session_state.user_id,
                        feeling,
                        sentiment,
                        confidence
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error analyzing sentiment: {e}")
                    st.info("Your feeling has been saved, but sentiment analysis was not available.")
                    # Still save the feeling without sentiment analysis
                    save_mental_health_record(
                        st.session_state.user_id,
                        feeling,
                        "neutral",  # Default sentiment
                        0.5  # Default confidence
                    )
            else:
                # NLTK not available, just save the feeling
                st.info("Your feeling has been saved. Sentiment analysis is currently unavailable.")
                save_mental_health_record(
                    st.session_state.user_id,
                    feeling,
                    "neutral",  # Default sentiment
                    0.5  # Default confidence
                )
            
            # Provide personalized feedback
            if sentiment == "positive":
                st.success("🎉 That's wonderful to hear! Keep up the positive spirit!")
                st.info("💡 Consider sharing your joy with family or friends, or engaging in activities that make you happy.")
            elif sentiment == "neutral":
                st.info("🤔 It's okay to have neutral days. Consider trying something new or engaging in light activities.")
                st.info("💡 A short walk, calling a friend, or listening to music might help brighten your day.")
            else:
                st.warning("🫂 I'm sorry you're feeling this way. Remember, it's okay to not be okay.")
                st.info("💡 Consider reaching out to a family member, friend, or healthcare provider. You're not alone.")
            
            st.balloons()
    
    st.markdown("---")
    
    # Show mental health history
    show_mental_health_history()

def save_mental_health_record(user_id, feeling, sentiment, confidence):
    """Save mental health record to database"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO mental_health (user_id, feeling, sentiment, confidence) VALUES (?, ?, ?, ?)",
            (user_id, feeling, sentiment, confidence)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving record: {e}")
        return False

def show_mental_health_history():
    """Display mental health history with charts"""
    
    st.markdown("### 📊 Your Mental Health Journey")
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        # Get last 30 days of data
        query = """
        SELECT sentiment, confidence, timestamp, feeling
        FROM mental_health 
        WHERE user_id = ? 
        AND timestamp >= date('now', '-30 days')
        ORDER BY timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(st.session_state.user_id,))
        conn.close()
        
        if df.empty:
            st.info("📝 No mental health records yet. Start by sharing how you feel above!")
            return
        
        # Validate and clean data
        if 'confidence' in df.columns:
            df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce')
            df['confidence'] = df['confidence'].fillna(0.5)  # Default confidence if NaN
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Summary statistics
        st.markdown("#### 📈 Summary Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            positive_count = len(df[df['sentiment'] == 'positive'])
            st.metric("😊 Positive Days", positive_count)
        
        with col2:
            neutral_count = len(df[df['sentiment'] == 'neutral'])
            st.metric("😐 Neutral Days", neutral_count)
        
        with col3:
            negative_count = len(df[df['sentiment'] == 'negative'])
            st.metric("😔 Challenging Days", negative_count)
        
        # Sentiment trend chart
        st.markdown("#### 📈 Mood Trend (Last 30 Days)")
        
        # Create sentiment score for visualization
        sentiment_scores = {'positive': 1, 'neutral': 0, 'negative': -1}
        df['sentiment_score'] = df['sentiment'].map(sentiment_scores)
        
        # Group by date and get average sentiment
        daily_sentiment = df.groupby('date').agg({
            'sentiment_score': 'mean'
        }).reset_index()
        
        # Handle confidence separately to avoid errors
        if 'confidence' in df.columns:
            daily_confidence = df.groupby('date')['confidence'].mean().reset_index()
            daily_sentiment = daily_sentiment.merge(daily_confidence, on='date', how='left')
        
        if not daily_sentiment.empty:
            fig = go.Figure()
            
            # Add sentiment trend line
            fig.add_trace(go.Scatter(
                x=daily_sentiment['date'],
                y=daily_sentiment['sentiment_score'],
                mode='lines+markers',
                name='Mood Trend',
                line=dict(color='purple', width=3),
                marker=dict(size=8)
            ))
            
            # Add horizontal reference lines
            fig.add_hline(y=1, line_dash="dash", line_color="green", annotation_text="Positive")
            fig.add_hline(y=0, line_dash="dash", line_color="orange", annotation_text="Neutral")
            fig.add_hline(y=-1, line_dash="dash", line_color="red", annotation_text="Negative")
            
            fig.update_layout(
                title="Your Mood Over Time",
                xaxis_title="Date",
                yaxis_title="Mood Score",
                yaxis=dict(range=[-1.2, 1.2]),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment distribution pie chart
        st.markdown("#### 🥧 Mood Distribution")
        
        sentiment_counts = df['sentiment'].value_counts()
        
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Your Mood Breakdown",
            color_discrete_map={
                'positive': '#28a745',
                'neutral': '#ffc107',
                'negative': '#dc3545'
            }
        )
        
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Recent entries
        st.markdown("#### 📝 Recent Check-ins")
        
        # Select only columns that exist
        available_columns = ['timestamp', 'sentiment', 'feeling']
        if 'confidence' in df.columns:
            available_columns.append('confidence')
        
        recent_entries = df.head(5)[available_columns]
        
        for _, row in recent_entries.iterrows():
            emoji = {'positive': '😊', 'neutral': '😐', 'negative': '😔'}[row['sentiment']]
            
            with st.expander(f"{emoji} {row['timestamp'].strftime('%B %d, %Y %I:%M %p')} - {row['sentiment'].title()}"):
                st.write(row['feeling'])
                if 'confidence' in row and pd.notna(row['confidence']):
                    st.write(f"Confidence: {row['confidence']:.1%}")
        
    except Exception as e:
        st.error(f"Error loading mental health history: {e}")
