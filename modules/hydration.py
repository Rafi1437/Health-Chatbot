"""
Hydration Monitoring Module
Tracks daily water intake and provides hydration reminders for senior citizens
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import os

def calculate_recommended_water(age, weight_kg=70):
    """Calculate recommended daily water intake in ml"""
    
    # Convert age to integer if it's a string
    try:
        age = int(age)
    except (ValueError, TypeError):
        age = 65  # Default age for seniors
    
    # Base calculation: 30-35 ml per kg of body weight
    base_intake = weight_kg * 32
    
    # Age adjustment for seniors (65+ may need slightly more)
    if age >= 65:
        base_intake *= 1.1
    
    # Ensure minimum of 2000ml for seniors
    recommended = max(2000, int(base_intake))
    
    return recommended

def show_hydration():
    """Display hydration monitoring page"""
    
    st.markdown("""
    <style>
    .main {
        background-color: #e6f3ff;
    }
    .hydration-progress {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .water-reminder {
        background-color: #e1f5fe;
        border-left: 5px solid #03a9f4;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    .stButton > button {
        background-color: #03a9f4;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 10px;
    }
    .progress-bar {
        height: 30px;
        background-color: #f0f0f0;
        border-radius: 15px;
        overflow: hidden;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 💧 Hydration Tracker")
    st.markdown("## Stay hydrated for better health!")
    
    # Get user info
    user_age = st.session_state.get('user_age', 65)
    recommended_intake = calculate_recommended_water(user_age)
    
    # Display recommended intake
    st.info(f"💡 **Recommended Daily Water Intake:** {recommended_intake} ml ({recommended_intake/1000:.1f} liters)")
    
    # Water intake form
    with st.form("hydration_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            water_amount = st.number_input(
                "💧 Water Intake (ml)",
                min_value=0,
                max_value=5000,
                value=250,
                step=50,
                help="Enter the amount of water you drank"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("📝 Add Intake", use_container_width=True)
        
        if submitted:
            if water_amount > 0:
                save_hydration_record(
                    st.session_state.user_id,
                    water_amount,
                    recommended_intake
                )
                st.success(f"✅ Added {water_amount} ml to your hydration log!")
                st.balloons()
            else:
                st.error("❌ Please enter a valid water amount")
    
    # Show today's progress
    show_today_progress(recommended_intake)
    
    # Show hydration history
    show_hydration_history()
    
    # Show hydration tips
    show_hydration_tips()

def save_hydration_record(user_id, water_ml, recommended_ml):
    """Save hydration record to database"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO hydration (user_id, water_ml, recommended_ml) VALUES (?, ?, ?)",
            (user_id, water_ml, recommended_ml)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving hydration record: {e}")
        return False

def show_today_progress(recommended_intake):
    """Display today's hydration progress"""
    
    st.markdown("### 📊 Today's Progress")
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        # Get today's intake
        query = """
        SELECT SUM(water_ml) as total_intake, COUNT(*) as intake_count
        FROM hydration 
        WHERE user_id = ? 
        AND date(timestamp) = date('now')
        """
        
        cursor = conn.cursor()
        cursor.execute(query, (st.session_state.user_id,))
        result = cursor.fetchone()
        conn.close()
        
        total_intake = result[0] if result[0] else 0
        intake_count = result[1] if result[1] else 0
        
        # Calculate progress
        progress_percentage = min(100, (total_intake / recommended_intake) * 100)
        remaining = max(0, recommended_intake - total_intake)
        
        # Display progress card
        st.markdown('<div class="hydration-progress">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💧 Total Intake", f"{total_intake} ml")
        
        with col2:
            st.metric("🎯 Goal", f"{recommended_intake} ml")
        
        with col3:
            st.metric("📈 Progress", f"{progress_percentage:.1f}%")
        
        # Progress bar
        st.markdown("#### Hydration Progress")
        
        # Create custom progress bar
        fig = go.Figure(go.Bar(
            x=[progress_percentage],
            y=['Progress'],
            orientation='h',
            marker=dict(
                color=['#03a9f4'] if progress_percentage < 100 else ['#4caf50'],
                line=dict(color='white', width=2)
            )
        ))
        
        fig.update_layout(
            xaxis=dict(range=[0, 100], showgrid=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            height=80,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Status message
        if progress_percentage >= 100:
            st.success("🎉 Excellent! You've reached your daily hydration goal!")
        elif progress_percentage >= 75:
            st.info(f"💪 Great job! You're {progress_percentage:.1f}% there. Only {remaining} ml more to go!")
        elif progress_percentage >= 50:
            st.warning(f"💧 Good progress! You're {progress_percentage:.1f}% there. Need {remaining} ml more.")
        else:
            st.error(f"💦 Keep going! You're at {progress_percentage:.1f}%. Need {remaining} ml more.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick add buttons
        st.markdown("#### 🚀 Quick Add")
        col1, col2, col3, col4 = st.columns(4)
        
        quick_amounts = [250, 500, 750, 1000]
        
        for i, amount in enumerate(quick_amounts):
            with [col1, col2, col3, col4][i]:
                if st.button(f"+{amount} ml", use_container_width=True, key=f"quick_{amount}"):
                    save_hydration_record(
                        st.session_state.user_id,
                        amount,
                        recommended_intake
                    )
                    st.success(f"✅ Added {amount} ml!")
                    st.rerun()
        
    except Exception as e:
        st.error(f"Error loading today's progress: {e}")

def show_hydration_history():
    """Display hydration history with charts"""
    
    st.markdown("### 📈 Hydration History")
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        
        # Get last 7 days of data
        query = """
        SELECT date(timestamp) as date, SUM(water_ml) as total_intake, recommended_ml
        FROM hydration 
        WHERE user_id = ? 
        AND timestamp >= date('now', '-7 days')
        GROUP BY date(timestamp)
        ORDER BY date DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(st.session_state.user_id,))
        conn.close()
        
        if df.empty:
            st.info("📝 No hydration records yet. Start tracking your water intake above!")
            return
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Calculate achievement percentage
        df['achievement_percentage'] = (df['total_intake'] / df['recommended_ml']) * 100
        
        # 7-day trend chart
        st.markdown("#### 📊 7-Day Hydration Trend")
        
        fig = go.Figure()
        
        # Add actual intake bars
        fig.add_trace(go.Bar(
            x=df['date'].dt.strftime('%b %d'),
            y=df['total_intake'],
            name='Actual Intake',
            marker_color='#03a9f4',
            text=df['total_intake'],
            textposition='auto'
        ))
        
        # Add recommended intake line
        fig.add_trace(go.Scatter(
            x=df['date'].dt.strftime('%b %d'),
            y=df['recommended_ml'],
            mode='lines',
            name='Recommended',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Daily Water Intake vs Recommended",
            xaxis_title="Date",
            yaxis_title="Water Intake (ml)",
            height=400,
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Achievement percentage chart
        st.markdown("#### 🎯 Goal Achievement")
        
        fig_achievement = go.Figure(go.Bar(
            x=df['date'].dt.strftime('%b %d'),
            y=df['achievement_percentage'],
            marker_color=['#4caf50' if x >= 100 else '#ffc107' if x >= 75 else '#f44336' for x in df['achievement_percentage']],
            text=[f"{x:.0f}%" for x in df['achievement_percentage']],
            textposition='auto'
        ))
        
        fig_achievement.update_layout(
            title="Daily Goal Achievement (%)",
            xaxis_title="Date",
            yaxis_title="Achievement %",
            height=400,
            yaxis=dict(range=[0, 120])
        )
        
        st.plotly_chart(fig_achievement, use_container_width=True)
        
        # Summary statistics
        st.markdown("#### 📋 Summary Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_intake = df['total_intake'].mean()
            st.metric("📊 Average Daily Intake", f"{avg_intake:.0f} ml")
        
        with col2:
            days_achieved = len(df[df['achievement_percentage'] >= 100])
            st.metric("🎯 Days Goal Met", f"{days_achieved}/7")
        
        with col3:
            best_day = df.loc[df['total_intake'].idxmax()]
            st.metric("🏆 Best Day", f"{best_day['total_intake']:.0f} ml")
        
    except Exception as e:
        st.error(f"Error loading hydration history: {e}")

def show_hydration_tips():
    """Display hydration tips and reminders"""
    
    st.markdown("### 💡 Hydration Tips")
    
    tips = [
        {
            "title": "🌅 Start Your Day Right",
            "content": "Drink a glass of water first thing in the morning to kickstart your metabolism."
        },
        {
            "title": "⏰ Set Regular Reminders",
            "content": "Drink water every 1-2 hours, even if you don't feel thirsty."
        },
        {
            "title": "🥤 Keep Water Accessible",
            "content": "Keep a water bottle nearby throughout the day as a visual reminder."
        },
        {
            "title": "🍎 Eat Water-Rich Foods",
            "content": "Include fruits and vegetables like watermelon, cucumber, and oranges in your diet."
        },
        {
            "title": "🏃‍♂️ Before and After Exercise",
            "content": "Drink water before, during, and after physical activity."
        },
        {
            "title": "🌡️ Monitor Urine Color",
            "content": "Pale yellow urine indicates good hydration. Dark yellow means you need more water."
        }
    ]
    
    for i, tip in enumerate(tips):
        with st.expander(tip["title"]):
            st.write(tip["content"])
    
    # Reminder messages
    st.markdown('<div class="water-reminder">', unsafe_allow_html=True)
    st.markdown("#### ⏰ Hydration Reminders")
    st.write("• Drink a glass of water with each meal")
    st.write("• Keep a water bottle by your bedside")
    st.write("• Set phone alarms for water breaks")
    st.write("• Drink water before feeling thirsty")
    st.markdown('</div>', unsafe_allow_html=True)
