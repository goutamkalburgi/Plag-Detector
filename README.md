# Projects Plagiarism Detector using MOSS Integration
## A User Interface for MOSS Plagiarism Detection System. Plagiarism Detection in Project Submissions Through Seamless MOSS Integration.

[MOSS](https://theory.stanford.edu/~aiken/moss/), or Measure Of Software Similarity, is an automated system developed to determine the similarity of programs. Primarily, its core use-case is to detect potential plagiarism in programming courses. This repository provides a user-friendly interface for MOSS to make the process more accessible.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
- [Usage](#usage)
- [About MOSS](#about-moss)
- [Non-commercial Statement](#non-commercial-statement)
- [About the Developer](#about-the-developer)
- [License](#license)

## Features

- Extracts section submissions downloaded from Canvas (or other LMS) in ZIP format.
- Extracts all individual archives of sections, organizes individual student submissions and filters out relevant programming files based on the user's choice of programming language.
- Integrates with the MOSS system and displays results within the interface.
- Provides flexibility in terms of just extracting files or running the MOSS check.

## Getting Started

### Prerequisites

- Python 3.x
- pip3 (Python Package Installer)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Projects-Plagiarism-Detector-using-MOSS-Integration.git
```

2. Navigate into the project directory:

```bash
cd Projects-Plagiarism-Detector-using-MOSS-Integration
```

3. Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

4. Run the application:

```bash
pip3 main.py
```

## Usage

1. Upon launching, you'll be prompted to **enter the directory** containing section submissions archives. This directory will also be used to store the results.
2. **Specify the programming language** used in the student assignments from the available options.
3. Choose your preferred operation:
   - Extract Submissions and Run MOSS. (This action first extracts section submissions, followed by individual student archives. Next, it organizes relevant programming files and runs MOSS for similarity analysis.)
   - Extract Submissions and Organize Relevant Files. (This action first extracts section submissions and individual student archives. Then, it organizes the relevant programming files without running MOSS.)

After successful execution, a `results` folder will appear in your chosen directory with the following structure:

- `extracted_code_folders`: Directories for each student with relevant programming files based on your language selection.
- `other_files`: Contains `misc_files` (miscellaneous files) and `unzipped_code_files`.
- `archives`: Stores individual student submission archives for reference.

## About MOSS

MOSS is an integral tool in academic settings, primarily designed for detecting similarities in student code submissions. It's essential to understand that while MOSS pinpoints similarities, it doesn't directly label them as plagiarized. Thus, manual inspection of the highlighted sections is crucial.

**Key Points**:
- MOSS generates results as HTML pages, which display pairs of programs with similar codes.
- Users can configure MOSS to ignore legitimate shared codes, reducing false positives.
- **Note**: Solely relying on MOSS scores without manual verification is discouraged. The scores indicate potential areas of concern, not definitive plagiarism.
- Results are stored on the MOSS server for up to 14 days. After which, they might be removed to free up space.

## Non-commercial Statement

**Non-commercial Statement:** This application was developed for educational and academic purposes and is not intended for commercial use. It leverages the open-source capabilities of MOSS, honoring its non-commercial nature.

## About the Developer

**Goutamkumar Kalburgi** is a seasoned Software Developer with a profound passion for building communities. Holding a Master's degree in Computer Science, he boasts years of experience in the software industry, adept in various programming languages, databases, tools, and platforms. With a keen interest in constant learning and adapting, Goutamkumar stands out as a proficient professional in the field. 

## License

This project is under the MIT License. See the [LICENSE.md](LICENSE.md) file for more details.

---

If you encounter issues or have suggestions for improvement, feel free to open an issue or a pull request. If you find this project useful, please consider giving it a star ⭐.
