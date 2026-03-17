"""
Sentiment Analysis Model for Mental Health Monitoring
Uses NLTK and Scikit-learn for text classification
"""

import nltk
import pandas as pd
import numpy as np
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
import sys
sys.path.append(os.path.dirname(__file__))

# Download NLTK data with cloud-compatible path handling
try:
    import nltk
    import os
    import sys
    sys.path.append(os.path.dirname(__file__))
    
    # Create multiple possible NLTK data paths for cloud deployment
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
        print(f"📁 SentimentModel using NLTK data path: {best_path}")
        
        # Download required NLTK data to the best path
        required_packages = [
            ('tokenizers/punkt', 'punkt'),
            ('corpora/stopwords', 'stopwords')
        ]
        
        for resource, package in required_packages:
            try:
                nltk.data.find(resource)
                print(f"✅ {package} already available in sentiment_model")
            except LookupError:
                print(f"📦 SentimentModel downloading {package}...")
                try:
                    nltk.download(package, download_dir=best_path, quiet=True)
                    print(f"✅ {package} downloaded successfully in sentiment_model")
                except Exception as download_error:
                    print(f"⚠️  SentimentModel error downloading {package}: {download_error}")
                    # Continue with other downloads rather than failing
                    continue
    else:
        print("❌ SentimentModel could not find a writable directory for NLTK data")
                
except Exception as e:
    print(f"SentimentModel NLTK setup issue: {e}")
    print("Will attempt to continue with available data...")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class SentimentAnalyzer:
    """Sentiment Analysis Model for Mental Health"""
    
    def __init__(self):
        self.model = None
        self.stop_words = set(stopwords.words('english'))
        
    def preprocess_text(self, text):
        """Enhanced text preprocessing for sentiment analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Handle common emotional expressions and contractions
        contractions = {
            "i'm": "i am",
            "i've": "i have",
            "i'll": "i will",
            "i'd": "i would",
            "don't": "do not",
            "doesn't": "does not",
            "didn't": "did not",
            "can't": "cannot",
            "won't": "will not",
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "haven't": "have not",
            "hasn't": "has not",
            "hadn't": "had not",
            "shouldn't": "should not",
            "couldn't": "could not",
            "wouldn't": "would not",
            "mightn't": "might not",
            "mustn't": "must not"
        }
        
        for contraction, expansion in contractions.items():
            text = text.replace(contraction, expansion)
        
        # Remove special characters but keep important emotional punctuation
        text = re.sub(r'[^a-zA-Z\s!?\.]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords but keep important emotional words
        emotional_words = {
            'not', 'no', 'never', 'none', 'nothing', 'nowhere', 'neither', 'nor',
            'but', 'however', 'although', 'though', 'yet', 'still', 'anyway'
        }
        
        stop_words = self.stop_words - emotional_words
        tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
        
        # Join back to string
        processed_text = ' '.join(tokens)
        
        # Add emotional intensity markers
        if any(word in text for word in ['very', 'extremely', 'really', 'so', 'too']):
            processed_text += ' intense'
        if any(word in text for word in ['!', '!!!']):
            processed_text += ' exclamation'
            
        return processed_text
    
    def create_training_data(self):
        """Create comprehensive training dataset for sentiment analysis"""
        
        # Comprehensive mental health training data with all mood types
        training_data = [
            # Happy / Joyful Mood - Positive
            ("I feel great today", "positive"),
            ("I'm happy", "positive"),
            ("Feeling awesome!", "positive"),
            ("Everything is good", "positive"),
            ("So excited today!", "positive"),
            ("I'm feeling really happy today because everything seems to be going well and my mind feels light", "positive"),
            ("Today feels amazing, and I'm enjoying every moment with positive energy and motivation", "positive"),
            
            # Calm / Peaceful Mood - Positive
            ("I feel calm", "positive"),
            ("Peaceful day", "positive"),
            ("Relaxed and fine", "positive"),
            ("Mentally stable", "positive"),
            ("Feeling balanced", "positive"),
            ("I feel calm and relaxed today, with no major worries or stress in my mind", "positive"),
            ("My mind feels peaceful, and I'm able to think clearly without any pressure", "positive"),
            
            # Motivated / Confident Mood - Positive
            ("I feel confident", "positive"),
            ("Ready to work", "positive"),
            ("Fully motivated", "positive"),
            ("I can do this", "positive"),
            ("Feeling strong", "positive"),
            ("I feel motivated and confident today, ready to face challenges and achieve my goals", "positive"),
            ("I believe in myself today and feel prepared to handle anything that comes my way", "positive"),
            
            # Excited / Enthusiastic Mood - Positive
            ("I'm excited!", "positive"),
            ("Can't wait!", "positive"),
            ("Feeling thrilled", "positive"),
            ("So happy!", "positive"),
            ("Energetic", "positive"),
            ("I feel excited about upcoming opportunities and new experiences", "positive"),
            ("There's a lot of enthusiasm in me today, and I'm looking forward to what's coming next", "positive"),
            
            # Proud / Satisfied Mood - Positive
            ("Feeling proud", "positive"),
            ("Satisfied", "positive"),
            ("Achieved something", "positive"),
            ("Happy with myself", "positive"),
            ("Content", "positive"),
            ("I feel proud of myself for completing my tasks successfully", "positive"),
            ("There's a sense of satisfaction in me after achieving my goals", "positive"),
            
            # Additional positive examples
            ("Feeling blessed and grateful", "positive"),
            ("Had a wonderful day with family", "positive"),
            ("Good mood today", "positive"),
            ("Feeling optimistic about life", "positive"),
            ("Had a good night's sleep", "positive"),
            ("Enjoying my retirement", "positive"),
            ("Feeling loved and cared for", "positive"),
            
            # Neutral / Normal Mood - Neutral
            ("I'm okay today", "neutral"),
            ("Just another normal day", "neutral"),
            ("Feeling alright", "neutral"),
            ("Nothing special today", "neutral"),
            ("I'm doing fine", "neutral"),
            ("Regular day routine", "neutral"),
            ("Feeling normal", "neutral"),
            ("Just getting by", "neutral"),
            ("It's an ordinary day", "neutral"),
            ("Feeling neither good nor bad", "neutral"),
            ("I feel normal today, nothing particularly good or bad", "neutral"),
            ("It's just an ordinary day with no strong emotions", "neutral"),
            ("Fine", "neutral"),
            ("Normal day", "neutral"),
            ("Alright", "neutral"),
            
            # Sad / Depressed Mood - Negative
            ("I feel sad", "negative"),
            ("Not feeling good", "negative"),
            ("Low mood", "negative"),
            ("Feeling empty", "negative"),
            ("I'm down", "negative"),
            ("I feel a bit sad today, and my energy level is quite low", "negative"),
            ("There's a heavy feeling in my mind, and I don't feel very motivated to do anything", "negative"),
            
            # Angry / Frustrated Mood - Negative
            ("I'm angry", "negative"),
            ("So annoyed", "negative"),
            ("Feeling irritated", "negative"),
            ("This is frustrating", "negative"),
            ("I'm upset", "negative"),
            ("I feel frustrated today because things are not going as expected", "negative"),
            ("I'm feeling angry and irritated due to repeated problems and misunderstandings", "negative"),
            
            # Stressed / Anxious Mood - Negative
            ("Feeling stressed", "negative"),
            ("I'm anxious", "negative"),
            ("Nervous today", "negative"),
            ("Too much pressure", "negative"),
            ("Worried", "negative"),
            ("I feel stressed because there are many tasks and responsibilities on my mind", "negative"),
            ("I'm feeling anxious and worried about upcoming events and decisions", "negative"),
            
            # Tired / Exhausted Mood - Negative
            ("I'm tired", "negative"),
            ("Feeling sleepy", "negative"),
            ("Exhausted", "negative"),
            ("No energy", "negative"),
            ("Drained", "negative"),
            ("I feel extremely tired today and lack the energy to focus properly", "negative"),
            ("My body and mind feel exhausted after a long and busy day", "negative"),
            
            # Confused / Uncertain Mood - Negative
            ("I'm confused", "negative"),
            ("Not sure", "negative"),
            ("Feeling lost", "negative"),
            ("Unsure", "negative"),
            ("Doubtful", "negative"),
            ("I feel confused because I'm not sure what decision to make", "negative"),
            ("My mind is full of questions, and I'm struggling to find clarity", "negative"),
            
            # Disappointed Mood - Negative
            ("Disappointed", "negative"),
            ("Not satisfied", "negative"),
            ("Let down", "negative"),
            ("Feeling bad", "negative"),
            ("Upset", "negative"),
            ("I feel disappointed because things didn't turn out the way I expected", "negative"),
            ("My expectations were high, but the results made me feel low", "negative"),
            
            # Lonely / Isolated Mood - Negative
            ("Feeling lonely", "negative"),
            ("Alone", "negative"),
            ("Isolated", "negative"),
            ("No one around", "negative"),
            ("Empty inside", "negative"),
            ("I feel lonely today and miss having people around me", "negative"),
            ("There's a sense of isolation that makes me feel emotionally distant", "negative"),
            
            # Overwhelmed Mood - Negative
            ("Too much", "negative"),
            ("Overloaded", "negative"),
            ("Can't handle", "negative"),
            ("Mentally overloaded", "negative"),
            ("Burned out", "negative"),
            ("I feel overwhelmed because too many things are happening at the same time", "negative"),
            ("My mind feels overloaded with responsibilities and expectations", "negative"),
            
            # Additional negative examples
            ("Feeling sad and lonely", "negative"),
            ("I'm worried about my health", "negative"),
            ("Feeling depressed today", "negative"),
            ("Having anxiety issues", "negative"),
            ("Feeling isolated and alone", "negative"),
            ("Worried about the future", "negative"),
            ("Feeling unwell and tired", "negative"),
            ("Having trouble sleeping", "negative"),
            ("Feeling stressed and overwhelmed", "negative"),
            ("Concerned about my medication", "negative"),
            
            # Sarcastic / Playful Mood - Neutral (context-dependent)
            ("Yeah, great…", "neutral"),
            ("Just perfect", "neutral"),
            ("Amazing, obviously", "neutral"),
            ("Wow, nice", "neutral"),
            ("Sure, why not", "neutral"),
            ("Oh yeah, everything is just perfect today, as always", "neutral"),
            ("I'm feeling great, if you know what I mean", "neutral"),
        ]
        
        # Create DataFrame
        df = pd.DataFrame(training_data, columns=['text', 'sentiment'])
        
        # Preprocess text
        df['processed_text'] = df['text'].apply(self.preprocess_text)
        
        return df
    
    def train_model(self):
        """Train the enhanced sentiment analysis model"""
        # Get training data
        df = self.create_training_data()
        
        # Split data with stratification to ensure balanced classes
        X = df['processed_text']
        y = df['sentiment']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Create enhanced pipeline with better features
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=2000,  # Increased features
                ngram_range=(1, 3),  # Include trigrams
                min_df=1,  # Include all terms
                max_df=0.95,  # Remove very common terms
                sublinear_tf=True  # Use sublinear TF scaling
            )),
            ('classifier', MultinomialNB(
                alpha=0.1,  # Smoothing parameter
                fit_prior=True  # Learn class priors
            ))
        ])
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        print("Enhanced Model Training Complete!")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Show class distribution
        print("\nClass Distribution in Training Data:")
        print(y_train.value_counts())
        
        # Save model
        model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
        joblib.dump(self.model, model_path)
        print(f"Enhanced model saved to {model_path}")
        
        return self.model
    
    def load_model(self):
        """Load pre-trained model"""
        model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print("Model loaded successfully!")
            return True
        else:
            print("Model not found. Training new model...")
            self.train_model()
            return True
    
    def predict_sentiment(self, text):
        """Predict sentiment for given text"""
        if self.model is None:
            self.load_model()
        
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Predict sentiment
        prediction = self.model.predict([processed_text])[0]
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba([processed_text])[0]
        confidence = max(probabilities)
        
        return {
            'sentiment': prediction,
            'confidence': confidence,
            'probabilities': dict(zip(self.model.classes_, probabilities))
        }
    
    def get_sentiment_emoji(self, sentiment):
        """Get emoji for sentiment"""
        emoji_map = {
            'positive': '😊',
            'neutral': '😐',
            'negative': '😔'
        }
        return emoji_map.get(sentiment, '😐')
    
    def get_sentiment_color(self, sentiment):
        """Get color for sentiment"""
        color_map = {
            'positive': 'green',
            'neutral': 'orange',
            'negative': 'red'
        }
        return color_map.get(sentiment, 'gray')

# Initialize and train model
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # Check if model exists, if not train it
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    if not os.path.exists(model_path):
        print("Training new sentiment model...")
        analyzer.train_model()
    else:
        print("Model already exists. Loading...")
        analyzer.load_model()
    
    # Test predictions
    test_texts = [
        "I feel wonderful today!",
        "Just a normal day",
        "Feeling worried about my health"
    ]
    
    print("\nTesting predictions:")
    for text in test_texts:
        result = analyzer.predict_sentiment(text)
        print(f"Text: {text}")
        print(f"Sentiment: {result['sentiment']} ({result['confidence']:.2f})")
        print("---")
