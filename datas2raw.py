import os
from tkinter import filedialog, Tk, Button, Label

# Function to read raw data from multiple files and combine them
def combine_raw_data(files, output_file):
    with open(output_file, 'wb') as outfile:
        for file in files:
            with open(file, 'rb') as infile:
                outfile.write(infile.read())

# Function to handle the file selection and combining data
def combine_files():
    files = filedialog.askopenfilenames(title="Select Files", filetypes=[("All Files", "*.*")])
    if files:
        output_file = filedialog.asksaveasfilename(defaultextension=".raw", filetypes=[("RAW files", "*.raw")])
        if output_file:
            combine_raw_data(files, output_file)
            status_label.config(text=f"Combined data saved: {output_file}")
        else:
            status_label.config(text="Save operation cancelled.")
    else:
        status_label.config(text="No files selected.")

# Setup the GUI
root = Tk()
root.title("Combine Raw Data")

select_button = Button(root, text="Select Files and Combine Data", command=combine_files)
select_button.pack(pady=20)

status_label = Label(root, text="")
status_label.pack(pady=10)

root.mainloop()
