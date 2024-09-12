import tkinter as tk
from tkinter import filedialog, messagebox


def create_gui():
    root = tk.Tk()
    root.title("SRT File Loader")
    root.geometry("400x200")  # Adjust size as needed

    # Variables to store file paths and shift amount
    file_paths = []
    shift_amount = tk.StringVar()

    def select_files():
        nonlocal file_paths
        file_paths = filedialog.askopenfilenames(
            title="Select .srt Files",
            filetypes=[("Subtitle Files", "*.srt"), ("All Files", "*.*")]
        )

        if file_paths:
            # Clear previous widgets if any
            for widget in root.winfo_children():
                widget.destroy()

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
        # Store the shift amount entered by the user
        shift_value = shift_amount.get()
        if shift_value:
            try:
                shift_value = int(shift_value)
                # Print or use the shift amount as needed
                print(f"Shift amount (ms): {shift_value}")
                # Print or use the file paths as needed
                print(f"Selected files: {file_paths}")
            except ValueError:
                messagebox.showerror(
                    "Invalid Input", "Please enter a valid integer for the shift amount.")
        else:
            messagebox.showwarning("No Input", "Please enter a shift amount.")

    # Initial button to select files
    select_button = tk.Button(
        root, text="Select .srt files", command=select_files, width=20)
    select_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
