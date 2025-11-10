
import os
import argparse
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
    except FileNotFoundError:
        return f"Error: File not found at {pdf_path}"
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF file and save it to a text file.")
    parser.add_argument("pdf_file", help="The path to the PDF file.")
    parser.add_argument("-o", "--output", help="The output directory to save the text file. Defaults to the current directory.")

    args = parser.parse_args()

    pdf_file = args.pdf_file
    output_dir = args.output if args.output else os.getcwd()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extracted_text = extract_text_from_pdf(pdf_file)

    if extracted_text.startswith("Error:") or extracted_text.startswith("An error occurred:"):
        print(extracted_text)
        return

    base_filename = os.path.splitext(os.path.basename(pdf_file))[0]
    output_filepath = os.path.join(output_dir, f"{base_filename}.txt")

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"Successfully extracted text from {pdf_file} to {output_filepath}")

if __name__ == "__main__":
    main()
