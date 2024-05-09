import os
from customtkinter import *
import customtkinter as ctk
from tkinter import filedialog

# Initialize the main window
ctk.set_appearance_mode("System")  # Set the theme of the app
ctk.set_default_color_theme("blue")  # Set the color theme
root = ctk.CTk()  # Create the main window
root.title('File Searcher')
root.geometry("500x720")

# Function to find and display files
def find_files_by_extension(directory, file_extension, textbox):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                textbox.insert('end', os.path.join(root, file) + '\n')

# Function to handle the search process
def start_search():
    if search_extension_checkbox.get() == 1:  # If checkbox is checked
        file_extension = file_extension_entry.get()
    else:
        file_extension = '.txt'  # Default file extension
    directory = filedialog.askdirectory()
    if directory:  # If a directory is selected
        result_textbox.delete('1.0', 'end')  # Clear the textbox
        find_files_by_extension(directory, file_extension, result_textbox)

# UI Elements
result_textbox = ctk.CTkTextbox(root, height=350, width=400)

search_extension_checkbox = ctk.CTkCheckBox(root, text="Search file extension")
search_extension_checkbox.pack()

file_extension_entry = ctk.CTkEntry(root, placeholder_text=".txt")
file_extension_entry.pack()
file_extension_entry.configure(state = 'disabled')  # Initially disabled

# Function to toggle the state of file_extension_entry
def toggle_entry():
    if search_extension_checkbox.get() == 1:
        file_extension_entry.configure(state = 'normal')
    else:
        file_extension_entry.configure(state = 'disabled')

search_extension_checkbox.configure(command=toggle_entry)

search_button = ctk.CTkButton(root, text="Search", command=start_search)
search_button.pack(pady=10)

result_textbox.pack(pady=20)

# Run the application
root.mainloop()
