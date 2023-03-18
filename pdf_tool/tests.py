import unittest
import pypdf
from utilities import generate_bookmarks

class Tests(unittest.TestCase):

    def test_generate_bookmarks(self):
        init_writer = pypdf.PdfWriter()
        with open(f"empty.pdf", "wb") as file:
            init_writer.write(file)
        empty_reader = pypdf.PdfReader("empty.pdf")

        writer = generate_bookmarks(empty_reader)
        self.assertEqual(writer.get_outline_root(), {})

    def test_get_pdf_reader(self):
        pass

    def test_name_new_pdf(self):
        pass

if __name__ == '__main__':
    unittest.main()