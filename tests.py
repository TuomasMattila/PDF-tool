import unittest
import PDF_tool
import pypdf

class Tests(unittest.TestCase):

    def test_generate_bookmarks(self):
        init_writer = pypdf.PdfWriter()
        with open(f"empty.pdf", "wb") as file:
            init_writer.write(file)
        empty_reader = pypdf.PdfReader("empty.pdf")

        writer = PDF_tool.generate_bookmarks(empty_reader)
        self.assertEqual(writer.get_outline_root(), {})

        init_writer.add_blank_page(100, 100)
        init_writer.add_annotation(0, {})
        with open(f"one_bookmark.pdf", "wb") as file:
            init_writer.write(file)
        one_bookmark = pypdf.PdfReader("one_bookmark.pdf")

        writer = PDF_tool.generate_bookmarks(one_bookmark)
        print(writer.get_outline_root())
        self.assertEqual(writer.get_outline_root(), {})

    def test_get_pdf_reader(self):
        pass

    def test_name_new_pdf(self):
        pass

if __name__ == '__main__':
    unittest.main()