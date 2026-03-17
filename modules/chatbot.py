"""
Medical Chatbot Module
Provides basic medical assistance and health advice for senior citizens
"""

import streamlit as st
import sqlite3
import re
import os
from datetime import datetime

class MedicalChatbot:
    """Rule-based medical chatbot for senior citizens"""
    
    def __init__(self):
        self.responses = {
            'headache': [
                "I'm sorry to hear about your headache. Here are some suggestions:",
                "• Rest in a quiet, dark room",
                "• Drink plenty of water",
                "• Apply a cold compress to your forehead",
                "• Consider over-the-counter pain relievers if appropriate",
                "⚠️ If your headache is severe or persistent, please consult a doctor."
            ],
            'fever': [
                "Fever can be concerning. Here's what you can do:",
                "• Drink lots of fluids to stay hydrated",
                "• Get plenty of rest",
                "• Take a lukewarm bath to cool down",
                "• Monitor your temperature regularly",
                "⚠️ If fever exceeds 103°F (39.4°C) or lasts more than 3 days, seek medical attention."
            ],
            'cold': [
                "For cold symptoms, try these remedies:",
                "• Get adequate rest",
                "• Stay hydrated with warm fluids",
                "• Use a humidifier",
                "• Gargle with warm salt water",
                "• Consider over-the-counter cold medications",
                "⚠️ If symptoms worsen or last more than 10 days, consult your healthcare provider."
            ],
            'diabetes': [
                "Managing diabetes is important. Here are some tips:",
                "• Monitor your blood sugar regularly",
                "• Follow your prescribed diet plan",
                "• Take medications as prescribed",
                "• Exercise regularly (as approved by your doctor)",
                "• Maintain a healthy weight",
                "• Always consult your healthcare provider for diabetes management."
            ],
            'bp': [
                "Blood pressure management is crucial:",
                "• Take prescribed medications regularly",
                "• Reduce sodium intake",
                "• Exercise regularly (with doctor's approval)",
                "• Maintain a healthy weight",
                "• Limit alcohol consumption",
                "• Manage stress through relaxation techniques",
                "⚠️ Regular BP monitoring is essential. Consult your doctor for personalized advice."
            ],
            'diet': [
                "Healthy eating tips for seniors:",
                "• Eat a variety of colorful fruits and vegetables",
                "• Choose whole grains over refined grains",
                "• Include lean proteins in your diet",
                "• Limit processed foods and added sugars",
                "• Stay hydrated with water throughout the day",
                "• Consider smaller, more frequent meals"
            ],
            'exercise': [
                "Exercise is important at any age:",
                "• Start with gentle activities like walking",
                "• Consider low-impact exercises (swimming, cycling)",
                "• Include strength training with light weights",
                "• Practice balance exercises to prevent falls",
                "• Always warm up before exercising",
                "⚠️ Consult your doctor before starting any new exercise program."
            ],
            'sleep': [
                "Good sleep is essential for health:",
                "• Maintain a regular sleep schedule",
                "• Create a comfortable sleep environment",
                "• Avoid caffeine late in the day",
                "• Limit screen time before bed",
                "• Consider relaxation techniques before sleep",
                "⚠️ If sleep problems persist, consult your healthcare provider."
            ],
            'medication': [
                "Medication management is crucial:",
                "• Take medications exactly as prescribed",
                "• Keep a list of all medications you take",
                "• Store medications properly",
                "• Never share medications with others",
                "• Report side effects to your doctor",
                "• Consider using pill organizers"
            ],
            'emergency': [
                "⚠️ EMERGENCY SITUATION:",
                "• Call emergency services immediately (911 or local emergency number)",
                "• Don't wait if you experience chest pain, difficulty breathing, or stroke symptoms",
                "• Keep emergency numbers readily available",
                "• Have a list of medications and medical conditions ready",
                "• If possible, have someone stay with you until help arrives"
            ]
        }
        
        self.greetings = [
            "Hello! I'm here to help with your health questions.",
            "Hi there! How can I assist you today?",
            "Welcome! Feel free to ask about health concerns.",
            "Greetings! I'm here to provide health information."
        ]
        
        self.farewells = [
            "Take care of yourself! Remember to consult a doctor for serious concerns.",
            "Stay healthy! Don't hesitate to seek medical advice when needed.",
            "Goodbye! Your health is important - prioritize it.",
            "Take care! Remember, I'm here for general health information."
        ]
    
    def get_intent(self, message):
        """Extract intent from user message"""
        message_lower = message.lower()
        
        # Define keywords for each intent
        intent_keywords = {
            'headache': ['headache', 'head pain', 'migraine', 'head hurts'],
            'fever': ['fever', 'temperature', 'hot', 'feverish', 'chills'],
            'cold': ['cold', 'flu', 'sore throat', 'cough', 'congestion', 'runny nose'],
            'diabetes': ['diabetes', 'blood sugar', 'glucose', 'diabetic'],
            'bp': ['blood pressure', 'bp', 'hypertension', 'high blood pressure'],
            'diet': ['diet', 'food', 'eat', 'nutrition', 'healthy eating'],
            'exercise': ['exercise', 'workout', 'physical activity', 'fitness', 'walking'],
            'sleep': ['sleep', 'insomnia', 'rest', 'tired', 'fatigue'],
            'medication': ['medicine', 'medication', 'pills', 'drugs', 'prescription'],
            'emergency': ['emergency', 'chest pain', 'heart attack', 'stroke', 'difficulty breathing', 'severe']
        }
        
        # Check for keywords
        for intent, keywords in intent_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return intent
        
        return 'general'
    
    def get_response(self, message):
        """Generate response based on user message"""
        intent = self.get_intent(message)
        
        # Handle greetings
        if any(word in message.lower() for word in ['hello', 'hi', 'hey', 'greetings']):
            return self.greetings[0]
        
        # Handle farewells
        if any(word in message.lower() for word in ['bye', 'goodbye', 'exit', 'quit']):
            return self.farewells[0]
        
        # Get response based on intent
        if intent in self.responses:
            response = self.responses[intent]
            return '\n'.join(response)
        else:
            return (
                "I understand you have a health question. While I can provide general information, "
                "it's always best to consult with your healthcare provider for personalized medical advice. "
                "\n\nYou can ask me about:\n"
                "• Headache relief\n"
                "• Fever management\n"
                "• Cold and flu symptoms\n"
                "• Diabetes care\n"
                "• Blood pressure management\n"
                "• Healthy diet tips\n"
                "• Exercise recommendations\n"
                "• Sleep hygiene\n"
                "• Medication management"
            )

def show_chatbot():
    """Display medical chatbot interface"""
    
    st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .chat-container {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 10px 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 10px 0;
        text-align: right;
    }
    .bot-message {
        background-color: #f5f5f5;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 10px 0;
        text-align: left;
    }
    .disclaimer {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .stButton > button {
        background-color: #00acc1;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 🤖 Medical Assistant Chatbot")
    st.markdown("## Ask me about your health concerns")
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ Important Disclaimer:</strong> This chatbot provides general health information and does not replace professional medical advice. 
        Always consult with your healthcare provider for medical concerns, diagnosis, or treatment.
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    chatbot = MedicalChatbot()
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message"><strong>🤖 Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Type your health question...",
                placeholder="e.g., What can I do for a headache?",
                key="chat_input"
            )
        
        with col2:
            submitted = st.form_submit_button("💬 Send", use_container_width=True)
        
        if submitted and user_input.strip():
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now()
            })
            
            # Get bot response
            bot_response = chatbot.get_response(user_input)
            
            # Add bot response to history
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': bot_response,
                'timestamp': datetime.now()
            })
            
            # Save conversation to database
            save_chat_message(st.session_state.user_id, user_input, bot_response)
            
            # Rerun to display new messages
            st.rerun()
    
    # Quick action buttons
    st.markdown("### 🚀 Quick Questions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    quick_questions = [
        ("What helps with headaches?", col1),
        ("How to manage fever?", col2),
        ("Healthy diet tips?", col3),
        ("Exercise recommendations?", col4)
    ]
    
    for question, column in quick_questions:
        with column:
            if st.button(question, use_container_width=True, key=f"quick_{question[:10]}"):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': question,
                    'timestamp': datetime.now()
                })
                
                bot_response = chatbot.get_response(question)
                st.session_state.chat_history.append({
                    'role': 'bot',
                    'content': bot_response,
                    'timestamp': datetime.now()
                })
                
                save_chat_message(st.session_state.user_id, question, bot_response)
                st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

def save_chat_message(user_id, user_message, bot_response):
    """Save chat message to database"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO chatbot_logs (user_id, user_message, bot_response) VALUES (?, ?, ?)",
            (user_id, user_message, bot_response)
        )
        
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error saving chat message: {e}")
