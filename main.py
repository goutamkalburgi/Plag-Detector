import os
import eel
from file_manager import FileManager
from moss_interface import MossInterface
import ui_manager
import configuration


@eel.expose
def main(input_user_in, language_choice, operation_choice):
    """
    Main function exposed to Eel for frontend interactions.

    :param input_user_in: Input directory from the user.
    :param language_choice: The chosen language for processing.
    :param operation_choice: The chosen operation type (e.g., extraction, MOSS check, or both).
    """
    
    # Instantiate FileManager with user input directory
    file_manager = FileManager(input_user_in)

    # Instantiate MossInterface with required parameters from FileManager
    moss_interface = MossInterface(
        file_manager.extracted_code_folders,
        file_manager.results_folder,
        file_manager.output_file,
        file_manager.error_file
    )

    # Change current working directory to the provided user input directory
    os.chdir(file_manager.user_in)

    # Fetch language configurations based on user's language choice
    language_data = configuration.LANGUAGE_CONFIG[language_choice]

    # Determine operation(s) to perform based on user's choice
    choice = operation_choice
    if choice == '1' or choice == '3':
        file_manager.extract_submissions(language_data)
    if choice == '2' or choice == '3':
        moss_interface.run_moss(language_data)

if __name__ == "__main__":
    # Initialize the Eel web app with the 'web' folder
    eel.init('web')

    # Define the default window size for the app
    window_size = (800, 720)

    # Start the Eel web app with the main HTML file
    eel.start('index.html', size=window_size)


