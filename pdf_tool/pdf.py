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
    BM_MAX_LENGTH = 85
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
        for page in self.reader.pages:
            self.writer.add_page(page)
        self.writer.add_metadata(self.reader.metadata)

    def generate_bookmarks(self):
        for page_num, page in enumerate(self.reader.pages):
            text = page.extract_text()
            # If there is no text on a page, we will just skip it
            try:
                heading = text[:text.index("\n")].strip() # TODO: Have to make sure the bookmark text is not too short or long, cutting to '\n' might not be sufficient at all times
                if len(heading) > self.BM_MAX_LENGTH:
                    heading = heading[:self.BM_MAX_LENGTH]
            except:
                continue
            self.writer.add_outline_item(heading, page_num) # TODO: How to adjust the zoom of the bookmark? ('fit' parameter? How to use?)
        self.save_changes()

    def save_changes(self):
        try:
            self.writer.page_mode = '/UseOutlines'
            with open(f"{self.filename}", "wb") as file:
                self.writer.write(file)
            self.reader = pypdf.PdfReader(self.filename)
            return True
        except:
            print("Something went wrong")
            return False

    def edit_bookmark(self, old_bookmark, new_bookmark):
        pass

    def find_bookmark(self, bookmark, search_from=None):
        if search_from == None:
            search_from = self.reader.outline
        for item in search_from:
            if item == bookmark:
                return item
            else:
                if isinstance(item, list):
                    value = self.find_bookmark(bookmark, item)
                    if value:
                        return value
        return False
        




    
