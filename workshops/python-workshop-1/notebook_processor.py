import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import nbformat
import os

# Constants
APP_TITLE = "Notebook Processor"
APP_GEOMETRY = '650x300'
DROP_LABEL_TEXT = "Drop Here"
SUCCESS_TITLE = "Success"
ERROR_TITLE = "Error"
FILE_TYPE = ".ipynb"
MODIFIED_SUFFIX = "(cleaned)"

# Descriptive text
APP_DESCRIPTION = (
    "Drag and drop a Jupyter notebook onto the area below.\n\n"
    "The app will process the notebook by emptying code cells that do not contain:\n"
    "- Magic commands\n"
    "- Import statements\n"
    "- Commented-out pip/conda installs\n"
    "- Code cells following a markdown cell with the word 'example'\n\n"
    "Consecutive empty code cells will be collapsed into one.\n"
    "All outputs will also be cleared.\n\n"
    "The processed notebook will be saved in the same location as the original file "
    f"with {MODIFIED_SUFFIX} appended to its name."
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

def save_notebook(nb, original_path):
    """Save the processed notebook with a new name."""
    new_path = os.path.splitext(original_path)[0] + " " + MODIFIED_SUFFIX + FILE_TYPE
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
        """Handle the drop event and process the notebook."""
        if event.data:
            files = self.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f) and f.lower().endswith(FILE_TYPE):
                    try:
                        nb = nbformat.read(f, as_version=4)
                        nb = process_notebook_cells(nb)
                        new_path = save_notebook(nb, f)
                        messagebox.showinfo(SUCCESS_TITLE, f'Processed notebook saved as:\n{new_path}')
                    except Exception as e:
                        messagebox.showerror(ERROR_TITLE, f'An error occurred:\n{e}')
                else:
                    messagebox.showwarning(ERROR_TITLE, 'Please drop a Jupyter notebook file.')

if __name__ == "__main__":
    print('Starting app...')
    app = NotebookProcessorApp()
    app.mainloop()
