# Task 7 - Expert Chatbot for Computer Science

This project is an **Expert Chatbot for Computer Science** trained on the **arXiv dataset**. It provides intelligent responses based on user queries using **machine learning and large language models (LLMs)**.

## Features
- **Machine Learning-Based Text Classification** using Logistic Regression
- **Supports LLMs** like Llama3, Mistral, and Vicuna
- **Dataset Processing with Multithreading**
- **Streamlit-Based Web Interface**
- **FastAPI Backend for Model Inference**

## Project Structure
```
├── Backend.py            # Backend processing, training & inference
├── Frontend.py           # Streamlit-based frontend UI
├── chatbot_model.pkl     # Trained classification model
├── vectorizer.pkl        # TF-IDF vectorizer
├── label_encoder.pkl     # Label encoder
├── vicuna_model.pkl      # Vicuna model
├── vicuna_vectorizer.pkl # Vectorizer for Vicuna
├── vicuna_label_encoder.pkl # Label encoder for Vicuna
├── requirment.txt        # Project dependencies
├── README.md             # Documentation
```

## Installation
Ensure Python (>=3.7) is installed. Install dependencies using:
```sh
pip install -r requirment.txt
```

## Running the Application
### Start Backend API:
```sh
uvicorn Backend:app --host 0.0.0.0 --port 8000
```

### Run Streamlit Frontend:
```sh
streamlit run Frontend.py
```

## Data Source
The chatbot is trained on the **arXiv Computer Science dataset**. The dataset is stored in Google Drive:
🔗 [Dataset Link](your-google-drive-link-here)

## Usage
1. Enter a **query** related to computer science.
2. The chatbot predicts the **category** (AI, ML, NLP, etc.).
3. It generates a **response** using the selected LLM.

## Future Enhancements
- Fine-tune LLMs for better domain-specific responses
- Improve dataset classification using deep learning
- Add more categories from arXiv

