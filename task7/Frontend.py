import streamlit as st
import asyncio
import pickle
import time
import numpy as np
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB

# Load trained model and assets
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))
model = pickle.load(open("chatbot_model.pkl", "rb"))

# Define available LLM models
models = {
    "Llama3": "llama3",
    "Mistral": "mistral",
    "vicuna": "vicuna",  # Replaced Phi with DeepSeek-R1
}

# Streamlit UI Title
st.title("⚡️ Expert Chatbot for Computer Science (arXiv Dataset)")

# Model selection
selected_model = st.selectbox("Choose an LLM:", list(models.keys()), index=0, key="model_selection")

# Load LLM model
@st.cache_resource(show_spinner=False)
def load_llm(model_name):
    return OllamaLLM(model=model_name)

llm = load_llm(models[selected_model])

# System instruction for chatbot
system_instruction = "You are an expert in computer science. Provide concise, well-structured, and engaging explanations."

# Chat prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_instruction),
    ("user", "{question}")
])

# Async function to generate response
async def generate_response(topic):
    response = ""
    async for chunk in llm.astream(prompt_template.format(question=topic)):
        response += chunk
        yield response

async def main_async(topic):
    start_time = time.time()
    with st.spinner("Generating response..."):
        st.subheader("📝 Generated Response:")
        response_placeholder = st.empty()

        async for response in generate_response(topic):
            response_placeholder.write(response)

        execution_time = time.time() - start_time
        st.subheader("📊 Performance Metrics:")
        st.write(f"⏱ Response Time: {execution_time:.2f} seconds")
        st.write(f"🤖 Model Used: {selected_model}")

# Run async query
def run_async_query(topic):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_async(topic))



# Main chatbot interface
input_text = st.text_area("Enter your query:", key="chat_input")

if st.button("Generate Response", key="chat_button"):
    if input_text.strip():
        try:
            # Predict category
            query_vectorized = vectorizer.transform([input_text.strip()])
            predicted_label = model.predict(query_vectorized)[0]
            predicted_category = label_encoder.inverse_transform([predicted_label])[0]

            st.write(f"📌 Predicted Category: {predicted_category}")
            run_async_query(input_text.strip())
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query.")
