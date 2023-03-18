import pypdf

class Pdf:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.reader = pypdf.PdfReader(filename)
        except:
            try:
                self.reader = pypdf.PdfReader(filename + ".pdf")
            except:
                self.reader = None
        self.writer = pypdf.PdfWriter()
        for page_num, page in enumerate(self.reader.pages):
            self.writer.add_page(page)
        self.writer.add_metadata(self.reader.metadata)