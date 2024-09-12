import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox

# Create the main application window


def create_gui():
    # Initialize the Tkinter root object
    root = tk.Tk()
    root.title("SRT Shift Tool")
    root.geometry("300x150")  # Set the window size

    # Function to handle the file selection
    def select_files():
        file_paths = filedialog.askopenfilenames(
            title="Select SRT Files",
            filetypes=[("Subtitle Files", "*.srt"), ("All Files", "*.*")]
        )
        if file_paths:
            # Display a message showing the selected files
            messagebox.showinfo("Selected Files", "\n".join(file_paths))
        else:
            messagebox.showwarning(
                "No File Selected", "Please select at least one file.")

    # Add a label to guide the user
    label = tk.Label(
        root, text="Select SRT files to shift time codes", font=("Arial", 12))
    label.pack(pady=20)

    # Add the button to prompt file selection
    button = tk.Button(root, text="Select Files", command(select_files), width=20)
    button.pack(pady=10)

    # Run the application
    root.mainloop()


# Launch the GUI
if __name__ == "__main__":
    create_gui()
