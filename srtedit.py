import tkinter as tk
from tkinter import filedialog, messagebox
import re
from datetime import datetime, timedelta


def create_gui():
    root = tk.Tk()
    root.title("SRT File Loader")
    root.geometry("400x300")  # Adjust size as needed

    # Initialize variables to store file paths, file contents, and shift amount
    file_paths = []
    file_contents = {}
    shift_amount = tk.StringVar()

    def select_files():
        nonlocal file_paths, file_contents
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

            # Display shift amount entry
            shift_amount_label = tk.Label(
                root, text="Shift amount (ms):", font=("Arial", 12))
            shift_amount_label.pack(pady=10)

            shift_amount_entry = tk.Entry(
                root, textvariable=shift_amount, width=20)
            shift_amount_entry.pack(pady=5)

            # Add a button to submit the shift amount
            submit_button = tk.Button(
                root, text="Submit Shift Amount", command=submit_shift_amount, width=20)
            submit_button.pack(pady=10)

        else:
            messagebox.showwarning("No Files Selected",
                                   "Please select at least one .srt file.")

    def submit_shift_amount():
        shift_value = shift_amount.get()
        if shift_value:
            try:
                # Convert shift amount to integer (milliseconds)
                shift_value = int(shift_value)
                for file_path, content in file_contents.items():
                    updated_content = update_timestamps(content, shift_value)
                    print(f"\n--- Updated Content of {file_path} ---")
                    print(updated_content)
            except ValueError:
                messagebox.showerror(
                    "Invalid Input", "Please enter a valid integer for the shift amount.")
        else:
            messagebox.showwarning("No Input", "Please enter a shift amount.")

    def update_timestamps(content, shift_value):
        # Define the timestamp pattern (ISO 8601 format)
        pattern = r'(\d{2}:\d{2}:\d{2},\d{3})'

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

        # Replace all timestamps in the content
        updated_content = re.sub(pattern, shift_time, content)
        return updated_content

    # Initial button to select files
    select_button = tk.Button(
        root, text="Select .srt files", command=select_files, width=20)
    select_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
