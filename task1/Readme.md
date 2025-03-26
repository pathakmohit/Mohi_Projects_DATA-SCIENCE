# Task 1 - Text Summarizer

This project is a **Text Summarizer** that performs extractive summarization on user-provided text. It uses **NLTK** for natural language processing and **Tkinter** for a graphical user interface.

## Features
- **Extractive Summarization**: Generates concise summaries based on word frequency
- **Interactive GUI**: Built with Tkinter for text input and display
- **Clear Text**: Option to reset the chat history
- **Save Summary**: Saves the summarized text to a timestamped file
- **Simple Interface**: Lightweight and easy to use

## Project Structure
```
├── app.py            # Main Tkinter application
├── requirements.txt  # Project dependencies
├── README.md         # Documentation
```

## Installation
Ensure Python (>=3.7) is installed. Install dependencies using:
```sh
pip install -r requirements.txt
```

Download required NLTK resources (run once):
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Running the Application
### Start Tkinter App:
```sh
python app.py
```

## Data Source
The summarizer processes user-input text dynamically. No external dataset is required.

## Usage
1. Enter text in the **input field**.
2. Click **Summarize** or press **Enter** to generate a summary (default: 3 sentences).
3. View the summary in the chat history.
4. Use **Clear Text** to reset the display.
5. Click **Save Summary** to save the output to a `.txt` file.

## Future Enhancements
- Add adjustable summary length
- Implement abstractive summarization with LLMs
- Enhance GUI with themes or styling options

