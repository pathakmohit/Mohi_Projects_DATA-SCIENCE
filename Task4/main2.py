import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import spacy
import os
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Load medical NLP model
nlp = spacy.load("en_core_web_sm")

# Function to parse XML files and extract Q&A
def parse_medquad_xml(folder_path):
    data = []
    for root_folder, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root_folder, file)
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    focus = root.find("Focus").text.strip() if root.find("Focus") is not None else "Unknown"
                    
                    for qapair in root.findall(".//QAPair"):
                        question = qapair.find("Question").text.strip() if qapair.find("Question") is not None else "No Question"
                        answer = qapair.find("Answer").text.strip() if qapair.find("Answer") is not None else "No Answer"
                        data.append({"Focus": focus, "Question": question, "Answer": answer})
                
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")

    return pd.DataFrame(data)

# Paths
folder_path = r"D:\project101\Task4\MedQuAD-master\MedQuAD-master"  # XML dataset folder
csv_file_path = r"D:\project101\Task4\MedQuAD-master\MedQuAD-master\QA-TestSet-LiveQA-Med-Qrels-2479-Answers\QA-TestSet-LiveQA-Med-Qrels-2479-Answers\All-2479-Answers-retrieved-from-MedQuAD.csv"  # CSV file path

# Load XML Data
qa_data = parse_medquad_xml(folder_path)

# Load CSV Data
if os.path.exists(csv_file_path):
    prompt_data = pd.read_csv(csv_file_path)
else:
    print(f"Error: CSV file not found at {csv_file_path}")
    prompt_data = pd.DataFrame(columns=["Answer"])  # Empty DataFrame to avoid crashes

# Tokenize and prepare BM25 retrieval
if not qa_data.empty:
    questions = qa_data["Question"].tolist()
    tokenized_questions = [q.lower().split() for q in questions]
    bm25 = BM25Okapi(tokenized_questions)

    # Train ML model for Q&A matching
    tfidf_vectorizer = TfidfVectorizer()
    X_tfidf = tfidf_vectorizer.fit_transform(qa_data["Question"])
    y_labels = qa_data["Answer"]
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_tfidf, y_labels)
    joblib.dump((tfidf_vectorizer, model), "qa_model.pkl")
else:
    print("Error: No valid data found in XML files.")

# Function to retrieve best matching answer using BM25
def get_best_answer(user_query):
    if qa_data.empty:
        return "No data available.", "N/A"
    
    tokenized_query = user_query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    best_idx = scores.argmax()
    return qa_data.iloc[best_idx]["Answer"], qa_data.iloc[best_idx]["Focus"]

# Function to predict answer using ML model
def ml_predict_answer(user_query):
    try:
        tfidf_vectorizer, model = joblib.load("qa_model.pkl")
        query_tfidf = tfidf_vectorizer.transform([user_query])
        return model.predict(query_tfidf)[0]
    except Exception as e:
        print(f"ML Prediction Error: {e}")
        return "No prediction available."

# Medical entity recognition
def extract_entities(text):
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}
    return entities

# Streamlit UI
st.title("Medical Q&A Chatbot")
st.write("Ask a medical question based on the MedQuAD dataset.")

# User input options
input_option = st.radio("How would you like to ask a question?", ("Select a predefined question", "Type your own question"))

if input_option == "Select a predefined question":
    if prompt_data.empty:
        st.warning("No CSV data found. Please check the file path.")
    else:
        user_input = st.selectbox("Choose a medical question:", prompt_data["Answer"].tolist())
else:
    user_input = st.text_input("Type your medical question:")

if user_input:
    answer, disease = get_best_answer(user_input)
    ml_answer = ml_predict_answer(user_input)
    entities = extract_entities(user_input)
    
    st.subheader("Best Retrieved Answer:")
    st.write(answer)
    
    st.subheader("ML Predicted Answer:")
    st.write(ml_answer)
    
    st.subheader("Relevant Medical Condition:")
    st.write(disease)
    
    if entities:
        st.subheader("Detected Medical Terms:")
        st.json(entities)
