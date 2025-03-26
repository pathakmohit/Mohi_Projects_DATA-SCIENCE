import json
import pickle
import numpy as np
import nltk
import os
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# Disable TensorFlow OneDNN optimization to avoid conflicts
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Initialize lemmatizer and download NLTK resources
lemmatizer = WordNetLemmatizer()
nltk.download("punkt")
nltk.download("wordnet")

# ✅ **Dataset Path**
file_path = "D:/project101/task7/arxiv-metadata-oai-snapshot.json"

# ✅ **Load and Process Dataset with Multithreading**
def load_dataset(file_path, max_records=10000):
    texts, labels = [], []
    
    def process_line(line):
        try:
            data = json.loads(line)
            title = data.get("title", "").strip()
            abstract = data.get("abstract", "").strip()
            categories = data.get("categories", "").split()

            # Map categories to broader groups
            category_map = {
                "cs.AI": "Artificial Intelligence",
                "cs.LG": "Machine Learning",
                "cs.CL": "Computational Linguistics",
                "cs.NE": "Neural Networks",
                "cs.CV": "Computer Vision",
                "cs.DS": "Data Science",
                "cs.IR": "Information Retrieval",
            }

            # Assign mapped category or default "Other CS"
            matched_category = next((category_map[cat] for cat in categories if cat in category_map), "Other CS")

            if matched_category:
                return title + " " + abstract, matched_category
        except json.JSONDecodeError:
            return None

    with open(file_path, "r", encoding="utf-8") as file:
        with ThreadPoolExecutor() as executor:
            for result in executor.map(process_line, file):
                if result and len(texts) < max_records:
                    texts.append(result[0])
                    labels.append(result[1])

    return texts, labels

# ✅ **Balance Dataset to Avoid Overfitting**
def balance_dataset(texts, labels, max_per_class=800):
    category_counts = Counter(labels)
    balanced_texts, balanced_labels = [], []
    category_seen = {}

    for text, label in zip(texts, labels):
        if category_seen.get(label, 0) < max_per_class:
            balanced_texts.append(text)
            balanced_labels.append(label)
            category_seen[label] = category_seen.get(label, 0) + 1

    return balanced_texts, balanced_labels

# ✅ **Train Classification Model**
def train_text_classifier(texts, labels):
    # Encode labels
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    # Split data BEFORE TF-IDF transformation
    X_train_texts, X_test_texts, y_train, y_test = train_test_split(
        texts, labels_encoded, test_size=0.2, random_state=42, shuffle=True
    )

    # TF-IDF Vectorization (Optimized with max_df)
    vectorizer = TfidfVectorizer(max_features=3000, stop_words="english", sublinear_tf=True, max_df=0.85)
    X_train = vectorizer.fit_transform(X_train_texts)
    X_test = vectorizer.transform(X_test_texts)

    # Use Logistic Regression (Better than Naïve Bayes)
    model = LogisticRegression(max_iter=2000, solver="lbfgs", multi_class="ovr")
    model.fit(X_train, y_train)

    # Evaluate Model
    accuracy = model.score(X_test, y_test)
    print(f"✅ Model Training Complete | Accuracy: {accuracy:.4f}")

    return model, vectorizer, label_encoder

# ✅ **Save Model and Assets**
def save_model(model, vectorizer, label_encoder):
    try:
        pickle.dump(model, open("chatbot_model.pkl", "wb"))
        pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
        pickle.dump(label_encoder, open("label_encoder.pkl", "wb"))
        print("✅ Model and assets saved successfully!")
    except Exception as e:
        print(f"❌ Error saving model: {e}")

# ✅ **Load Model for Inference**
def load_model():
    try:
        model = pickle.load(open("chatbot_model.pkl", "rb"))
        vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
        label_encoder = pickle.load(open("label_encoder.pkl", "rb"))
        print("✅ Model loaded successfully!")
        return model, vectorizer, label_encoder
    except FileNotFoundError:
        print("❌ Error: Model files not found. Train the model first!")
        return None, None, None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None, None, None

# ✅ **Search Papers in Dataset**
def search_papers(query, file_path, max_results=5):
    results = []
    query_lower = query.lower()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    data = json.loads(line)
                    title = data.get("title", "").lower()
                    abstract = data.get("abstract", "").lower()
                    categories = data.get("categories", "").lower()

                    if query_lower in title or query_lower in abstract or query_lower in categories:
                        results.append({
                            "id": data.get("id"),
                            "title": data.get("title"),
                            "authors": data.get("authors"),
                            "categories": data.get("categories"),
                            "abstract": data.get("abstract"),
                            "doi": data.get("doi"),
                            "update_date": data.get("update_date")
                        })

                    if len(results) >= max_results:
                        break  

                except json.JSONDecodeError:
                    continue  

        return results

    except FileNotFoundError:
        print("❌ Error: Dataset file not found!")
        return []

# ✅ **Main Execution**
if __name__ == "__main__":
    print("🚀 Starting Backend Process...")

    # Load Dataset
    texts, labels = load_dataset(file_path)

    # If dataset is empty, stop execution
    if not texts:
        print("❌ No data found! Exiting...")
        exit(1)

    # Balance Dataset
    texts, labels = balance_dataset(texts, labels)

    # Train Model
    model, vectorizer, label_encoder = train_text_classifier(texts, labels)

    # Save Model
    save_model(model, vectorizer, label_encoder)

    print("🎯 Backend setup complete!")
