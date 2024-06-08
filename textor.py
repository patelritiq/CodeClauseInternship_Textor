# FILE: textor.py
# AUTHOR: Ritik Pratap Singh Patel
# COMPLETION DATE: 08 June 2024
# DESCRIPTION: "Textor": A basic text editor with spell checking and highlighting

import tkinter as tk
from tkinter import filedialog, messagebox

class SimpleTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("\'Textor\': Simple Text Editor")
        self.root.geometry("800x600")

        # Add Text Widget
        self.text_area = tk.Text(self.root, wrap='word')
        self.text_area.pack(expand=1, fill='both')
        self.text_area.tag_config("misspelled", foreground="red")

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add menu options
        self.menu_bar.add_command(label="New", command=self.new_file)
        self.menu_bar.add_command(label="Open", command=self.open_file)
        self.menu_bar.add_command(label="Save", command=self.save_file)
        self.menu_bar.add_command(label="Word Count", command=self.word_count)
        self.menu_bar.add_command(label="Exit", command=self.exit_editor)

        # Add status bar
        self.status_bar = tk.Label(self.root, text="Ready", anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

        self.file_path = None

        # Load a list of English words for spell checking
        try:
            with open("words.txt") as f:
                self.english_words = set(f.read().split())
        except FileNotFoundError:
            messagebox.showerror("Error", "words.txt file not found. Please ensure the file is in the same directory as this script.")
            self.root.destroy()

        # Bind text change event for highlighting
        self.text_area.bind("<KeyRelease>", self.highlight_misspellings)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.update_status("New file created")
        self.highlight_misspellings()  # Call to highlight on new file

    def open_file(self):
        self.file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.file_path:
            with open(self.file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.update_status(f"Opened {self.file_path}")
            self.highlight_misspellings()  # Call to highlight after opening

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.update_status(f"Saved {self.file_path}")

    def exit_editor(self):
        self.root.quit()

    def word_count(self):
        text_content = self.text_area.get(1.0, tk.END)
        words = len(text_content.split())
        self.update_status(f"Word count: {words}")

    def update_status(self, message):
        self.status_bar.config(text=message)

    def highlight_misspellings(self, event=None):
        self.text_area.tag_remove("misspelled", 1.0, tk.END)  # Remove previous highlighting

        text = self.text_area.get(1.0, tk.END)
        words = text.split()

        for word in words:
            # Remove any punctuation from the word
            cleaned_word = ''.join(char for char in word if char.isalnum())
            # Check if the cleaned word is not in the list of English words
            if cleaned_word.lower() not in self.english_words:
                start_idx = "1.0"
                while True:
                    start_idx = self.text_area.search(cleaned_word, start_idx, stopindex=tk.END)
                    if not start_idx:
                        break
                    end_idx = f"{start_idx}+{len(cleaned_word)}c"
                    self.text_area.tag_add("misspelled", start_idx, end_idx)
                    start_idx = end_idx

if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleTextEditor(root)
    root.mainloop()
