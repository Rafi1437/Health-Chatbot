"""
Fallback Sentiment Analysis - Works without NLTK
Used when NLTK is not available in cloud deployment
"""

import re
from typing import Dict, Any

class FallbackSentimentAnalyzer:
    """Fallback sentiment analyzer that works without NLTK"""
    
    def __init__(self):
        # Simple word lists for sentiment analysis
        self.positive_words = {
            'good', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'happy', 'joy', 
            'love', 'like', 'enjoy', 'pleased', 'satisfied', 'content', 'glad', 'delighted',
            'excited', 'thrilled', 'cheerful', 'optimistic', 'positive', 'bright', 'peaceful',
            'calm', 'relaxed', 'comfortable', 'better', 'best', 'awesome', 'perfect', 'nice'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'dislike', 'angry',
            'sad', 'depressed', 'unhappy', 'miserable', 'lonely', 'anxious', 'worried',
            'stressed', 'tired', 'exhausted', 'weak', 'sick', 'pain', 'hurt', 'difficult',
            'hard', 'problem', 'trouble', 'issue', 'concern', 'worry', 'fear', 'afraid',
            'scared', 'nervous', 'upset', 'disappointed', 'frustrated', 'annoyed', 'bothered'
        }
        
        self.neutral_words = {
            'okay', 'fine', 'alright', 'normal', 'regular', 'usual', 'typical', 'average',
            'moderate', 'reasonable', 'acceptable', 'sufficient', 'adequate', 'standard',
            'ordinary', 'common', 'general', 'basic', 'simple', 'clear', 'straightforward'
        }
    
    def preprocess_text(self, text: str) -> list:
        """Simple text preprocessing without NLTK"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Split into words
        words = text.split()
        
        # Remove empty strings
        words = [word for word in words if word]
        
        return words
    
    def predict_sentiment(self, text: str) -> Dict[str, Any]:
        """Predict sentiment using simple word-based approach"""
        try:
            words = self.preprocess_text(text)
            
            if not words:
                return {
                    'sentiment': 'neutral',
                    'confidence': 0.5,
                    'method': 'fallback_empty'
                }
            
            # Count sentiment words
            positive_count = sum(1 for word in words if word in self.positive_words)
            negative_count = sum(1 for word in words if word in self.negative_words)
            neutral_count = sum(1 for word in words if word in self.neutral_words)
            
            total_sentiment_words = positive_count + negative_count + neutral_count
            
            if total_sentiment_words == 0:
                # No sentiment words found, analyze based on context
                if any(word in text.lower() for word in ['hello', 'hi', 'hey', 'good morning']):
                    return {
                        'sentiment': 'positive',
                        'confidence': 0.6,
                        'method': 'fallback_greeting'
                    }
                else:
                    return {
                        'sentiment': 'neutral',
                        'confidence': 0.5,
                        'method': 'fallback_no_sentiment_words'
                    }
            
            # Calculate sentiment scores
            positive_score = positive_count / total_sentiment_words
            negative_score = negative_count / total_sentiment_words
            neutral_score = neutral_count / total_sentiment_words
            
            # Determine sentiment
            if positive_score > negative_score and positive_score > neutral_score:
                sentiment = 'positive'
                confidence = min(0.5 + positive_score * 0.5, 0.9)
            elif negative_score > positive_score and negative_score > neutral_score:
                sentiment = 'negative'
                confidence = min(0.5 + negative_score * 0.5, 0.9)
            else:
                sentiment = 'neutral'
                confidence = max(0.5, neutral_score)
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'method': 'fallback_word_based',
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': neutral_count
            }
            
        except Exception as e:
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'method': 'fallback_error',
                'error': str(e)
            }
    
    def get_sentiment_emoji(self, sentiment: str) -> str:
        """Get emoji for sentiment"""
        emoji_map = {
            'positive': '😊',
            'negative': '😔',
            'neutral': '😐'
        }
        return emoji_map.get(sentiment, '😐')

# Test the fallback analyzer
if __name__ == "__main__":
    analyzer = FallbackSentimentAnalyzer()
    
    test_texts = [
        "I am feeling very happy today!",
        "I am sad and worried about everything.",
        "I am okay, just a normal day.",
        "Hello, how are you?",
        "This is terrible and awful."
    ]
    
    for text in test_texts:
        result = analyzer.predict_sentiment(text)
        print(f"Text: '{text}'")
        print(f"Sentiment: {result['sentiment']} (Confidence: {result['confidence']:.2f})")
        print(f"Method: {result['method']}")
        print("-" * 50)
