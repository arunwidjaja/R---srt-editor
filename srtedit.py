import tkinter as tk
from tkinter import filedialog, messagebox
import re
from datetime import datetime, timedelta
import os


def create_gui():

    # Initialize GUI elements
    # Window
    root = tk.Tk()
    root.title("SRT File Loader")
    root.geometry("400x300")  # Adjust size as needed

    # Initialize variables to store file paths, file contents, and shift amount
    file_contents = {}  # dictionary containing file path and contents of file
    shift_value = 0
    shift_amount = tk.StringVar()

    # Button for file Selection
    def display_get_files():
        select_button = tk.Button(
            root, text="Select .srt files", command=get_files, width=20)
        select_button.pack(pady=20)

    # Field for submitting shift amount
    def display_get_shift_amount():
        submit_button = tk.Button(
            root, text="Submit Shift Amount", command=get_shift_amount, width=20)
        shift_amount_entry = tk.Entry(
            root, textvariable=shift_amount, width=20)
        shift_amount_label = tk.Label(
            root, text="Shift amount (ms):", font=("Arial", 12))
        shift_amount_label.pack(pady=10)
        shift_amount_entry.pack(pady=5)
        submit_button.pack(pady=10)

    # Reads files selected by user
    # Displays shift amount text field afterwards
    def get_files():
        nonlocal file_contents
        file_paths = filedialog.askopenfilenames(
            title="Select .srt Files",
            filetypes=[("Subtitle Files", "*.srt"), ("All Files", "*.*")]
        )
        if file_paths:
            # Clear previous widgets if any
            for widget in root.winfo_children():
                widget.destroy()

            # Read and store file contents
            file_contents.clear()  # Clear existing file contents
            for file_path in file_paths:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        file_contents[file_path] = content
                except Exception as e:
                    messagebox.showerror("Error", f"Error reading file {
                                         file_path}: {str(e)}")
            # Display shift amount GUI
            display_get_shift_amount()
        else:
            messagebox.showwarning("No Files Selected",
                                   "Please select at least one .srt file.")

    # Reads shift amount entered by user
    # Updates timestamps upon completion
    def get_shift_amount():
        nonlocal shift_value
        shift_value = shift_amount.get()
        if shift_value:
            try:
                # Convert shift amount to integer (milliseconds) and update timestamps
                shift_value = int(shift_value)
                update_timestamps(file_contents, shift_value)
            except ValueError:
                messagebox.showerror(
                    "Invalid Input", "Please enter a valid integer for the shift amount.")
        else:
            messagebox.showwarning("No Input", "Please enter a shift amount.")

    # Updates timestamps and writes new file to the same directory as the source file
    def update_timestamps(file_contents, shift_value):
        # Define the timestamp pattern (ISO 8601 format)
        pattern = r'(\d{2}:\d{2}:\d{2},\d{3})'

        # parses a timestamp and shifts it
        def shift_time(match):
            iso_time = match.group(0)
            try:
                dt = datetime.strptime(iso_time, '%H:%M:%S,%f')
                # Create a timedelta for the shift amount
                delta = timedelta(milliseconds=shift_value)
                new_dt = dt + delta
                # Convert back to ISO time format
                new_iso_time = new_dt.strftime('%H:%M:%S,%f')[
                    :-3]  # Format with milliseconds
                return new_iso_time
            except ValueError as e:
                print(f"Error processing time '{iso_time}': {e}")
                return iso_time

        for file_path, content in file_contents.items():
            updated_content = re.sub(pattern, shift_time, content)
            print(f"\n--- Updated content of {file_path} ---")

            # Writing files
            base, ext = os.path.splitext(file_path)
            new_file_path = f"{base}.shift{ext}"
            write_updated_srt(new_file_path, updated_content)

    # Writes to disk
    def write_updated_srt(file_path, content):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated file saved as: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error writing file {
                file_path}: {str(e)}")

    display_get_files()

    root.mainloop()


if __name__ == "__main__":
    create_gui()
