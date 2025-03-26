import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import time
import asyncio

# Define available models
models = {
    "Llama3": "llama3",  # Llama3 model
    "Mistral": "mistral",  # Mistral model
    "Falcon": "falcon",  # Falcon model
}

st.title("⚡️ Ultra-Fast Article Generator (Optimized for Responsiveness)")

# Model selection (default to Llama3)
default_model = list(models.keys())[0] if models else None
selected_model = st.selectbox("Choose an LLM:", list(models.keys()), index=0 if default_model in models else None)

@st.cache_resource(show_spinner=False)
def load_model(model_name):
    return OllamaLLM(model=model_name)

llm = load_model(models[selected_model])

system_instruction = "You are an expert writer. Generate *very* concise, well-structured, and engaging articles. Focus on extreme brevity for lightning-fast responses. Prioritize speed over extensive detail."

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_instruction),
    ("user", "{question}")
])

async def generate_article(topic):
    # Stream the response token by token for faster feedback
    response = ""
    async for chunk in llm.astream(prompt_template.format(question=topic)):
        response += chunk
        yield response  # Stream the response to the UI

async def main_async(topic):
    start_time = time.time()
    with st.spinner("Generating... (expecting rapid response)"):
        st.subheader("📝 Generated Article (Concise):")
        response_placeholder = st.empty()  # Placeholder for streaming response

        # Stream the response
        async for response in generate_article(topic):
            response_placeholder.write(response)

        execution_time = time.time() - start_time

        st.subheader("📊 Performance Metrics:")
        st.write(f"⏱ Response Time: {execution_time:.2f} seconds")
        st.write(f"🤖 Model Used: {selected_model}")

        if execution_time > 2:
            st.warning("Response time exceeded 2 seconds. Consider a smaller model or shorter prompts for faster results.")

input_text = st.text_area("Enter a topic (brevity is key for speed):")

if st.button("Generate Article"):
    if input_text.strip():
        try:
            # Run the async function using asyncio.run
            asyncio.run(main_async(input_text.strip()))
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a topic.")