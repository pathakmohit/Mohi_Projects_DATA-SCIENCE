import gensim
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import time
import requests
from bs4 import BeautifulSoup
import threading
import pickle  # For persistent storage

# Step 1: Initialize a vector database (dictionary for in-memory storage)
vector_database = {}
corpus_data = []  # Stores all fetched and processed text data
MODEL_PATH = "word2vec_model.pkl"
DB_PATH = "vector_database.pkl"

# Step 2: Train a Word2Vec model on the initial corpus
def train_word2vec(corpus):
    sentences = [sentence.split() for sentence in corpus]
    model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
    return model

# Step 3: Update the vector database with new information
def update_vector_database(model, new_data):
    global vector_database
    for sentence in new_data:
        words = sentence.split()
        for word in words:
            if word in model.wv:
                vector_database[word] = model.wv[word]
    save_data()

# Step 4: Fetch new information from the web
def fetch_new_information(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        new_data = [p.get_text() for p in soup.find_all('p') if len(p.get_text().split()) > 5]  # Filter short texts
        return new_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# Step 5: Generate responses using word similarity and TF-IDF weighting
def generate_response(user_input, model):
    global vector_database
    if not vector_database:
        return "I'm still learning. Please ask later."
    
    user_words = user_input.split()
    response_words = []
    
    for word in user_words:
        if word in vector_database:
            similar_words = model.wv.most_similar(word, topn=3)
            response_words.append(similar_words[0][0])  # Pick the closest match
        else:
            response_words.append(word)  # Keep unknown words unchanged
    
    return ' '.join(response_words)

# Step 6: Periodically update the knowledge base
def periodic_update(urls, model, interval=3600):  # Updates every hour
    global corpus_data
    while True:
        for url in urls:
            new_data = fetch_new_information(url)
            if new_data:
                corpus_data.extend(new_data)
                model.build_vocab([sentence.split() for sentence in new_data], update=True)
                model.train([sentence.split() for sentence in new_data], total_examples=len(new_data), epochs=5)
                update_vector_database(model, new_data)
                print(f"Vector database updated from {url}")
        time.sleep(interval)

# Step 7: Persistent Storage
def save_data():
    with open(DB_PATH, "wb") as db_file:
        pickle.dump(vector_database, db_file)
    with open(MODEL_PATH, "wb") as model_file:
        pickle.dump(model, model_file)

def load_data():
    global vector_database, model
    if os.path.exists(DB_PATH) and os.path.exists(MODEL_PATH):
        with open(DB_PATH, "rb") as db_file:
            vector_database = pickle.load(db_file)
        with open(MODEL_PATH, "rb") as model_file:
            model = pickle.load(model_file)

# Modified main execution block
if __name__ == "__main__":
    print("Initializing chatbot...")
    load_data()
    
    # Check if model exists, otherwise initialize with default corpus
    try:
        if 'model' not in globals():
            initial_corpus = [
                "artificial intelligence is transforming technology rapidly",
                "machine learning enables computers to learn from data",
                "natural language processing helps machines understand human language"
            ]
            corpus_data.extend(initial_corpus)
            model = train_word2vec(initial_corpus)
            update_vector_database(model, initial_corpus)
            print("Initialized with default corpus")
        else:
            print("Loaded existing model")
            
        # Start update thread with real news sources
        news_sources = [
            "https://www.bbc.com/news/technology",
            "https://techcrunch.com/"
        ]
        update_thread = threading.Thread(
            target=periodic_update,
            args=(news_sources, model, 1800)  # Update every 30 minutes instead of hour
        )
        update_thread.daemon = True
        update_thread.start()
        
        print("Chatbot ready! Type 'exit' or 'quit' to stop.")
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    print("Saving data and shutting down...")
                    save_data()
                    break
                if user_input:  # Only process non-empty input
                    response = generate_response(user_input, model)
                    print(f"Chatbot: {response}")
            except KeyboardInterrupt:
                print("\nInterrupted by user. Saving data...")
                save_data()
                break
            except Exception as e:
                print(f"Error processing input: {e}")
                
    except Exception as e:
        print(f"Failed to initialize chatbot: {e}")