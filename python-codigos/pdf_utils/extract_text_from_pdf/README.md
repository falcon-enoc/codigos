# Extract Text from PDF

This script extracts all selectable text from a PDF file and saves it to a text file.

## Installation

1.  Clone the repository or download the files.
2.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script from the command line, providing the path to the PDF file as an argument.

### Basic Usage

```bash
python extract_text_from_pdf.py /path/to/your/file.pdf
```

This will save the extracted text to a file named `file.txt` in the same directory where the script is run.

### Specify Output Directory

You can use the `-o` or `--output` flag to specify a different directory to save the output file.

```bash
python extract_text_from_pdf.py /path/to/your/file.pdf -o /path/to/output/directory
```

If the directory does not exist, it will be created.

### Help

To see the help message with all available options, use the `-h` or `--help` flag.

```bash
python extract_text_from_pdf.py -h
```
