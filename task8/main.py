import nltk
import random
import asyncio
from langdetect import detect
from googletrans import Translator
import tkinter as tk
from tkinter import Scrollbar, Text
from nltk.chat.util import Chat, reflections
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
nltk.download('averaged_perceptron_tagger_eng')

# Download required NLTK datasets
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")

# Initialize components
translator = Translator()
lemmatizer = WordNetLemmatizer()

# Define culturally appropriate responses for multiple languages
chat_pairs = {
    "en": [
        (r"hello|hi|hey", ["Hello!", "Hi there!", "Hey! How can I assist you today?"]),
        (r"how are you", ["I'm doing great as a bot!", "Fine, thanks for asking!"]),
        (r"what is your name", ["I'm your friendly ChatBot!", "Call me ChatBot."]),
        (r"who created you", ["A Python developer brought me to life with NLTK!"]),
        (r"bye|goodbye", ["Take care!", "See you soon!"]),
        (r"how can you help me", ["I can chat in multiple languages and answer basic questions."]),
        (r"thank you|thanks", ["You're welcome!", "My pleasure!"])
    ],
    "es": [
        (r"hola|saludos", ["¡Hola!", "¡Saludos! ¿En qué puedo ayudarte?"]),
        (r"cómo estás", ["¡Estoy bien como bot!", "¡Gracias, estoy genial!"]),
        (r"cuál es tu nombre", ["¡Soy tu ChatBot amistoso!", "¡Llámame ChatBot!"]),
        (r"quién te creó", ["¡Un desarrollador de Python me dio vida con NLTK!"]),
        (r"adiós|hasta luego", ["¡Cuídate!", "¡Hasta pronto!"]),
        (r"cómo puedes ayudarme", ["Puedo charlar en varios idiomas y responder preguntas básicas."]),
        (r"gracias", ["¡De nada!", "¡Con gusto!"])
    ],
    "fr": [
        (r"bonjour|salut", ["Bonjour!", "Salut! Comment puis-je vous aider?"]),
        (r"comment vas-tu", ["Je vais bien en tant que bot!", "Merci, je suis super!"]),
        (r"quel est ton nom", ["Je suis votre ChatBot amical!", "Appelez-moi ChatBot."]),
        (r"qui t'a créé", ["Un développeur Python m'a donné vie avec NLTK!"]),
        (r"au revoir|à bientôt", ["Prenez soin de vous!", "À bientôt!"]),
        (r"comment peux-tu m'aider", ["Je peux discuter dans plusieurs langues et répondre à des questions simples."]),
        (r"merci", ["De rien!", "Avec plaisir!"])
    ],
    "de": [
        (r"hallo|hi", ["Hallo!", "Hi! Wie kann ich dir helfen?"]),
        (r"wie geht es dir", ["Mir geht's gut als Bot!", "Danke, ich bin super!"]),
        (r"wie heißt du", ["Ich bin dein freundlicher ChatBot!", "Nenn mich ChatBot."]),
        (r"wer hat dich erschaffen", ["Ein Python-Entwickler hat mich mit NLTK zum Leben erweckt!"]),
        (r"tschüss|auf wiedersehen", ["Pass auf dich auf!", "Bis bald!"]),
        (r"wie kannst du mir helfen", ["Ich kann in mehreren Sprachen chatten und einfache Fragen beantworten."]),
        (r"danke", ["Gern geschehen!", "Bitte schön!"])
    ]
}

# Create chatbots for each language
chatbots = {lang: Chat(pairs, reflections) for lang, pairs in chat_pairs.items()}

def get_wordnet_pos(word):
    """Map NLTK POS tag to WordNet POS tag."""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def detect_language(text):
    """Detect the language of the input text."""
    try:
        lang = detect(text)
        return lang if lang in chat_pairs else "en"  # Fallback to English if not supported
    except Exception:
        return "en"

async def translate_text(text, target_lang):
    """Translate text to the target language asynchronously."""
    try:
        loop = asyncio.get_event_loop()
        translation = await loop.run_in_executor(None, lambda: translator.translate(text, dest=target_lang))
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

async def preprocess_input(user_input, user_lang):
    """Preprocess input with tokenization and lemmatization in the original language."""
    tokens = word_tokenize(user_input.lower())
    lemmatized = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]
    return " ".join(lemmatized)

async def get_chatbot_response(user_input):
    """Get response in the user's detected language."""
    user_lang = detect_language(user_input)
    processed_input = await preprocess_input(user_input, user_lang)
    
    # Use the chatbot for the detected language directly
    bot_response = chatbots[user_lang].respond(processed_input)
    
    if not bot_response:
        # Language-specific fallback responses
        fallbacks = {
            "en": "Sorry, I didn't understand. Could you rephrase?",
            "es": "Lo siento, no entendí. ¿Podrías reformularlo?",
            "fr": "Désolé, je n'ai pas compris. Pouvez-vous reformuler?",
            "de": "Entschuldigung, das habe ich nicht verstanden. Könntest du es umformulieren?"
        }
        bot_response = fallbacks.get(user_lang, fallbacks["en"])
    
    return bot_response, user_lang

def send_message():
    """Handle user input and chatbot response in the GUI."""
    user_input = entry_field.get().strip()
    if not user_input:
        return
    if user_input.lower() in ["exit", "quit"]:
        root.quit()
        return
    
    loop = asyncio.get_event_loop()
    chatbot_response, lang = loop.run_until_complete(get_chatbot_response(user_input))
    
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"You ({lang.upper()}): {user_input}\n", "user")
    chat_window.insert(tk.END, f"Chatbot ({lang.upper()}): {chatbot_response}\n\n", "bot")
    chat_window.config(state=tk.DISABLED)
    chat_window.see(tk.END)
    
    entry_field.delete(0, tk.END)

# Create GUI Window
root = tk.Tk()
root.title("Multilingual Chatbot")
root.geometry("500x600")
root.resizable(False, False)

# Create chat display area
chat_window = Text(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = Scrollbar(chat_window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_window.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_window.yview)

# Entry field
entry_field = tk.Entry(root, font=("Arial", 14))
entry_field.pack(padx=10, pady=10, fill=tk.X)
entry_field.bind("<Return>", lambda event: send_message())

# Send button
send_button = tk.Button(root, text="Send", font=("Arial", 14), command=send_message)
send_button.pack(padx=10, pady=10)

# Styling for chat messages
chat_window.tag_config("user", foreground="blue")
chat_window.tag_config("bot", foreground="green")

# Initial welcome message in multiple languages
chat_window.config(state=tk.NORMAL)
chat_window.insert(tk.END, "Welcome! Willkommen! Bienvenue! ¡Bienvenido!\n", "bot")
chat_window.insert(tk.END, "I respond in your language: EN, DE, FR, ES supported.\n\n", "bot")
chat_window.config(state=tk.DISABLED)

# Run the chatbot GUI
root.mainloop()