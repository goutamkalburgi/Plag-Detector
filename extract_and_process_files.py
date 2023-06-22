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

ERROR_FILE = "error.txt"
OUTPUT_FILE = "output.txt"
supported_archive_extensions = ['.zip', '.rar', '.7z']
cpp_file_extensions = ['.cpp', '.h']
misc_file_extensions = ['.pdf', '.docx', '.txt', '.csv', '.xlsx', '.pptx', '.jpg', '.png', '.mp3', '.mp4', '.html', '.css']

# Global directory variables
other_files = 'other_files'
os.makedirs(other_files, exist_ok=True)
extracted_code_folders = 'extracted_code_folders'
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

def extract_archive(file, target_folder):
    file_name, file_extension = os.path.splitext(file)
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
            with open(ERROR_FILE, "a") as error_file:
                error_file.write(f"Unsupported file format {file}: {file_extension}\n")
    except Exception as e:
        with open(ERROR_FILE, "a") as error_file:
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

def move_unsupported_files(target_folder, misc_files_folder):
    # Move non .cpp and .h files
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = Path(os.path.join(root, file))
            if file_path.suffix.lower() not in cpp_file_extensions:
                target_path = os.path.join(misc_files_folder, file)
                unique_target_path = unique_file(target_path)
                shutil.move(str(file_path), unique_target_path)

def prompt_user():
    print("What would you like to do?")
    print("1. Extract submissions and individual files")
    print("2. Run MOSS plagiarism check")
    print("3. Both (Extract and Run MOSS)")
    choice = input("Enter your choice (1, 2, or 3): ")
    return choice

def extract_submissions():
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
            move_unsupported_files(dir, misc_files_folder)

            shutil.move(str(file), os.path.join(archives_folder, file.name))
        elif file.suffix.lower() in cpp_file_extensions:
            prefix = file.stem.split('_', 1)[0]  # Extract the common prefix
            destination_folder = os.path.join(extracted_code_folders, prefix)
            os.makedirs(destination_folder, exist_ok=True)  # Create the destination folder if it doesn't exist
            shutil.move(str(file), os.path.join(destination_folder, file.name))
        elif file.suffix.lower() in misc_file_extensions:
            shutil.move(str(file), os.path.join(misc_files_folder, file.name))

def run_moss():
    os.chdir('extracted_code_folders')
    print("Running MOSS...")
    moss_command = "perl ../moss.pl -l cc -d */*.cpp */*.h"
    result = subprocess.run(moss_command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    with open("../" + OUTPUT_FILE, "w") as file:
        file.write(result.stdout)

def main():
    choice = prompt_user()
    if choice == '1' or choice == '3':
        extract_submissions()
    if choice == '2' or choice == '3':
        run_moss()

if __name__ == "__main__":
    main()



 