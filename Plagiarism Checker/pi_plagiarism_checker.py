import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfFileReader
import os
from tqdm import tqdm
from tkinter import ttk


def compare_text(text1, text2):
    """Compare two strings and return the percentage similarity"""
    words1 = set(text1.split())
    words2 = set(text2.split())
    similarity = len(words1 & words2) / len(words1 | words2) * 100
    return similarity


def check_plagiarism():
    """Check plagiarism between two selected PDF files"""
    # Open file dialogs to select PDF files
    file1 = filedialog.askopenfilename(
        title="Select PDF file 1", filetypes=[("PDF Files", "*.pdf")]
    )
    file2 = filedialog.askopenfilename(
        title="Select PDF file 2", filetypes=[("PDF Files", "*.pdf")]
    )

    if file1 and file2:
        # Read the text from the PDF files
        try:
            text1 = ""
            with open(file1, "rb") as f:
                reader = PdfFileReader(f)
                total_pages = reader.getNumPages()
                with tqdm(total=total_pages, desc="File 1") as pbar:
                    for i in range(total_pages):
                        pbar.update(1)
                        text1 += reader.getPage(i).extractText()

            text2 = ""
            with open(file2, "rb") as f:
                reader = PdfFileReader(f)
                total_pages = reader.getNumPages()
                with tqdm(total=total_pages, desc="File 2") as pbar:
                    for i in range(total_pages):
                        pbar.update(1)
                        text2 += reader.getPage(i).extractText()

            # Compare the text and show the result
            similarity = compare_text(text1, text2)
            result_label.config(text=f"Similarity: {similarity:.2f}%")

        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please select two PDF files to compare.")


def clear_result():
    """Clear the result label"""
    result_label.config(text="")


# Create the main window
root = tk.Tk()
root.title("Plagiarism Checker")
root.geometry("400x250")
root.resizable(False, False)

# Set ttk theme
style = ttk.Style()
style.theme_use("clam")

# Create a label to display the result
result_label = ttk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=25)

# Create a button to check plagiarism
check_button = ttk.Button(
    root, text="Check Plagiarism", command=check_plagiarism, width=20
)
check_button.pack(pady=10)

# Create a button to clear the result
clear_button = ttk.Button(
    root, text="Clear Result", command=clear_result, width=20
)
clear_button.pack(pady=10)

# Create a progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress.pack(pady=10)

root.mainloop()
