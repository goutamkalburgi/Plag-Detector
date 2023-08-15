import os
import zipfile
import rarfile
import py7zr
import shutil
from pathlib import Path
import configuration
import eel

class FileManager:
    """Handles file management tasks such as archive extraction, directory flattening, and file organization."""

    def __init__(self, user_input):
        """Initialize FileManager with user's input and sets up required directories."""

        # Define constant file names for errors and output
        self.error_file = "error.txt"
        self.output_file = "output.txt"

        # User's provided input directory
        self.user_in = user_input

        # Define and create a unique 'results' directory
        self.results_folder = self.unique_file(os.path.join(self.user_in, 'results'))  # unique results directory
        os.makedirs(self.results_folder, exist_ok=True)

        # Define and create directory for miscellaneous files under 'results'
        self.other_files = os.path.join(self.results_folder, 'other_files')  # store in results directory
        os.makedirs(self.other_files, exist_ok=True)

        # Define and create directory for extracted code under 'results'
        self.extracted_code_folders = os.path.join(self.results_folder, 'extracted_code_folders')  # store in results directory
        os.makedirs(self.extracted_code_folders, exist_ok=True)

        # Additional directories for archives, miscellaneous files, and unzipped code files
        self.archives_folder = os.path.join(self.other_files, 'archives')
        os.makedirs(self.archives_folder, exist_ok=True)

        self.misc_files_folder = os.path.join(self.other_files, 'misc_files')
        os.makedirs(self.misc_files_folder, exist_ok=True)

        self.unzipped_code_folder = os.path.join(self.other_files, 'unzipped_code_files')
        os.makedirs(self.unzipped_code_folder, exist_ok=True)

    
    def get_instance_variables(self):
        """Return instance variables for debugging or logging purposes."""
        return vars(self)
    

    def unique_file(self, file_path):
        """Return a unique file path by appending a number if the file already exists."""
        original_file_name, ext = os.path.splitext(file_path)
        counter = 1
        file_path = original_file_name + ext
        while os.path.exists(file_path):
            name = f"{original_file_name}{counter}"
            file_path = f"{name}{ext}"
            counter += 1
        return file_path
    
    def extract_archive(self, file, target_folder):
        """Extracts archive files (zip, rar, 7z) to the target folder."""
        file_name, file_extension = os.path.splitext(file)
        error_file_path = os.path.join(self.results_folder, self.error_file)

        try:
            # Extraction based on file type
            if file_extension == ".zip":
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(target_folder)
            elif file_extension == ".rar":
                with rarfile.RarFile(file, 'r') as rar_ref:
                    rar_ref.extractall(target_folder)
            elif file_extension == ".7z":
                with py7zr.SevenZipFile(file, mode='r') as z:
                    z.extractall(target_folder)
            else:
                # Log unsupported file formats
                eel.appendToLog(f"Unsupported file format {file}: {file_extension}", False)
                with open(error_file_path, "a") as file:
                    file.write(f"Unsupported file format {file}: {file_extension}\n")
        except Exception as e:
            # Log exceptions that occur during extraction
            eel.appendToLog(f"Error processing file {file}: {str(e)}", False)
            with open(error_file_path, "a") as file:
                file.write(f"Error processing file {file}: {str(e)}\n")



    def flatten_dir(self, target_folder):
        """Flatten the directory structure by moving all files to the root of the target folder and removing empty directories."""
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                file_path = os.path.join(root, file)
                target_path = os.path.join(target_folder, file)
                if file_path != target_path:
                    unique_target_path = self.unique_file(target_path)
                    shutil.move(file_path, unique_target_path)
        for root, dirs, files in os.walk(target_folder, topdown=False):
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except OSError:
                    pass  # Directory not empty; safe to ignore

    
    def move_unsupported_files(self, target_folder, file_extensions):
        """Move files with unsupported extensions to the miscellaneous files folder."""
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                file_path = Path(os.path.join(root, file))
                if file_path.suffix.lower() not in file_extensions:
                    target_path = os.path.join(self.misc_files_folder, file)
                    unique_target_path = self.unique_file(target_path)
                    shutil.move(str(file_path), unique_target_path)


    def extract_submissions(self, language_data, optional_callback=None):
        """Extract submission archives, then extract individual archives, flatten the structure, and organize files."""
        section_archive_count = 0
        individual_archive_count = 0

        for file in Path('.').glob('*.*'):
            if file.suffix in configuration.SUPPORTED_ARCHIVE_EXTENSIONS:
                self.extract_archive(str(file), self.other_files)
                section_archive_count += 1

        # Check for no section archives
        if section_archive_count == 0:
            eel.appendToLog("No sections archives found.", False)
            eel.completeProgressBar()
            return section_archive_count, individual_archive_count
        
        eel.appendToLog("Extracting Sections Archives...", True)

        eel.appendToLog("Extracting all individual archives of sections and flattening the content...", True)
        for file in Path(self.other_files).glob('*.*'):
            if file.suffix in configuration.SUPPORTED_ARCHIVE_EXTENSIONS:
                individual_archive_count += 1
                dir = os.path.join(self.extracted_code_folders, str(file.stem))
                try:
                    os.makedirs(dir)
                except OSError:
                    pass  # Directory already exists
                self.extract_archive(str(file), dir)
                self.flatten_dir(dir)
                self.move_unsupported_files(dir, language_data['extensions'])
                shutil.move(str(file), os.path.join(self.archives_folder, file.name))
            elif file.suffix.lower() in language_data['extensions']:
                prefix = file.stem.split('_', 1)[0]  # Extract the common prefix
                destination_folder = os.path.join(self.extracted_code_folders, prefix)
                os.makedirs(destination_folder, exist_ok=True)  # Create the destination folder if it doesn't exist
                shutil.move(str(file), os.path.join(destination_folder, file.name))
            elif file.suffix.lower() in configuration.MISC_FILE_EXTENSIONS:
                shutil.move(str(file), os.path.join(self.misc_files_folder, file.name))

        # Check for no individual archives
        if individual_archive_count == 0 or individual_archive_count == 1:
            eel.appendToLog("Found zero or only one individual archive inside section archives.", False)
            eel.completeProgressBar()
        eel.appendToLog("Extraction and flattening of content completed. Please check the 'extracted_code_folders' directory within the '" + self.results_folder + "' folder for the obtained results.", True)
        
        if optional_callback:
            optional_callback()
        
        return section_archive_count, individual_archive_count
    
    def complete_progress_bar(self):
        eel.completeProgressBar()
