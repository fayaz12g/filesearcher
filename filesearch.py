import os
import threading
from customtkinter import *
import customtkinter as ctk
from tkinter import filedialog
from CTkToolTip import *

# Initialize the main window
ctk.set_appearance_mode("system")  # Set the theme of the app
ctk.set_default_color_theme("dark-blue")  # Set the color theme
root = ctk.CTk()  # Create the main window
root.title('File Searcher')
root.geometry("530x980")

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
icon_path = os.path.join(script_directory, 'icon.ico')
root.iconbitmap(icon_path)

# Function to find and display files
def find_files_by_extension(directory, file_extension, textbox):
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Adjust the comparison based on case sensitivity
            if case_sensitive.get():
                match_string = search_entry.get()
                match_file = file
                match_extension = file_extension
            else:
                match_string = search_entry.get().lower()
                match_file = file.lower()
                match_extension = file_extension.lower()

            # Check if we need to search for a specific string in the file names
            if search_entry.get() and match_string not in match_file:
                continue

            # Check if we need to search for files with a specific extension
            if search_extension_checkbox.get() and not match_file.endswith(match_extension):
                continue

            # Construct the file path
            file_path = os.path.join(root, file)

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

    progressbar.stop()



# Function to handle the search process
def start_search_thread():
    result_textbox.configure(state='normal') 
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
        progressbar.start()
        result_textbox.insert('end', "Begining Search. You will get another message when the search \nfinishes\n\n")
        find_files_by_extension(directory, file_extension, result_textbox)
    result_textbox.configure(state='disabled') 

# UI Elements
titlebar = ctk.CTkLabel(root, text="File Searcher", font=('Futura',50))
titlebar.pack(pady=50)
result_textbox = ctk.CTkTextbox(root, height=350, width=400)
result_textbox.configure(state='disabled')  # Initially disabled

search_label = ctk.CTkLabel(root, text="Search String:", font=('Futura',15))
search_tooltip = CTkToolTip(search_label, message="(leave empty to list all files)")
search_label.pack()

search_entry = ctk.CTkEntry(root)
search_entry.pack(pady=5)

case_sensitive = ctk.CTkSwitch(root, text = "Case Sensitive")
case_sensitive.pack()

newlabel = ctk.CTkLabel(root, text="", font=('Futura',15))
newlabel.pack(pady=5)

display_label = ctk.CTkLabel(root, text="Display Result As:", font=('Futura',15))
display_tooltip = CTkToolTip(display_label, message=f'''Full = Full Path to the file
Truncated = Truncated path starting from the folder you choose
Bare = File name and extension only''')
display_label.pack()

display_name = ctk.CTkSegmentedButton(root, values=["Full", "Truncated", "Bare"], width=300, dynamic_resizing=True)
display_name.set("Truncated")
display_name.pack(pady=5)

newlabel = ctk.CTkLabel(root, text="", font=('Futura',15))
newlabel.pack(pady=5)

search_extension_checkbox = ctk.CTkCheckBox(root, text="Search by file extension:")
extension_tooltip = CTkToolTip(search_extension_checkbox, message="(leave unchecked to search all files)")
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

progressbar = ctk.CTkProgressBar(root, orientation="horizontal", progress_color="#800080", mode='indeterminate', indeterminate_speed=2, corner_radius=10, width=300)
progressbar.pack()

display_label2 = ctk.CTkLabel(root, text="Hover Over Each Option for More Informoation", font=('Futura',10))
display_label2.pack()


# Run the application
root.mainloop()
