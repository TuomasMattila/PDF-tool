"""
Utility for adding bookmarks to pdf files.
Author: Tuomas Mattila

The script copies every page from input pdf to output pdf,
reads first line from each page and adds a bookmark with that text,
adds the input file's metadata to the output and saves the pdf.
The new pdf with the bookmarks replaces the old pdf.
"""

import pypdf
import sys


def get_pdf_reader(filename: str) -> pypdf.PdfReader | bool:
    """
    Attempts creating a `PdfReader` object from a PDF file path
    defined by `filename`.
    
    Returns a `PdfReader` if successful, `False` otherwise.
    """
    reader = False
    try:
        reader = pypdf.PdfReader(filename)
    except:
        try:
            reader = pypdf.PdfReader(filename + ".pdf")
        except:
            print("Invalid file, try again.")
    return reader


def generate_bookmarks(reader: pypdf.PdfReader) -> pypdf.PdfWriter:
    """Generates bookmarks for a PDF file defined by `reader`."""
    writer = pypdf.PdfWriter()

    for page_num, page in enumerate(reader.pages):
        writer.add_page(page)
        text = page.extract_text()
        # If there is no text on a page, we will just skip it
        try:
            heading = text[:text.index("\n")]
        except:
            continue
        writer.add_outline_item(heading, page_num)

    writer.add_metadata(reader.metadata)

    return writer


def name_new_pdf(filename: str) -> str:
    """Generates new name for the output file."""
    if filename.endswith(".pdf"):
        # new_filename = filename
        new_filename = filename[:filename.index(".pdf")] + "_new" + ".pdf" # TODO: will be deleted eventually
    else:
        # new_filename = filename + ".pdf"
        new_filename = filename + "_new" + ".pdf" # TODO: will be deleted eventually
    return new_filename


def main():

    print("\n--- PDF tool ---")

    # Check if any valid PDF was inputted as command-line argument
    try:
        filename = sys.argv[1]
        reader = pypdf.PdfReader(filename)
        invalid_file = False
    except:
        invalid_file = True

    # Main loop
    while True:
        while invalid_file:
            filename = input("\nGive the name of the PDF file (Q to quit): ")
            if filename.lower() == "q":
                quit()
            else:
                reader = get_pdf_reader(filename)
                if reader: invalid_file = False

        print(f"\nReading {filename} with {len(reader.pages)} pages...")

        if reader.outline:
            answer = input("\nThis PDF already contains bookmarks,\nAre you sure you want to replace them? (Y/N): ")
            if answer.lower() != 'y':
                invalid_file = True
                continue

        writer = generate_bookmarks(reader)

        new_filename = name_new_pdf(filename)

        try:
            with open(f"{new_filename}", "wb") as file:
                writer.write(file)
            print(f"Success! Added {writer.get_outline_root()['/Count']} bookmarks to {new_filename}.")
        except:
            print(f"Something went wrong when attempting to save the file {new_filename}")
            print("Make sure you do not have a file with that name open.\n")
        invalid_file = True

if __name__ == '__main__':
    main()