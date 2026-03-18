"""
ULTIMATE NLTK FIX FOR STREAMLIT CLOUD
This is the definitive solution for NLTK errors on Streamlit Cloud deployment
"""

import os
import sys
import nltk
import streamlit as st

def ultimate_nltk_setup():
    """Ultimate NLTK setup that works on Streamlit Cloud"""
    
    try:
        # Step 1: Set NLTK data path to multiple locations
        nltk_data_paths = [
            '/home/adminuser/nltk_data',  # Streamlit Cloud primary
            '/home/adminuser/.nltk_data',  # Alternative Streamlit path
            os.path.expanduser('~/nltk_data'),  # Home directory
            '/tmp/nltk_data',  # Temporary directory
            './nltk_data',  # Local directory
            os.path.join(os.getcwd(), 'nltk_data'),  # Current working
            '/mount/data/nltk_data',  # Mount point
            '/app/nltk_data',  # App directory
        ]
        
        # Add all paths to NLTK
        for path in nltk_data_paths:
            if path not in nltk.data.path:
                nltk.data.path.append(path)
        
        # Step 2: Create directories and test write permissions
        working_path = None
        for path in nltk_data_paths:
            try:
                os.makedirs(path, exist_ok=True)
                # Test write permissions
                test_file = os.path.join(path, 'nltk_test.txt')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                working_path = path
                st.success(f"✅ NLTK data path: {path}")
                break
            except Exception as e:
                continue
        
        if not working_path:
            st.error("❌ Could not find writable NLTK data directory")
            return False
        
        # Step 3: Download NLTK data with absolute paths
        nltk_packages = [
            ('tokenizers/punkt', 'punkt'),
            ('corpora/stopwords', 'stopwords'),
            ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
            ('corpora/wordnet', 'wordnet'),
            ('tokenizers/punkt_tab', 'punkt_tab')
        ]
        
        success_count = 0
        for resource, package in nltk_packages:
            try:
                # Check if already exists
                nltk.data.find(resource)
                st.success(f"✅ {package} already available")
                success_count += 1
            except LookupError:
                # Download with absolute path
                try:
                    st.info(f"📦 Downloading {package}...")
                    nltk.download(package, download_dir=working_path, quiet=False)
                    # Verify download
                    nltk.data.find(resource)
                    st.success(f"✅ {package} downloaded successfully")
                    success_count += 1
                except Exception as download_error:
                    st.error(f"❌ Failed to download {package}: {download_error}")
                    # Try alternative download method
                    try:
                        st.warning(f"🔄 Trying alternative download for {package}...")
                        nltk.download(package, quiet=True)
                        st.success(f"✅ {package} downloaded (alternative method)")
                        success_count += 1
                    except Exception as alt_error:
                        st.error(f"❌ Alternative download also failed: {alt_error}")
        
        # Step 4: Verify NLTK functionality
        try:
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            
            # Test tokenization
            test_text = "Hello world, this is a test for NLTK functionality."
            tokens = word_tokenize(test_text)
            
            # Test stopwords
            stop_words = set(stopwords.words('english'))
            
            if len(tokens) > 0 and len(stop_words) > 0:
                st.success("✅ NLTK functionality verified")
                return True
            else:
                st.error("❌ NLTK functionality test failed")
                return False
                
        except Exception as func_error:
            st.error(f"❌ NLTK functionality test error: {func_error}")
            return False
            
    except Exception as e:
        st.error(f"❌ Ultimate NLTK setup failed: {e}")
        return False

def create_no_nltk_fallback():
    """Create a complete fallback system when NLTK fails"""
    
    st.warning("⚠️ NLTK is not available. Using fallback systems.")
    
    # Create a simple sentiment analyzer without NLTK
    class SimpleSentimentAnalyzer:
        def __init__(self):
            self.positive_words = {
                'good', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'happy', 'joy',
                'love', 'like', 'enjoy', 'pleased', 'satisfied', 'content', 'glad',
                'delighted', 'excited', 'thrilled', 'cheerful', 'optimistic', 'positive'
            }
            
            self.negative_words = {
                'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'dislike',
                'angry', 'sad', 'depressed', 'unhappy', 'miserable', 'lonely',
                'anxious', 'worried', 'stressed', 'tired', 'exhausted', 'sick'
            }
        
        def predict_sentiment(self, text):
            words = text.lower().split()
            positive_count = sum(1 for word in words if word in self.positive_words)
            negative_count = sum(1 for word in words if word in self.negative_words)
            
            if positive_count > negative_count:
                return {'sentiment': 'positive', 'confidence': 0.8, 'method': 'simple_word_based'}
            elif negative_count > positive_count:
                return {'sentiment': 'negative', 'confidence': 0.8, 'method': 'simple_word_based'}
            else:
                return {'sentiment': 'neutral', 'confidence': 0.6, 'method': 'simple_word_based'}
        
        def get_sentiment_emoji(self, sentiment):
            emoji_map = {'positive': '😊', 'negative': '😔', 'neutral': '😐'}
            return emoji_map.get(sentiment, '😐')
    
    return SimpleSentimentAnalyzer()

# Test the ultimate fix
if __name__ == "__main__":
    st.title("🔧 Ultimate NLTK Fix Test")
    
    if st.button("🚀 Test Ultimate NLTK Setup"):
        if ultimate_nltk_setup():
            st.success("🎉 NLTK setup successful!")
        else:
            st.warning("⚠️ NLTK setup failed, using fallback...")
            analyzer = create_no_nltk_fallback()
            st.info("✅ Fallback system created successfully")
