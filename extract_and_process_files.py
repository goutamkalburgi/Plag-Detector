"""
Author: Goutamkumar Kalburgi
Date: 06/21/2023
Description:    This script automates file extraction, organization, and code comparison using various compression formats. 
                It extracts individual archives, flattens their contents, and moves them to relevant folders. 
                It then runs Moss, a plagiarism detection tool, to compare code files for similarity. 
                The output is saved to 'output.txt'. This script supports popular archive formats like ZIP, RAR, and 7Z, and handles files of different types such as text files, code files, and miscellaneous files. 
                It provides a convenient way to analyze and compare student code submissions.
"""
import os
import zipfile
import rarfile
import py7zr
import glob
import shutil
from pathlib import Path
import subprocess
import eel  # Import eel
import multiprocessing
import tkinter as tk
from tkinter import filedialog

# Initialize Eel with the 'web' folder
eel.init('web')

ERROR_FILE = "error.txt"
OUTPUT_FILE = "output.txt"
supported_archive_extensions = ['.zip', '.rar', '.7z']
programming_languages = {
    'C++': { 'extensions': ['.cpp', '.h'], 'moss': 'cc' },
    'Java': { 'extensions': ['.java'], 'moss': 'java' },
    'C#': { 'extensions': ['.cs'], 'moss': 'csharp' },
    'Python': { 'extensions': ['.py'], 'moss': 'python' },
    'Visual Basic': { 'extensions': ['.vb', '.vbs'], 'moss': 'vb' },
    'Javascript': { 'extensions': ['.js'], 'moss': 'javascript' },
    'TypeScript': { 'extensions': ['.ts'], 'moss': 'javascript' }  # TypeScript is not directly supported by MOSS, so we'll use JavaScript as its language code.
}
misc_file_extensions = ['.pdf', '.docx', '.txt', '.csv', '.xlsx', '.pptx', '.jpg', '.png', '.mp3', '.mp4', '.html', '.css']

# Declare global variables
user_in = None
results_folder = None
other_files = None
extracted_code_folders = None
archives_folder = None
misc_files_folder = None
unzipped_code_folder = None

# Initialize the global variables
def init(user_input):
    global user_in, results_folder, other_files, extracted_code_folders, archives_folder, misc_files_folder, unzipped_code_folder
    user_in = user_input

    results_folder = unique_file(os.path.join(user_in, 'results'))  # unique results directory
    os.makedirs(results_folder, exist_ok=True)

    other_files = os.path.join(results_folder, 'other_files')  # store in results directory
    os.makedirs(other_files, exist_ok=True)

    extracted_code_folders = os.path.join(results_folder, 'extracted_code_folders')  # store in results directory
    os.makedirs(extracted_code_folders, exist_ok=True)

    archives_folder = os.path.join(other_files, 'archives')
    os.makedirs(archives_folder, exist_ok=True)

    misc_files_folder = os.path.join(other_files, 'misc_files')
    os.makedirs(misc_files_folder, exist_ok=True)

    unzipped_code_folder = os.path.join(other_files, 'unzipped_code_files')
    os.makedirs(unzipped_code_folder, exist_ok=True)

def unique_file(file_path):
    original_file_name, ext = os.path.splitext(file_path)
    counter = 1
    file_path = original_file_name + ext

    while os.path.exists(file_path):
        name = f"{original_file_name}{counter}"
        file_path = f"{name}{ext}"
        counter += 1
    return file_path

def tkinter_file_dialog(q):
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    root.destroy()
    q.put(folder_selected)

@eel.expose
def select_directory():
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=tkinter_file_dialog, args=(q,))
    p.start()
    p.join()
    result = q.get()
    return result if result else None


# Get user input for programming language
# def get_programming_language():
#     print("Please choose a programming language:")
#     print("1. C++")
#     print("2. Java")
#     print("3. C#")
#     print("4. Python")
#     print("5. Visual Basic")
#     print("6. Javascript")
#     print("7. TypeScript")
#     choice = input("Enter your choice (1-7): ")
    
#     if choice == '1':
#         return programming_languages['C++']
#     elif choice == '2':
#         return programming_languages['Java']
#     elif choice == '3':
#         return programming_languages['C#']
#     elif choice == '4':
#         return programming_languages['Python']
#     elif choice == '5':
#         return programming_languages['Visual Basic']
#     elif choice == '6':
#         return programming_languages['Javascript']
#     elif choice == '7':
#         return programming_languages['TypeScript']
    

def extract_archive(file, target_folder):
    file_name, file_extension = os.path.splitext(file)
    error_file_path = os.path.join(results_folder, ERROR_FILE)

    try:
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
            print(f'Unsupported file format: {file_extension}')
            with open(error_file_path, "a") as error_file:
                error_file.write(f"Unsupported file format {file}: {file_extension}\n")
    except Exception as e:
        with open(error_file_path, "a") as error_file:
            error_file.write(f"Error processing file {file}: {str(e)}\n")

def flatten_dir(target_folder):
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            target_path = os.path.join(target_folder, file)
            if file_path != target_path:
                unique_target_path = unique_file(target_path)
                shutil.move(file_path, unique_target_path)

    # Remove empty subdirectories
    for root, dirs, files in os.walk(target_folder, topdown=False):
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except OSError:
                pass  # Directory not empty

def move_unsupported_files(target_folder, misc_files_folder, file_extensions):
    # Move non .cpp and .h files
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = Path(os.path.join(root, file))
            if file_path.suffix.lower() not in file_extensions:
                target_path = os.path.join(misc_files_folder, file)
                unique_target_path = unique_file(target_path)
                shutil.move(str(file_path), unique_target_path)

# def prompt_user():
#     print("What would you like to do?")
#     print("1. Extract submissions and individual files")
#     print("2. Run MOSS plagiarism check")
#     print("3. Both (Extract and Run MOSS)")
#     choice = input("Enter your choice (1, 2, or 3): ")
#     return choice

def extract_submissions(language_data):
    print("Extracting Sections Archives...")
    for file in Path('.').glob('*.*'):
        if file.suffix in supported_archive_extensions:
            extract_archive(str(file), other_files)
            
    print("Extracting all individual archives of sections and flattening the content...")
    for file in Path(other_files).glob('*.*'):
        if file.suffix in supported_archive_extensions:
            dir = os.path.join(extracted_code_folders, str(file.stem))
            try:
                os.makedirs(dir)
            except OSError:
                pass  # Directory already exists

            extract_archive(str(file), dir)
            flatten_dir(dir)
            move_unsupported_files(dir, misc_files_folder, language_data['extensions'])

            shutil.move(str(file), os.path.join(archives_folder, file.name))
        elif file.suffix.lower() in language_data['extensions']:
            prefix = file.stem.split('_', 1)[0]  # Extract the common prefix
            destination_folder = os.path.join(extracted_code_folders, prefix)
            os.makedirs(destination_folder, exist_ok=True)  # Create the destination folder if it doesn't exist
            shutil.move(str(file), os.path.join(destination_folder, file.name))
        elif file.suffix.lower() in misc_file_extensions:
            shutil.move(str(file), os.path.join(misc_files_folder, file.name))


def run_moss(language_data):
    print("Running MOSS...")
    moss_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moss.pl")  # get absolute path of moss.pl file
    moss_file = moss_file.replace(' ', '\\ ')
    moss_command = f"perl {moss_file} -l {language_data['moss']} -d " + " ".join(f"*/*{ext}" for ext in language_data['extensions'])
    result = subprocess.run(moss_command, shell=True, cwd=extracted_code_folders, capture_output=True, text=True)
    eel.update_result(result.stdout)  # Pass the stdout to JavaScript function
    print(result.stdout)
    # Define output and error file paths inside the 'results' folder
    output_file_path = os.path.join(results_folder, OUTPUT_FILE)
    error_file_path = os.path.join(results_folder, ERROR_FILE)

    # Write to output file
    with open(output_file_path, "w") as file:  
        file.write(result.stdout)
        
    # If there is an error, write to error file
    if result.returncode != 0:
        print("Error: " + result.stderr)
        with open(error_file_path, "w") as file:
            file.write(result.stderr)


# The inputs are now passed as function arguments instead of being read from the terminal
@eel.expose  # Expose this function to JavaScript
def main(input_user_in, language_choice, operation_choice):
    init(input_user_in)
    os.chdir(user_in)
    language_data = programming_languages[language_choice]
    choice = operation_choice
    if choice == '1' or choice == '3':
        extract_submissions(language_data)
    if choice == '2' or choice == '3':
        run_moss(language_data)

if __name__ == "__main__":
    window_size = (800, 720)
    eel.start('index.html', size=window_size)  # Name of the HTML file