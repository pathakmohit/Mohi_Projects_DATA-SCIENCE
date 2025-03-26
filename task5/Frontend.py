import streamlit as st
import requests
import base64
from PIL import Image
import io

BACKEND_URL = "http://localhost:8000"  # Adjust based on your backend deployment

st.title("Multi-Modal Chatbot")
st.write("This chatbot accepts text or image input and responds accordingly.")

# Text input
user_input = st.text_area("Enter your message:")

# Image input
def to_image(uploaded_file):
    if uploaded_file is not None:
        try:
            # Open the image in memory to avoid reading it multiple times
            image = Image.open(uploaded_file)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")  # Ensure saving as PNG
            image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return image_base64
        except Exception as e:
            st.error(f"Error processing image: {e}")
            return None
    return None

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Handle sending the request to backend
if st.button("Send"):
    if not user_input and not uploaded_file:
        st.warning("Please enter a message or upload an image.")
    else:
        # Convert image to base64 if available
        image_base64 = to_image(uploaded_file)
        
        # Prepare data for the backend
        data = {"user_input": user_input, "image_input": image_base64}
        
        with st.spinner("Sending request to chatbot..."):
            response = requests.post(f"{BACKEND_URL}/chat", json=data)
        
        # Handle the response
        if response.status_code == 200:
            st.write("### Chatbot Response:")
            st.write(response.json()["response"])
        else:
            st.error("Error communicating with backend.")
