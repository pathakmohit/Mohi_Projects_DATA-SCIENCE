import io
import base64
import time
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
import google.generativeai as genai
import uvicorn
import os
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate API Key
if not GEMINI_API_KEY:
    raise ValueError("Google Gemini API key is missing. Please set GEMINI_API_KEY in .env file.")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model with generation configuration
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

try:
    gemini_model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )
except Exception as e:
    raise ValueError(f"Error initializing Gemini model: {e}")

# Create FastAPI instance
app = FastAPI()

# Define input schema
class ChatRequest(BaseModel):
    user_input: str
    image_input: str = None  # Optional base64 image

def image_to_base64(image):
    """Converts a PIL Image to a base64 encoded string."""
    if image.mode == "RGBA":
        image = image.convert("RGB")  # Convert RGBA to RGB to avoid JPEG errors
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")  # Ensure saving as JPEG
    return base64.b64encode(buffered.getvalue()).decode()

def send_message_with_retry(chat_session, message, max_retries=5):
    """Handles retries with exponential backoff for rate limits."""
    for attempt in range(max_retries):
        try:
            response = chat_session.send_message(message)
            return response
        except Exception as e:
            if "429" in str(e):  # Rate limit error
                wait_time = (2 ** attempt) + random.uniform(0, 2)
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded after 5 attempts")

@app.post("/chat")
async def multimodal_chatbot(request: ChatRequest):
    """Handles text and image inputs for the chatbot."""
    user_input = request.user_input
    image_input = request.image_input
    text_response = ""

    try:
        # Handle text input
        if user_input:
            chat_session = gemini_model.start_chat(history=[])
            response = send_message_with_retry(chat_session, user_input)
            text_response = response.text

        # Handle image input
        if image_input:
            try:
                # Decode base64 image
                image_bytes = base64.b64decode(image_input)
                image = Image.open(io.BytesIO(image_bytes))

                # Generate image caption
                image_caption_prompt = f"Describe this image: {image_to_base64(image)}"
                chat_session = gemini_model.start_chat(history=[])
                image_caption_response = send_message_with_retry(chat_session, image_caption_prompt)
                image_caption = image_caption_response.text

                text_response += f"\nImage Caption (Gemini): {image_caption}"

            except Exception as e:
                text_response += f"\nError processing image: {e}"

        return {"response": text_response.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {e}")

# Run server if executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
