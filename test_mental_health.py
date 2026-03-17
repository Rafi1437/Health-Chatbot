"""
Test script to verify mental health module functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from ml.sentiment_model import SentimentAnalyzer

def test_sentiment_model():
    """Test the sentiment analysis model"""
    print("Testing Sentiment Analysis Model...")
    
    analyzer = SentimentAnalyzer()
    analyzer.load_model()
    
    test_texts = [
        "I feel wonderful today!",
        "Just a normal day",
        "Feeling worried about my health"
    ]
    
    for text in test_texts:
        result = analyzer.predict_sentiment(text)
        print(f"Text: {text}")
        print(f"Sentiment: {result['sentiment']} ({result['confidence']:.2f})")
        print("---")
    
    print("✅ Sentiment model test completed successfully!")

if __name__ == "__main__":
    test_sentiment_model()
