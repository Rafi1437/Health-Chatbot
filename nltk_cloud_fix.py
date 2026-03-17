"""
NLTK Cloud Fix - Handles NLTK data for Streamlit Cloud deployment
"""

import os
import sys
import nltk
import streamlit as st

def setup_nltk_for_cloud():
    """Setup NLTK data specifically for cloud deployment"""
    
    # Create multiple possible NLTK data paths
    possible_paths = [
        '/home/adminuser/nltk_data',  # Streamlit Cloud
        os.path.expanduser('~/nltk_data'),  # Home directory
        '/tmp/nltk_data',  # Temporary directory
        './nltk_data',  # Local directory
        os.path.join(os.getcwd(), 'nltk_data')  # Current working directory
    ]
    
    # Add all possible paths to NLTK data path
    for path in possible_paths:
        if path not in nltk.data.path:
            nltk.data.path.append(path)
    
    # Find the best available path
    best_path = None
    for path in possible_paths:
        try:
            os.makedirs(path, exist_ok=True)
            # Test if we can write to this path
            test_file = os.path.join(path, 'test_write.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            best_path = path
            break
        except Exception:
            continue
    
    if best_path:
        st.info(f"📁 Using NLTK data path: {best_path}")
        
        # Download required NLTK data to the best path
        required_packages = [
            ('tokenizers/punkt', 'punkt'),
            ('corpora/stopwords', 'stopwords'),
            ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger')
        ]
        
        for resource, package in required_packages:
            try:
                nltk.data.find(resource)
                st.success(f"✅ {package} already available")
            except LookupError:
                st.warning(f"📦 Downloading {package}...")
                try:
                    nltk.download(package, download_dir=best_path, quiet=True)
                    st.success(f"✅ {package} downloaded successfully")
                except Exception as e:
                    st.error(f"❌ Failed to download {package}: {e}")
                    # Continue with other packages
                    continue
        
        return best_path
    else:
        st.error("❌ Could not find a writable directory for NLTK data")
        return None

def verify_nltk_setup():
    """Verify NLTK setup is working"""
    try:
        # Test basic NLTK functionality
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        
        # Test tokenization
        test_text = "Hello world, this is a test."
        tokens = word_tokenize(test_text)
        
        # Test stopwords
        stop_words = set(stopwords.words('english'))
        
        return True, "NLTK setup is working correctly"
    except Exception as e:
        return False, f"NLTK setup failed: {str(e)}"

if __name__ == "__main__":
    # Test the setup
    setup_nltk_for_cloud()
    is_working, message = verify_nltk_setup()
    
    if is_working:
        st.success("✅ NLTK setup verification passed!")
        st.info(message)
    else:
        st.error("❌ NLTK setup verification failed!")
        st.error(message)
