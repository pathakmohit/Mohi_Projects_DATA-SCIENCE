# Task 6 - AI-Powered Knowledge Expansion Chatbot

This project is an **AI-powered chatbot** that continuously expands its knowledge by fetching real-time web data, training a Word2Vec model, and updating its vector database.

## Features
- **Real-time Web Scraping** for knowledge updates
- **Word2Vec-Based Text Similarity**
- **Persistent Knowledge Storage** with Pickle
- **Automated Periodic Updates**
- **Cosine Similarity for Response Generation**

## Project Structure
```
├── main.py            # Core chatbot logic
├── faiss_index.bin    # Precomputed FAISS index (if applicable)
├── word2vec_model.pkl # Trained Word2Vec model
├── vector_database.pkl # Stored word embeddings
├── README.md          # Documentation
```

## Installation
Ensure Python (>=3.7) is installed. Install dependencies using:
```sh
pip install -r requirements.txt
```

## Running the Application
```sh
python main.py
```

## How It Works
1. The chatbot **fetches new data** from the web.
2. It **trains a Word2Vec model** on new text.
3. The **vector database updates** with learned knowledge.
4. Responses are generated using **word similarity and TF-IDF weighting**.
5. The chatbot runs periodic updates for continuous learning.

## Future Enhancements
- Implement FAISS for **faster vector searches**
- Improve **word similarity metrics**
- Enhance **multi-threaded data fetching**



