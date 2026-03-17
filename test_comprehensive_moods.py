"""
Comprehensive test script for all mood types
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from ml.sentiment_model import SentimentAnalyzer

def test_all_moods():
    """Test all mood types with both short and long responses"""
    
    analyzer = SentimentAnalyzer()
    analyzer.load_model()
    
    # Test cases organized by expected sentiment
    test_cases = {
        'positive': [
            # Happy / Joyful Mood
            "I feel great today",
            "I'm happy",
            "Feeling awesome!",
            "Everything is good",
            "So excited today!",
            "I'm feeling really happy today because everything seems to be going well and my mind feels light",
            "Today feels amazing, and I'm enjoying every moment with positive energy and motivation",
            
            # Calm / Peaceful Mood
            "I feel calm",
            "Peaceful day",
            "Relaxed and fine",
            "Mentally stable",
            "Feeling balanced",
            "I feel calm and relaxed today, with no major worries or stress in my mind",
            "My mind feels peaceful, and I'm able to think clearly without any pressure",
            
            # Motivated / Confident Mood
            "I feel confident",
            "Ready to work",
            "Fully motivated",
            "I can do this",
            "Feeling strong",
            "I feel motivated and confident today, ready to face challenges and achieve my goals",
            "I believe in myself today and feel prepared to handle anything that comes my way",
            
            # Excited / Enthusiastic Mood
            "I'm excited!",
            "Can't wait!",
            "Feeling thrilled",
            "So happy!",
            "Energetic",
            "I feel excited about upcoming opportunities and new experiences",
            "There's a lot of enthusiasm in me today, and I'm looking forward to what's coming next",
            
            # Proud / Satisfied Mood
            "Feeling proud",
            "Satisfied",
            "Achieved something",
            "Happy with myself",
            "Content",
            "I feel proud of myself for completing my tasks successfully",
            "There's a sense of satisfaction in me after achieving my goals",
        ],
        
        'neutral': [
            # Neutral / Normal Mood
            "I'm okay today",
            "Just another normal day",
            "Feeling alright",
            "Nothing special today",
            "I'm doing fine",
            "Regular day routine",
            "Feeling normal",
            "Just getting by",
            "It's an ordinary day",
            "Feeling neither good nor bad",
            "I feel normal today, nothing particularly good or bad",
            "It's just an ordinary day with no strong emotions",
            "Fine",
            "Normal day",
            "Alright",
            
            # Sarcastic / Playful Mood
            "Yeah, great…",
            "Just perfect",
            "Amazing, obviously",
            "Wow, nice",
            "Sure, why not",
            "Oh yeah, everything is just perfect today, as always",
            "I'm feeling great, if you know what I mean",
        ],
        
        'negative': [
            # Sad / Depressed Mood
            "I feel sad",
            "Not feeling good",
            "Low mood",
            "Feeling empty",
            "I'm down",
            "I feel a bit sad today, and my energy level is quite low",
            "There's a heavy feeling in my mind, and I don't feel very motivated to do anything",
            
            # Angry / Frustrated Mood
            "I'm angry",
            "So annoyed",
            "Feeling irritated",
            "This is frustrating",
            "I'm upset",
            "I feel frustrated today because things are not going as expected",
            "I'm feeling angry and irritated due to repeated problems and misunderstandings",
            
            # Stressed / Anxious Mood
            "Feeling stressed",
            "I'm anxious",
            "Nervous today",
            "Too much pressure",
            "Worried",
            "I feel stressed because there are many tasks and responsibilities on my mind",
            "I'm feeling anxious and worried about upcoming events and decisions",
            
            # Tired / Exhausted Mood
            "I'm tired",
            "Feeling sleepy",
            "Exhausted",
            "No energy",
            "Drained",
            "I feel extremely tired today and lack the energy to focus properly",
            "My body and mind feel exhausted after a long and busy day",
            
            # Confused / Uncertain Mood
            "I'm confused",
            "Not sure",
            "Feeling lost",
            "Unsure",
            "Doubtful",
            "I feel confused because I'm not sure what decision to make",
            "My mind is full of questions, and I'm struggling to find clarity",
            
            # Disappointed Mood
            "Disappointed",
            "Not satisfied",
            "Let down",
            "Feeling bad",
            "Upset",
            "I feel disappointed because things didn't turn out the way I expected",
            "My expectations were high, but the results made me feel low",
            
            # Lonely / Isolated Mood
            "Feeling lonely",
            "Alone",
            "Isolated",
            "No one around",
            "Empty inside",
            "I feel lonely today and miss having people around me",
            "There's a sense of isolation that makes me feel emotionally distant",
            
            # Overwhelmed Mood
            "Too much",
            "Overloaded",
            "Can't handle",
            "Mentally overloaded",
            "Burned out",
            "I feel overwhelmed because too many things are happening at the same time",
            "My mind feels overloaded with responsibilities and expectations",
        ]
    }
    
    print("🧠 COMPREHENSIVE MOOD ANALYSIS TEST")
    print("=" * 60)
    
    total_tests = 0
    correct_predictions = 0
    
    for expected_sentiment, texts in test_cases.items():
        print(f"\n🎯 Testing {expected_sentiment.upper()} moods:")
        print("-" * 40)
        
        category_correct = 0
        category_total = 0
        
        for text in texts:
            result = analyzer.predict_sentiment(text)
            predicted = result['sentiment']
            confidence = result['confidence']
            
            total_tests += 1
            category_total += 1
            
            if predicted == expected_sentiment:
                correct_predictions += 1
                category_correct += 1
                status = "✅"
            else:
                status = "❌"
            
            # Show first few examples from each category
            if category_total <= 3:
                print(f"{status} '{text[:50]}...' -> {predicted} ({confidence:.2f})")
        
        accuracy = (category_correct / category_total) * 100 if category_total > 0 else 0
        print(f"📊 Category Accuracy: {accuracy:.1f}% ({category_correct}/{category_total})")
    
    # Overall accuracy
    overall_accuracy = (correct_predictions / total_tests) * 100 if total_tests > 0 else 0
    print(f"\n🎉 OVERALL ACCURACY: {overall_accuracy:.1f}% ({correct_predictions}/{total_tests})")
    
    if overall_accuracy >= 80:
        print("🌟 EXCELLENT! The model is working very well!")
    elif overall_accuracy >= 70:
        print("👍 GOOD! The model is performing well!")
    elif overall_accuracy >= 60:
        print("👌 ACCEPTABLE! The model is working reasonably well!")
    else:
        print("⚠️ NEEDS IMPROVEMENT! Consider adding more training data.")

if __name__ == "__main__":
    test_all_moods()
