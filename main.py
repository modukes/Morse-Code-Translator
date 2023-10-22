from morse_code import morse_code_dict
from tkinter import *
from PIL import Image, ImageTk
import pyperclip

# ---------------------------- CONSTANTS ------------------------------- #
FONT = ("Roboto", 12, "normal")
OPTIONS = ['English', 'Arabic', 'Persian', 'Greek', 'Japanese', 'Chinese', 'Korean']


# ---------------------------- FUNCTIONS  ------------------------------- #

# -------- COPY MORSE TO CLIPBOARD -------- #
def morse_to_clipboard():
    """Copy the text in the Morse code field to the clipboard."""
    morse_text = morse_field.get("1.0", "end-1c")
    pyperclip.copy(morse_text)

    if len(morse_text) == 0:
        copy_message_label.config(text="Field Is Empty, Nothing to Copy!", fg='red')
    else:
        copy_message_label.config(text="Morse code copied!", fg='green')

    copied_message_clear()


# -------- COPY TEXT TO CLIPBOARD -------- #
def text_to_clipboard():
    """Copy the text in the text field to the clipboard."""
    entry_text = text_field.get("1.0", "end-1c")
    pyperclip.copy(entry_text)

    if len(entry_text) == 0:
        copy_message_label.config(text="Field Is Empty, Nothing to Copy!", fg='red')
    else:
        copy_message_label.config(text="Text copied!", fg='green')

    copied_message_clear()


# -------- TEXT TO MORSE CODE CONVERSION -------- #
def text_to_morse(event):
    """Convert the text in the text field to Morse code and display it in the Morse code field."""
    text = text_field.get("1.0", "end-1c")
    morse_code = text_to_morse_code(text)
    morse_field.delete("1.0", END)
    morse_field.insert("1.0", morse_code)


# -------- MORSE TO TEXT CONVERSION -------- #
def morse_to_text(event):
    """Convert the Morse code in the Morse code field to text and display it in the text field."""
    morse_code = morse_field.get("1.0", "end-1c")
    text = morse_code_to_text(morse_code)
    text_field.delete("1.0", END)
    text_field.insert("1.0", text)


# -------- Convert Text to Morse Code -------- #
def text_to_morse_code(text):
    """Convert text to Morse code based on the selected language."""
    text = text_field.get("1.0", "end-1c").upper()
    chosen_language = selected_language.get()

    if chosen_language in morse_code_dict:
        morse_dict = morse_code_dict[chosen_language]
        morse_code = " ".join([morse_dict.get(letter, letter) for letter in text])
        return morse_code

    else:
        return "Language not supported"


# -------- Convert Morse Code To Text -------- #
def morse_code_to_text(morse_code):
    """Convert Morse code to text based on the selected language."""
    text = ""
    chosen_language = selected_language.get()

    if chosen_language in morse_code_dict:
        lang_dict = morse_code_dict[chosen_language]
        morse_code = morse_code.split()
        for code in morse_code:
            if code in lang_dict.values():
                text += list(lang_dict.keys())[list(lang_dict.values()).index(code)]
            else:
                text += code
    else:
        text += morse_code

    return text


# -------- Clear Notification After 3 SECS -------- #
def copied_message_clear():
    window.after(3000, clear_message)


def clear_message():
    copy_message_label.config(text="")

# -------- Update the Code Table -------- #
def update_morse_table(selected_language):
    # Clear the table
    for widget in morse_table.winfo_children():
        widget.grid_forget()

    if selected_language in morse_code_dict:
        morse_dict = morse_code_dict[selected_language]
        row = 0
        i = 0
        for letter, code in morse_dict.items():
            if letter != ' ':
                Label(morse_table, text=f'{letter}  {code}').grid(row=row, column=i, padx=10)
                i += 1
                if i == 10:
                    i = 0
                    row += 1


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Morse Code Translator")
window.config(padx=20, pady=20)

icon = Image.open('./assets/copy-clip.png')
icon.thumbnail((20, 20))
copy_icon = ImageTk.PhotoImage(icon)

copy_message_label = Label(window, text="", font=FONT)
copy_message_label.grid(row=2, column=0, columnspan=3)

text = Label(text='Text', font=FONT)
text.grid(row=0, column=0, padx=8, sticky="w")

text_field = Text(width=50, height=5)
text_field.grid(row=1, padx=10, pady=10, columnspan=1, sticky="we")
text_field.bind("<KeyRelease>", text_to_morse)

text_copy_button = Button(window, image=copy_icon, command=text_to_clipboard)
text_copy_button.image = copy_icon
text_copy_button.grid(row=0, padx=10, column=0, sticky="e")

morse_code_label = Label(text='Morse Code', font=FONT)
morse_code_label.grid(row=0, column=1, padx=8, sticky="w")

morse_field = Text(width=50, height=5)
morse_field.grid(row=1, padx=10, pady=10, column=1, columnspan=2, sticky="ew")
morse_field.bind("<KeyRelease>", morse_to_text)

morse_copy_button = Button(window, image=copy_icon, command=morse_to_clipboard)
morse_copy_button.image = copy_icon
morse_copy_button.grid(row=0, padx=10, column=2, sticky="e")

selected_language = StringVar(window)
selected_language.set(OPTIONS[0])

language_label = Label(text='Choose Your Language', font=FONT)
language_label.grid(row=2, column=2, padx=8, sticky="e")

language_menu = OptionMenu(window, selected_language, *OPTIONS, command=update_morse_table)
language_menu.grid(row=3, padx=10, column=2, sticky="e")

morse_table = Frame(window)
morse_table.grid(row=4, column=0, columnspan=2, sticky="w")

update_morse_table(selected_language.get())

window.mainloop()
