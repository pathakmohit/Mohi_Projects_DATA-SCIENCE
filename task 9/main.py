import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon (only needed once)
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyze sentiment and return category (Positive, Negative, Neutral)."""
    score = sia.polarity_scores(text)['compound']
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def generate_response(sentiment):
    """Generate an appropriate response based on sentiment."""
    responses = {
        "Positive": "😊 I'm glad to hear that! How else can I assist you?",
        "Negative": "😔 I'm sorry to hear that. Let me know how I can help.",
        "Neutral": "🤖 Thanks for sharing! How can I assist you further?"
    }
    return responses.get(sentiment, "I am here to help!")

# Streamlit UI
st.title("Sentiment-Aware Chatbot")
st.write("Chat with me and I'll respond based on your emotions!")

# User input
user_input = st.text_input("You:")
if user_input:
    sentiment = analyze_sentiment(user_input)
    response = generate_response(sentiment)
    st.write(f"Chatbot ({sentiment}): {response}")