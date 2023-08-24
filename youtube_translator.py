import tkinter as tk
import customtkinter
from tkinter import scrolledtext
from googletrans import Translator
import pyperclip

class BatchTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Translator ( Afkar )")
        self.root.geometry("770x950")  # Set ukuran jendela
        self.root.configure(padx=0, pady=20)  # Padding atas dan bawah
      
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

        self.languages = {
            "en": "English",
            "nl": "Dutch",
            "de": "German",
            "ar": "Arabic",
            "it": "Italian",
            "ru": "Russian",
            "fr": "French",
            "ja": "Japanese",
            "es": "Spanish"
        }

        self.input_label = tk.Label(root, text="Enter Text")
        self.input_label.pack()

        self.input_text = customtkinter.CTkTextbox(root, wrap=tk.WORD, height=2, width=10)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=20)

        self.character_count_label = tk.Label(root, text="Characters: 0/100")
        self.character_count_label.pack()

        self.translate_button = customtkinter.CTkButton(root, text="Translate", width=80, fg_color="#2980b9", command=self.translate)
        self.translate_button.pack()

        self.input_text.bind("<KeyRelease>", self.update_character_count)
        

        self.output_texts = {}
        for lang_code, lang_name in self.languages.items():
            lang_label = customtkinter.CTkLabel(root, text=lang_name)
            lang_label.pack(anchor="w", padx=20)  # Mengatur posisi label ke kiri)

            lang_frame = customtkinter.CTkFrame(root)
            lang_frame.pack(fill=tk.BOTH, expand=True, padx=20)

            lang_text = customtkinter.CTkTextbox(lang_frame, wrap=tk.WORD, height=5, width=10)
            lang_text.pack(fill=tk.BOTH, expand=True)

            copy_button = customtkinter.CTkButton(lang_frame, text="Copy", width=50, command=lambda lang=lang_name: self.copy_text(lang))
            copy_button.pack(side=tk.RIGHT)  # Pindahkan tombol ke sebelah kanan frame

            self.output_texts[lang_name] = lang_text

    def update_character_count(self, event):
        input_text = self.input_text.get("1.0", "end-1c")
        character_count = len(input_text)
        
        self.character_count_label.config(text=f"Characters: {character_count}/100")
        
        if character_count > 100:
            self.input_label.config(text="Stop")
        else:
            self.input_label.config(text="Enter Text")

        if character_count >= 100:
            self.input_text.config(state="normal")
            self.input_text.delete("end-2c", "end-1c")  # Menghapus karakter terakhir jika lebih dari 100


    def translate(self):
        input_text = self.input_text.get("1.0", "end-1c")
        translations = self.translate_to_multiple_languages(input_text)

        for lang_name, translated_text in translations.items():
            self.output_texts[lang_name].delete("1.0", "end")
            self.output_texts[lang_name].insert("1.0", translated_text)

    def translate_to_multiple_languages(self, text):
        translations = {}
        translator = Translator()

        for lang_code, lang_name in self.languages.items():
            translated_text = translator.translate(text, dest=lang_code).text
            translations[lang_name] = translated_text

        return translations

    def copy_text(self, lang_name):
        translated_text = self.output_texts[lang_name].get("1.0", "end-1c")
        pyperclip.copy(translated_text)

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = BatchTranslatorApp(root)
    root.mainloop()