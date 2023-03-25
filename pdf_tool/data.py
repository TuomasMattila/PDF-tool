"""
Contains a class for storing and processing data.
"""
from pdf_tool import utils
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
        if not self.pdfs:
            return False
        else:
            for pdf in self.pdfs:
                if pdf.filename in filenames:
                    pdf.writer = utils.generate_bookmarks(pdf.reader)
            return True

    def combine_pdfs(self, filenames):
        readers = [pdf.reader for pdf in self.pdfs if pdf.filename in filenames]
        if readers:
            writer = utils.combine_pdfs(readers)
            if writer:
                utils.save_new_pdf(writer, 'Combined.pdf')
                return True
        return False
    
    def get_bookmarks(self, filename: str) -> list:
        bookmarks = [pdf.get_bookmarks() for pdf in self.pdfs if pdf.filename == filename]
        return bookmarks

    def save_files(self, filenames):
        if not self.pdfs:
            return False
        else:
            for pdf in self.pdfs:
                if pdf.filename in filenames:
                    # utils.save_new_pdf(pdf.writer, pdf.filename)
                    utils.save_new_pdf(pdf.writer, utils.name_new_pdf(pdf.filename)) # TODO: In the final version, we will not be generating the new filename, at least not like this
            return True

    def reset(self):
        self.__init__()
