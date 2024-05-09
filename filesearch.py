import os
import threading
from customtkinter import *
import customtkinter as ctk
from tkinter import filedialog

# Initialize the main window
ctk.set_appearance_mode("System")  # Set the theme of the app
ctk.set_default_color_theme("blue")  # Set the color theme
root = ctk.CTk()  # Create the main window
root.title('File Searcher')
root.geometry("530x830")

# Function to find and display files
def find_files_by_extension(directory, file_extension, textbox):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if search_extension_checkbox.get() and file.endswith(file_extension):
                file_path = os.path.join(root, file)
            elif not search_extension_checkbox.get():
                file_path = os.path.join(root, file)
            else:
                continue

            # Determine how to display the file path based on display_name
            if display_name.get() == "Full":
                display_path = file_path
            elif display_name.get() == "Truncated":
                display_path = file_path.replace(directory, "")
            elif display_name.get() == "Bare":
                display_path = os.path.basename(file_path)
            else:
                display_path = file_path  # Default to full path if display_name is unrecognized

            # Use the thread-safe method to update the textbox
            textbox.insert('end', display_path + '\n')
            textbox.see('end')  # Auto-scroll to the end of the textbox

    textbox.insert('end', "\n\nEnd of File Search")


# Function to handle the search process
def start_search_thread():
    # Start the search in a new thread
    search_thread = threading.Thread(target=start_search)
    search_thread.start()

def start_search():
    if search_extension_checkbox.get() == 1:  # If checkbox is checked
        file_extension = "." + file_extension_entry.get()
    else:
        file_extension = 'txt'  # Default file extension
    directory = filedialog.askdirectory()
    if directory:  # If a directory is selected
        result_textbox.delete('1.0', 'end')  # Clear the textbox
        find_files_by_extension(directory, file_extension, result_textbox)

# UI Elements
titlebar = ctk.CTkLabel(root, text="File Searcher", font=('Futura',50))
titlebar.pack(pady=50)
result_textbox = ctk.CTkTextbox(root, height=350, width=400)

search_label = ctk.CTkLabel(root, text="Search for string (leave empty to list all files)", font=('Futura',15))
search_label.pack()

display_label = ctk.CTkLabel(root, text="Display Result As:", font=('Futura',15))
display_label.pack()

display_name = ctk.CTkComboBox(root, values=["Full", "Truncated", "Bare"])
display_name.pack(pady=10)

search_extension_checkbox = ctk.CTkCheckBox(root, text="Search by file extension (leave unchecked to search all files)")
search_extension_checkbox.pack()

file_extension_entry = ctk.CTkEntry(root, placeholder_text="txt")
file_extension_entry.pack(pady=15)
file_extension_entry.configure(state='disabled')  # Initially disabled

# Function to toggle the state of file_extension_entry
def toggle_entry():
    if search_extension_checkbox.get() == 1:
        file_extension_entry.configure(state='normal')
    else:
        file_extension_entry.configure(state='disabled')

search_extension_checkbox.configure(command=toggle_entry)

search_button = ctk.CTkButton(root, text="Search Folder", command=start_search_thread)
search_button.pack(pady=10)

result_textbox.pack(pady=20)

# Run the application
root.mainloop()
