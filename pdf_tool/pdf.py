"""
Class for storing PDf file's filename, reader and writer.
"""
import pypdf

class Pdf:
    """
    Class that contains all information about one PDF file.
    Stores the filename, reader and writer for the pdf.

    Reader is generated using the `filename` given as an argument,
    and all pages and metadata from reader are added to the writer.
    """
    def __init__(self, filename: str):
        self.filename = filename
        try:
            self.reader = pypdf.PdfReader(filename)
        except:
            try:
                self.reader = pypdf.PdfReader(filename + ".pdf")
            except:
                self.reader = None
        # outline_str = str(self.reader.outline) # TODO: Remove these later, only for debugging purposes when needed
        # outline_list = outline_str.split(', ')
        # final_str = ''
        # for item in outline_list:
        #     if item.isdigit() or item.startswith('\'/Page\''):
        #         final_str += item + ', '
        #     else:
        #         final_str += item + ',\n'
        # print(final_str)
        self.writer = pypdf.PdfWriter()

    def get_bookmarks(self):
        if not self.reader:
            return False
        bookmarks = []
        self.get_bookmark_names(self.reader.outline, bookmarks)
        return bookmarks
    
    def get_bookmark_names(self, outline, bm_list):
        """
        Recursive function for getting all bookmarks in
        a hierarchical bookmarks structure.
        """
        for item in outline:
            if isinstance(item, list):
                self.get_bookmark_names(item, bm_list)
            else:
                bm_list.append(item['/Title'])