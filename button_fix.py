"""
Button Fix for Streamlit - Ensures single-click functionality
Addresses issues where buttons require multiple clicks to work
"""

import streamlit as st

def apply_button_fix():
    """Apply comprehensive button fix for better responsiveness"""
    
    st.markdown("""
    <style>
    /* Enhanced button styles for single-click functionality */
    .stButton > button {
        background-color: #6f42c1 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: 2px solid #6f42c1 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        touch-action: manipulation !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        min-height: 44px !important;
        min-width: 120px !important;
        width: 100% !important;
        display: block !important;
        position: relative !important;
        z-index: 10 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        outline: none !important;
        text-align: center !important;
        line-height: 1.4 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    /* Button hover effects */
    .stButton > button:hover {
        background-color: #5a3d8a !important;
        border-color: #5a3d8a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Button active/pressed state */
    .stButton > button:active {
        background-color: #4c2f7d !important;
        border-color: #4c2f7d !important;
        transform: translateY(0px) !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    /* Button focus state */
    .stButton > button:focus {
        outline: 2px solid #6f42c1 !important;
        outline-offset: 2px !important;
    }
    
    /* Mobile-specific button fixes */
    @media (max-width: 768px) {
        .stButton > button {
            font-size: 18px !important;
            padding: 14px 28px !important;
            min-height: 48px !important;
            min-width: 140px !important;
            margin: 8px 0 !important;
        }
    }
    
    /* Form button container fixes */
    .stForm {
        margin-bottom: 20px !important;
    }
    
    .stForm > div {
        background-color: transparent !important;
        padding: 0 !important;
        border: none !important;
    }
    
    /* Button container spacing */
    div[data-testid="stForm"] {
        margin: 10px 0 !important;
    }
    
    /* Streamlit button element fixes */
    button[kind="primary"] {
        background-color: #6f42c1 !important;
        color: white !important;
        border: 2px solid #6f42c1 !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        touch-action: manipulation !important;
        min-height: 44px !important;
        transition: all 0.2s ease !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #5a3d8a !important;
        border-color: #5a3d8a !important;
    }
    
    button[kind="primary"]:active {
        background-color: #4c2f7d !important;
        border-color: #4c2f7d !important;
    }
    
    /* Input field fixes for better form interaction */
    .stTextInput > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > select {
        border: 2px solid #dee2e6 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 16px !important;
        transition: border-color 0.2s ease !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stTextInput > div > input:focus,
    .stTextArea > div > textarea:focus,
    .stSelectbox > div > select:focus {
        border-color: #6f42c1 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(111, 66, 193, 0.1) !important;
    }
    
    /* Mobile input fixes */
    @media (max-width: 768px) {
        .stTextInput > div > input,
        .stTextArea > div > textarea,
        .stSelectbox > div > select {
            font-size: 18px !important;
            padding: 14px !important;
            min-height: 44px !important;
        }
    }
    
    /* Prevent double-click issues */
    .stButton > button {
        -webkit-tap-highlight-color: transparent !important;
        -webkit-touch-callout: none !important;
        -webkit-user-select: none !important;
        user-select: none !important;
    }
    
    /* Loading state fixes */
    .stButton > button:disabled {
        opacity: 0.6 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }
    
    /* Sidebar button fixes */
    .css-1lcbm0y {
        padding: 10px 0 !important;
    }
    
    .css-1lcbm0y button {
        margin: 5px 0 !important;
        width: 100% !important;
        text-align: left !important;
    }
    
    /* Navigation button fixes */
    .css-17qicbe {
        padding: 8px 12px !important;
    }
    
    .css-17qicbe button {
        width: 100% !important;
        margin: 4px 0 !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        min-height: 40px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def enhanced_button(text, key=None, help=None, on_click=None, args=None, type="primary", disabled=False, use_container_width=True):
    """Enhanced button with better click handling"""
    
    # Add JavaScript for better click handling
    st.markdown("""
    <script>
    // Prevent double-click and ensure single-click functionality
    document.addEventListener('DOMContentLoaded', function() {
        // Add click prevention to all buttons
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            let isProcessing = false;
            
            button.addEventListener('click', function(e) {
                if (isProcessing) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }
                
                isProcessing = true;
                
                // Reset processing state after a short delay
                setTimeout(() => {
                    isProcessing = false;
                }, 500);
            });
            
            // Prevent double-tap on mobile
            button.addEventListener('touchend', function(e) {
                e.preventDefault();
                const clickEvent = new Event('click');
                button.dispatchEvent(clickEvent);
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Create enhanced button
    return st.button(
        text,
        key=key,
        help=help,
        on_click=on_click,
        args=args,
        type=type,
        disabled=disabled,
        use_container_width=use_container_width
    )

def enhanced_form_submit_button(label, key=None, help=None, on_click=None, args=None, disabled=False):
    """Enhanced form submit button"""
    
    return st.form_submit_button(
        label,
        key=key,
        help=help,
        on_click=on_click,
        args=args,
        disabled=disabled
    )

# Test the button fix
if __name__ == "__main__":
    st.title("🔧 Button Fix Test")
    
    apply_button_fix()
    
    st.markdown("### Button Fix Test")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Regular Button:**")
        if st.button("Regular Button"):
            st.success("Regular button clicked!")
    
    with col2:
        st.markdown("**Enhanced Button:**")
        if enhanced_button("Enhanced Button"):
            st.success("Enhanced button clicked!")
    
    st.markdown("### Form Test")
    
    with st.form("test_form"):
        text_input = st.text_input("Enter something:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.form_submit_button("Regular Submit"):
                st.success(f"Regular form submitted: {text_input}")
        
        with col2:
            if enhanced_form_submit_button("Enhanced Submit"):
                st.success(f"Enhanced form submitted: {text_input}")
