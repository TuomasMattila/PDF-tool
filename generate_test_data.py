"""
Script for generating test data.
Generates PDF files that have bookmarks in three levels.
"""

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
import random

def generate_test_pdf(title, first_min=0, first_max=0, second_min=0, second_max=0, third_min=0, third_max=0):
    """
    Generates a PDF file for testing purposes.
    ``title`` is the PDF file name, the rest are
    minimum and maximum number of bookmarks for each level.
    """
    canvas = Canvas(title)
    canvas.setTitle(title)
    for i in range(random.randint(first_min, first_max)):
        canvas.drawString(inch, 10*inch, f"{i+1} Heading asd")
        canvas.bookmarkPage(f"{i}")
        canvas.addOutlineEntry(f"{i+1} Heading", f"{i}", 0)
        canvas.showPage()
        for j in range(random.randint(second_min, second_max)):
            canvas.drawString(inch, 10*inch, f"{i+1}.{j+1} Heading asd")
            canvas.bookmarkPage(f"{i}.{j}")
            canvas.addOutlineEntry(f"{i+1}.{j+1} Heading", f"{i}.{j}", 1)
            canvas.showPage()
            for k in range(random.randint(third_min, third_max)):
                canvas.drawString(inch, 10*inch, f"{i+1}.{j+1}.{k+1} Heading asd")
                canvas.bookmarkPage(f"{i}.{j}.{k}")
                canvas.addOutlineEntry(f"{i+1}.{j+1}.{k+1} Heading", f"{i}.{j}.{k}", 2)
                canvas.showPage()
    canvas.showPage()
    canvas.save()

generate_test_pdf("test_0.pdf")
generate_test_pdf("test_1.pdf", 1, 5, 1, 5, 1, 5)
generate_test_pdf("test_2.pdf", 2, 5, 2, 5, 2, 5)
generate_test_pdf("test_3.pdf", 3, 5, 3, 5, 3, 5)
generate_test_pdf("test_4.pdf", 4, 5, 4, 5, 4, 5)
generate_test_pdf("test_5.pdf", 5, 5, 5, 5, 5, 5)
generate_test_pdf("test_6.pdf", 5, 5, 5, 5, 5, 5)
generate_test_pdf("test_7.pdf", 5, 5, 5, 5, 5, 5)
