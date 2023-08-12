"""
configuration.py

This module contains static configurations for the file management system. It provides settings for various languages,
their extensions, supported archive formats, and other relevant configurations.
"""

# Dictionary containing supported programming languages and their associated metadata:
# - 'extensions' indicates the file extensions associated with the language.
# - 'moss' refers to the language identifier used by MOSS (a plagiarism detection system).
# New languages and their associated settings can be added as needed.
LANGUAGE_CONFIG = {
    'C++': {'extensions': ['.cpp', '.h'], 'moss': 'cc'},
    'Java': {'extensions': ['.java'], 'moss': 'java'},
    'C#': {'extensions': ['.cs'], 'moss': 'csharp'},
    'Python': {'extensions': ['.py'], 'moss': 'python'},
    'Visual Basic': {'extensions': ['.vb', '.vbs'], 'moss': 'vb'},
    'Javascript': {'extensions': ['.js'], 'moss': 'javascript'},
    'TypeScript': {'extensions': ['.ts'], 'moss': 'javascript'}
    # Further languages can be added here.
}

# List of miscellaneous file extensions. These are typically non-code file types 
# that may be found within the user's provided directories but need separate handling.
MISC_FILE_EXTENSIONS = ['.pdf', '.docx', '.txt', '.csv', '.xlsx', '.pptx', '.jpg', '.png', '.mp3', '.mp4', '.html', '.css']

# List of supported archive formats that the system can extract.
SUPPORTED_ARCHIVE_EXTENSIONS = ['.zip', '.rar', '.7z']

# Additional configuration data can be added to this module as needed.
