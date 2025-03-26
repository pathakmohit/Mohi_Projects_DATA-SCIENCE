import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import datetime
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest
import string

# Download necessary NLTK resources
import nltk
nltk.download('punkt')
nltk.download('stopwords')

class SummarizerGUI:
    def __init__(self, master):
        self.master = master
        self.setup_gui()

    def setup_gui(self):
        self.master.title("Text Summarizer")
        self.master.geometry("500x600")
        self.master.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ''' Chat History Text Box '''
        self.chat_history = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=60, height=25, font=("Arial", 10)
        )
        self.chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.chat_history.config(state=tk.DISABLED)

        ''' Input and Button Frames '''
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        self.user_input = ttk.Entry(input_frame, width=50, font=("Arial", 10))
        self.user_input.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)
        self.user_input.bind("<Return>", lambda event: self.summarize_text())

        self.summarize_button = ttk.Button(
            input_frame, text="Summarize", command=self.summarize_text
        )
        self.summarize_button.pack(side=tk.RIGHT)

        ''' Button Frame for Clear and Save '''
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.clear_button = ttk.Button(
            button_frame, text="Clear Text", command=self.clear_text
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))

        self.save_button = ttk.Button(
            button_frame, text="Save Summary", command=self.save_summary
        )
        self.save_button.pack(side=tk.LEFT)

    def summarize_text(self):
        # Get the user's input text to summarize
        user_text = self.user_input.get()
        self.user_input.delete(0, tk.END)

        if user_text.strip():
            # Generate the summary using the extractive summarization function
            try:
                summary = extractive_summary(user_text, sentence_count=3)
                self.update_chat_history(f"Summary: {summary}")
            except Exception as e:
                self.update_chat_history(f"Error summarizing text: {e}")
        else:
            messagebox.showwarning("Input Error", "Please provide some text to summarize.")

    def update_chat_history(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)

    def clear_text(self):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state=tk.DISABLED)

    def save_summary(self):
        filename = (
            f"summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        with open(filename, "w") as f:
            f.write(self.chat_history.get(1.0, tk.END))
        messagebox.showinfo("Summary Saved", f"Summary has been saved to {filename}")

# Extractive Summarization Function
def extractive_summary(text, sentence_count=3):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    
    # Remove stopwords and punctuation
    words = [
        word for word in word_tokens
        if word not in stop_words and word not in string.punctuation
    ]
    
    # Calculate word frequency
    freq_dist = FreqDist(words)
    
    # Rank sentences by their significance
    sentences = sent_tokenize(text)
    sentence_scores = {
        sent: sum(freq_dist[word] for word in word_tokenize(sent.lower()) if word in freq_dist)
        for sent in sentences
    }
    
    # Get the top `sentence_count` sentences
    summary_sentences = nlargest(sentence_count, sentence_scores, key=sentence_scores.get)
    return ' '.join(summary_sentences)


if __name__ == "__main__":
    root = tk.Tk()
    SummarizerGUI(root)
    root.mainloop()
