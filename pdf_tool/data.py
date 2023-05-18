"""
Contains a class for storing and processing data.
"""
import pypdf
from pdf_tool.pdf import Pdf

class Data:
    """Class for storing and processing `Pdf` objects."""
    def __init__(self):
        self.pdfs = []

    def add_pdfs(self, filenames: list):
        for filename in filenames:
            if filename in self.get_filenames():
                self.remove_pdf(filename)
            self.add_pdf(Pdf(filename))

    def add_pdf(self, pdf_file: Pdf):
        self.pdfs.append(pdf_file)

    def remove_pdf(self, filename: str):
        self.pdfs = [p for p in self.pdfs if p.filename != filename]

    def get_filenames(self) -> list:
        return [pdf_file.filename for pdf_file in self.pdfs]
    
    def generate_bookmarks(self, filenames):
        if not self.pdfs or filenames == []:
            return False
        else:
            for pdf in self.pdfs:
                if pdf.filename in filenames:
                    pdf.generate_bookmarks()
            return True

    def combine_pdfs(self, filenames):
        readers = [pdf.reader for pdf in self.pdfs if pdf.filename in filenames]
        if readers:
            writer = pypdf.PdfWriter()
            page_num = 0
            for reader in readers:
                first_page = True
                for page in reader.pages:
                    writer.add_page(page)
                    text = page.extract_text()
                    # If there is no text on a page, we will just skip it
                    try:
                        heading = text[:text.index("\n")]
                    except:
                        continue
                    if first_page:
                        parent_bookmark = writer.add_outline_item(heading, page_num)
                        first_page = False
                    else:
                        writer.add_outline_item(heading, page_num, parent_bookmark)
                    page_num += 1
            if writer:
                try:
                    writer.page_mode = '/UseOutlines'
                    with open('Combined.pdf', "wb") as file:
                        writer.write(file)
                    return True
                except:
                    return False
        return False
    
    def get_bookmarks(self, filename: str) -> list:
        bookmarks = [pdf.reader.outline for pdf in self.pdfs if pdf.filename == filename]
        return bookmarks

    def reset(self):
        self.__init__()
