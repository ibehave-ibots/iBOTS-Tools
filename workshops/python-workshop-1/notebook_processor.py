import shutil
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import nbformat
from nbformat.v4 import upgrade
import os

# Constants
APP_TITLE = "Notebook Processor"
APP_GEOMETRY = '650x400'
DROP_LABEL_TEXT = "Drag the folder or the notebook and drop here"
SUCCESS_TITLE = "Success"
ERROR_TITLE = "Error"
FILE_TYPE = ".ipynb"
MODIFIED_SUFFIX = "(cleaned)"

# Descriptive text
APP_DESCRIPTION = (
    "Drag and drop a Jupyter notebook or a directory onto the area below.\n\n"
    "If a notebook is dropped, the app will process the notebook by emptying code cells that do not contain:\n"
    "- Magic commands\n"
    "- Import statements\n"
    "- Commented-out pip/conda installs\n"
    "- Code cells following a markdown cell with the word 'example'\n\n"
    "If a directory is dropped, the app will recursively process all notebooks, "
    "copy '.py', '.png', and '.jpg' files,\n"
    f"and create a new directory with {MODIFIED_SUFFIX} appended to the name.\n"
    "Other directories without these file types will be skipped.\n\n"
    "Consecutive empty code cells will be collapsed into one.\n"
    "All outputs will also be cleared.\n\n"
    f"Processed files will be saved in a new {MODIFIED_SUFFIX} directory without changing individual notebook names."
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

def save_notebook(nb, original_path, add_suffix=True):
    """Save the processed notebook with a new name."""
    if add_suffix:
        base, ext = os.path.splitext(original_path)
        new_path = f"{base} {MODIFIED_SUFFIX}{ext}"
    else:
        new_path = original_path

    with open(new_path, 'w', encoding='utf-8') as file:
        nbformat.write(nb, file)
    return new_path


class NotebookProcessorApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)  # Adjusted for a wider initial width
        self.resizable(width=False, height=False)  # Prevents the window from being resizable
        self.create_widgets()
        self.create_widgets()

    def create_widgets(self):
        """Create and place widgets for the app."""
        description_label = tk.Label(self, text=APP_DESCRIPTION, justify=tk.LEFT, anchor="w", padx=10, pady=10)
        description_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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
                        new_path = save_notebook(nb, item)
                        messagebox.showinfo(SUCCESS_TITLE, f'Processed notebook saved as:\n{new_path}')
                    except Exception as e:
                        messagebox.showerror(ERROR_TITLE, f'An error occurred while processing the file:\n{e}')
                else:
                    messagebox.showwarning(ERROR_TITLE, 'Please drop a Jupyter notebook file or a directory containing notebooks.')

    def process_directory(self, directory_path, new_dir_path=None):
        """Process all notebooks in the given directory and its subdirectories. Copy certain file types."""
        if new_dir_path is None:
            parent_dir = os.path.abspath(os.path.join(directory_path, os.pardir))
            new_dir_name = os.path.basename(directory_path) + " " + MODIFIED_SUFFIX
            new_dir_path = os.path.join(parent_dir, new_dir_name)
            os.makedirs(new_dir_path, exist_ok=True)

        notebook_found = False
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                # Recursively process subdirectories
                sub_dir_path = os.path.join(new_dir_path, os.path.basename(item_path))
                os.makedirs(sub_dir_path, exist_ok=True)
                self.process_directory(item_path, sub_dir_path)
            elif item.lower().endswith(FILE_TYPE):
                # A notebook has been found
                notebook_found = True
                nb = nbformat.read(item_path, as_version=4)
                nb = process_notebook_cells(nb)
                new_file_path = os.path.join(new_dir_path, item)
                save_notebook(nb, new_file_path, add_suffix=False)
            elif item.lower().endswith(('.py', '.png', '.jpg')):
                # Copy .py, .png, and .jpg files to the cleaned directory
                shutil.copy2(item_path, new_dir_path)

        # If no notebook was found in the directory and no file was copied, remove the created directory
        if not notebook_found and not any(item.lower().endswith(('.py', '.png', '.jpg')) for item in os.listdir(directory_path)):
            os.rmdir(new_dir_path)
                
                
if __name__ == "__main__":
    print('Starting app...')
    app = NotebookProcessorApp()
    app.mainloop()
