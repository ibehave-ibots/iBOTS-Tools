import shutil
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import nbformat
from nbformat.v4 import upgrade
import os

# Constants
APP_TITLE = "Notebook Processor"
APP_GEOMETRY = '650x500'
DROP_LABEL_TEXT = "Drag the folder or the notebook and drop here"
SUCCESS_TITLE = "Success"
ERROR_TITLE = "Error"
FILE_TYPE = ".ipynb"

# Descriptive text
APP_DESCRIPTION = (
    "Drag and drop a Jupyter notebook or a directory onto the area below.\n\n"
    "If a notebook is dropped, the app will process the notebook by emptying code cells that do not contain:\n"
    "- Magic commands\n"
    "- Import statements\n"
    "- Commented-out pip/conda installs\n"
    "- Code cells following a markdown cell with the word 'example'\n\n"
    "If a directory is dropped, the app will recursively process all notebooks within it.\n\n"
    "You can choose to add a suffix to the existing notebook names or to the processed notebooks. "
    "By default, the suffix '(Solutions)' will be added to the existing files.\n\n"
    "Consecutive empty code cells will be collapsed into one.\n"
    "All outputs will also be cleared.\n\n"
    "Choose whether to add the suffix to the existing files or to the new, processed files using the options provided."
)

def is_code_cell_empty(cell_source):
    # Ensure cell_source is a string
    if not isinstance(cell_source, str):
        return True  # If it's not a string, it's considered empty for safety

    for line in cell_source.split('\n'):
        stripped_line = line.strip()
        # Check for magic commands or import statements
        if stripped_line.startswith('%') or 'import ' in stripped_line:
            return False
        # Check for commented-out pip/conda installs with optional spaces
        if stripped_line.startswith('#') and any(magic in stripped_line for magic in ['%pip', '%conda']):
            return False
        if "https://uni-bonn.sciebo.de" in stripped_line:
            return False
    return True

def process_notebook_cells(nb):
    """Process the cells of the notebook to meet the criteria."""
    nb = upgrade(nb)
    keep_next_code_cell = False
    previous_cell_was_empty_code = False
    cells_to_remove = []

    for index, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown':
            # Check if the markdown cell contains the word "example"
            keep_next_code_cell = 'example' in cell.source.lower()
            previous_cell_was_empty_code = False  # Reset for markdown cells
        elif cell.cell_type == 'code':
            cell.outputs = []  # Clear outputs for all code cells
            if keep_next_code_cell or not is_code_cell_empty(cell.source):
                # Do not empty this code cell
                previous_cell_was_empty_code = False
            else:
                # Empty this code cell
                if previous_cell_was_empty_code:
                    # Mark the previous cell for removal if it was also empty
                    cells_to_remove.append(index - 1)
                cell.source = ''
                previous_cell_was_empty_code = True
            # Reset the flag as it applies only to the next code cell after the markdown
            keep_next_code_cell = False  

    # Remove marked cells in reverse to avoid index shifting
    for index in reversed(cells_to_remove):
        del nb.cells[index]

    return nb

def save_notebook(nb, original_path, suffix="(Solutions)", apply_to_existing=True):
    base, ext = os.path.splitext(original_path)
    new_name_for_original = f"{base} {suffix}{ext}"

    if apply_to_existing:
        if os.path.exists(new_name_for_original):
            # Ask the user if they want to overwrite the existing file
            response = messagebox.askyesno("Overwrite File", 
                                           f"The file {new_name_for_original} already exists. Do you want to overwrite it?")
            if response:  # If the user confirms, proceed with overwriting
                os.remove(new_name_for_original)
            else:  # If the user does not confirm, cancel the operation
                return None
        os.rename(original_path, new_name_for_original)
        new_path = original_path
    else:
        new_path = new_name_for_original
        if os.path.exists(new_path):
            # Ask the user if they want to overwrite the existing file
            response = messagebox.askyesno("Overwrite File", 
                                           f"The file {new_path} already exists. Do you want to overwrite it?")
            if not response:  # If the user does not confirm, cancel the operation
                return None
    
    with open(new_path, 'w', encoding='utf-8') as file:
        nbformat.write(nb, file)
    
    return new_path



# Complete code for the Notebook Processor app with suffix option

class NotebookProcessorApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)  # Adjusted for a wider initial width
        self.resizable(width=False, height=False)  # Prevents the window from being resizable
        
        # Set default suffix and location to add the suffix
        self.suffix = tk.StringVar(value="(Solutions)")
        self.suffix_location = tk.StringVar(value="existing")
        
        self.create_widgets()

    def create_widgets(self):
        """Create and place widgets for the app."""
        description_label = tk.Label(self, text=APP_DESCRIPTION, justify=tk.LEFT, anchor="w", padx=10, pady=10)
        description_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        suffix_label = tk.Label(self, text="Suffix for file names:", justify=tk.LEFT, anchor="w", padx=10)
        suffix_label.pack(side=tk.TOP, fill=tk.X)
        suffix_entry = tk.Entry(self, textvariable=self.suffix)
        suffix_entry.pack(side=tk.TOP, fill=tk.X, padx=10)

        radio_frame = tk.Frame(self)
        radio_label = tk.Label(radio_frame, text="Apply suffix to:", justify=tk.LEFT, anchor="w")
        radio_label.pack(side=tk.LEFT)
        radio_new = tk.Radiobutton(radio_frame, text="New file", variable=self.suffix_location, value="new")
        radio_new.pack(side=tk.LEFT)
        radio_existing = tk.Radiobutton(radio_frame, text="Existing file", variable=self.suffix_location, value="existing")
        radio_existing.pack(side=tk.LEFT)
        radio_frame.pack(side=tk.TOP, fill=tk.X, padx=10)

        drop_label = tk.Label(self, text=DROP_LABEL_TEXT, bg='lightgrey', width=50, height=10)
        drop_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        drop_label.drop_target_register(DND_FILES)
        drop_label.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        if event.data:
            items = self.tk.splitlist(event.data)
            for item in items:
                if os.path.isdir(item):
                    try:
                        self.process_directory(item)
                        messagebox.showinfo(SUCCESS_TITLE, f'All notebooks in "{item}" have been processed.')
                    except Exception as e:
                        messagebox.showerror(ERROR_TITLE, f'An error occurred while processing the directory:\n{e}')
                elif os.path.isfile(item) and item.lower().endswith(FILE_TYPE):
                    try:
                        nb = nbformat.read(item, as_version=4)
                        nb = process_notebook_cells(nb)
                        new_path = save_notebook(nb, item, suffix=self.suffix.get().strip(), apply_to_existing=self.suffix_location.get() == "existing")
                        messagebox.showinfo(SUCCESS_TITLE, f'Processed notebook saved as:\n{new_path}')
                    except Exception as e:
                        messagebox.showerror(ERROR_TITLE, f'An error occurred while processing the file:\n{e}')
                else:
                    messagebox.showwarning(ERROR_TITLE, 'Please drop a Jupyter notebook file or a directory containing notebooks.')

    def process_directory(self, directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                if ".ipynb_checkpoints" in item_path:
                    continue  # Skip the checkpoints directory
                # Recursively process subdirectories
                self.process_directory(item_path)
            elif item.lower().endswith(FILE_TYPE):
                try:
                    nb = nbformat.read(item_path, as_version=4)
                    nb = process_notebook_cells(nb)
                    # Determine whether to rename the original file
                    rename_original = self.suffix_location.get() == "existing"
                    save_notebook(nb, item_path, suffix=self.suffix.get().strip(), apply_to_existing=rename_original)
                except Exception as e:
                    messagebox.showerror(ERROR_TITLE, f'An error occurred while processing the file "{item_path}":\n{e}')

# Starting the app
if __name__ == "__main__":
    print('Starting app...')
    app = NotebookProcessorApp()
    app.mainloop()
