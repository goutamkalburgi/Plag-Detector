import subprocess
import eel
import os

class MossInterface:
    """Interface for MOSS (Measure of Software Similarity) plagiarism detection tool."""

    def __init__(self, extracted_code_folders, results_folder, output_file, error_file):
        """
        Initialize the MossInterface with relevant directories and files.

        :param extracted_code_folders: Folder containing extracted code for checking.
        :param results_folder: Directory where result and error files are stored.
        :param output_file: Name of the file where MOSS results are written.
        :param error_file: Name of the file where MOSS errors are written.
        """
        self.extracted_code_folders = extracted_code_folders
        self.results_folder = results_folder
        self.output_file = output_file
        self.error_file = error_file

    def run_moss(self, language_data):
        """Run the MOSS tool using provided language_data.

        :param language_data: Dictionary with 'moss' for language specifier and 'extensions' as file extensions list.
        """
        eel.appendToLog("Running MOSS...", True)
        
        # Get the absolute path of the moss.pl script
        moss_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moss.pl")
        
        # Escape spaces in path for use in shell command
        moss_file = moss_file.replace(' ', '\\ ')

        print(self.extracted_code_folders)

        # Construct the MOSS command
        moss_command_posix = f"perl {moss_file} -l {language_data['moss']} -d " + " ".join(f"*/*{ext}" for ext in language_data['extensions'])
        moss_command_nt = f"perl \"{moss_file}\" -l {language_data['moss']} -d " + " ".join(f"/{ext}" for ext in language_data['extensions'])

        if os.name == "nt":
            # Check if bash is available in PATH
            bash_path = "bash"  # This assumes that bash (from either Git Bash, Cygwin, or WSL) is added to the PATH

            try:
                subprocess.run([bash_path, "--version"], capture_output=True, text=True)
            except FileNotFoundError:
                eel.appendToLog("Bash is not found in the system PATH. The software won't work on Windows without bash. "
                                "Install either <a href='https://gitforwindows.org/'>Git Bash</a>, "
                                "<a href='https://www.cygwin.com/'>Cygwin</a>, or enable "
                                "<a href='https://docs.microsoft.com/en-us/windows/wsl/'>WSL</a>. "
                                "Make sure to add it to the system PATH and verify by running 'bash --version' in a terminal.", False)
                return

            # If bash is in PATH, can directly call bash to run your moss command
            result = subprocess.run([bash_path, "-c", moss_command_nt], cwd=self.extracted_code_folders, capture_output=True, text=True)
        else:
            # Execute the MOSS command and capture the output
            result = subprocess.run(moss_command_posix, shell=True, cwd=self.extracted_code_folders, capture_output=True, text=True)
        
        # Define paths for output and error files inside the 'results' folder
        output_file_path = os.path.join(self.results_folder, self.output_file)
        error_file_path = os.path.join(self.results_folder, self.error_file)

        # If there was an error during the MOSS execution, write the error to error file
        if result.returncode != 0:
            eel.appendToLog("MOSS analysis encountered an unexpected error. Please review the error log below.<br>" + result.stderr, False)
            with open(error_file_path, "w") as file:
                file.write("MOSS analysis encountered an unexpected error. Please review the error log below.\n" + result.stderr)
        else:
            # Pass the stdout to JavaScript function
            lines = result.stdout.split('\n')
            lastLine = lines[-2]
            eel.appendToLog("MOSS analysis completed successfully! Review the results below.<br>'" + lastLine + "'", True)
            # Write MOSS result to output file
            with open(output_file_path, "w") as file:
                file.write("MOSS analysis completed successfully! Review the results below.\n" + result.stdout)
        eel.completeProgressBar()







