"""
Contains a class for storing and processing data.
"""
from pdf_tool import utils
from pdf_tool.pdf import Pdf

class Data:
    def __init__(self):
        self.pdfs = []

    def add_pdfs(self, filenames: list):
        for filename in filenames:
            self.pdfs.append(Pdf(filename))

    def add_pdf(self, pdf_file: Pdf):
        self.pdfs.append(pdf_file)

    def remove_pdf(self, filename: str):
        self.pdfs = [p for p in self.pdfs if p.filename != filename]

    def get_filenames(self) -> list:
        return [pdf_file.filename for pdf_file in self.pdfs]
    
    def generate_bookmarks(self):
        for pdf in self.pdfs:
            pdf.writer = utils.generate_bookmarks(pdf.reader)

    def save_files(self):
        for pdf in self.pdfs:
            pdf.filename = utils.name_new_pdf(pdf.filename)
            utils.save_new_pdf(pdf.writer, pdf.filename)

    def reset(self):
        self.__init__()
