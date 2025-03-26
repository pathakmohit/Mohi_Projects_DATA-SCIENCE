# Task 2 - Ultra-Fast Article Generator

This project is an **Ultra-Fast Article Generator** designed for rapid article creation using **large language models (LLMs)**. It leverages asynchronous processing and streaming for optimized responsiveness, with a **Streamlit-based interface**.

## Features
- **Model Selection**: Choose from Llama3, Mistral, or Falcon LLMs
- **Streaming Output**: Displays article content token-by-token for immediate feedback
- **Speed Optimization**: Prioritizes brevity and efficiency in responses
- **Performance Metrics**: Tracks and displays response time
- **Interactive UI**: Built with Streamlit for ease of use

## Project Structure
```
├── app.py            # Main Streamlit application
├── requirements.txt  # Project dependencies
├── README.md         # Documentation
```

## Installation
Ensure Python (>=3.7) is installed. Install dependencies using:
```sh
pip install -r requirements.txt
```

## Running the Application
### Start Streamlit App:
```sh
streamlit run app.py
```

## Data Source
The generator uses pre-trained LLMs (Llama3, Mistral, Falcon) via the **Ollama integration**. No external dataset is required.

## Usage
1. Select an **LLM** from the dropdown (e.g., Llama3, Mistral, Falcon).
2. Enter a **topic** in the text area (keep it short for faster results).
3. Click **Generate Article** to create a concise article.
4. View the streamed article and performance metrics (response time, model used).

## Future Enhancements
- Add support for additional LLMs
- Implement caching for frequently requested topics
- Enhance UI with real-time word count or progress bar

