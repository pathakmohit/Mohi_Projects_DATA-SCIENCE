# Multilingual Chatbot

This is a **Multilingual Chatbot** built using Python, NLTK, and Google Translate API. It supports English, Spanish, French, and German, detecting the user's language and responding appropriately. The chatbot is integrated with a GUI built using Tkinter.

## Features
- Supports multiple languages (English, Spanish, French, German)
- Automatic language detection
- Tokenization and lemmatization of user inputs
- Interactive GUI built with Tkinter
- Asynchronous translation for better performance

## Installation
### Prerequisites
Ensure you have Python installed (>=3.6). Then, install the required dependencies:

```sh
pip install -r requirements.txt
```

### Required Libraries
The chatbot requires the following Python libraries:
- `nltk`
- `langdetect`
- `googletrans==4.0.0-rc1`
- `tk`
- `asyncio`

## Usage
Run the chatbot with the following command:

```sh
python main.py
```

### How It Works
1. The chatbot detects the user's language.
2. It processes the input using NLP techniques (tokenization, lemmatization, POS tagging).
3. It finds an appropriate response from predefined responses in the detected language.
4. If a response is not found, a fallback message is given.
5. The chatbot displays the conversation in a Tkinter GUI.

## Example Interactions
#### English
```sh
User: Hello
Chatbot: Hi there! How can I assist you today?
```
#### Spanish
```sh
Usuario: Hola
Chatbot: ¡Hola! ¿En qué puedo ayudarte?
```

## Project Structure
```
├── main.py            # Main chatbot script
├── requirements.txt   # Dependencies
├── README.md          # Project documentation
```

## Future Enhancements
- Add support for more languages
- Improve chatbot responses with machine learning
- Enhance UI with more interactive elements



