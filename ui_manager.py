import eel
import tkinter as tk
from tkinter import filedialog
import multiprocessing

class UIManager:
    """Manage the UI interactions, especially with the directory selection."""

    def __init__(self):
        """Initialize the UIManager with a multiprocessing queue."""
        self.q = multiprocessing.Queue()

    def tkinter_file_dialog(self):
        """
        Open the Tkinter file dialog to select a directory.

        The selected directory is put into the multiprocessing queue.
        """
        root = tk.Tk()                 # Create a root Tkinter window
        root.withdraw()                # Hide the root window
        folder_selected = filedialog.askdirectory()  # Open directory selection dialog
        root.destroy()                # Close the root window
        self.q.put(folder_selected)   # Put selected directory in the queue

    @eel.expose
    def select_directory(self):
        """
        Expose the directory selection to Eel.

        Start the Tkinter file dialog in a separate process to avoid freezing the Eel interface.
        Return the selected directory or None if no directory was selected.
        """
        p = multiprocessing.Process(target=self.tkinter_file_dialog)  # Start tkinter in a separate process
        p.start()                    # Start the process
        p.join()                     # Wait for the process to complete
        result = self.q.get()        # Get the selected directory from the queue
        return result if result else None

# Create an instance of UIManager for Eel interactions
ui_manager = UIManager()

@eel.expose
def exposed_select_directory():
    """
    Expose the directory selection function to Eel.

    Returns the selected directory or None if no directory was selected.
    """
    return ui_manager.select_directory()
