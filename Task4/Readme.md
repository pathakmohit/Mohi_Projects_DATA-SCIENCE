# Task 4 - Medical Q&A Chatbot

This project is a **Medical Q&A Chatbot** built using the **MedQuAD dataset**. It retrieves and predicts answers to medical questions using **natural language processing and machine learning**.

## Features
- **Question Retrieval** using BM25 ranking
- **Answer Prediction** with KNN and TF-IDF
- **Medical Entity Recognition** using SpaCy
- **Dual Input**: Predefined or custom questions
- **Streamlit-Based Web Interface**

## Project Structure
```
├── app.py                # Main Streamlit application
├── download_from_drive.py # Google Drive download script
├── data/                 # Folder for MedQuAD dataset
├── qa_model.pkl          # Trained ML model
├── requirements.txt      # Project dependencies
├── README.md             # Documentation
```

## Installation
Ensure Python (>=3.9) is installed. Install dependencies using:
```sh
pip install -r requirements.txt
```

## Running the Application
### Start Streamlit App:
```sh
streamlit run app.py
```

## Data Source
The chatbot uses the **MedQuAD dataset**. The dataset is stored in Google Drive:
🔗 [Dataset Link](https://drive.google.com/drive/folders/1kZrd9Ir8h8Z_iMJgwXCqyAGIvHujsgin?usp=drive_link)

## Usage
1. Choose a **predefined question** from the dropdown or type a **custom question**.
2. View the **retrieved answer**, **ML-predicted answer**, **medical condition**, and **entities**.

## Future Enhancements
- Improve answer accuracy with advanced NLP models
- Expand dataset with more medical Q&A pairs
- Add support for real-time medical updates

