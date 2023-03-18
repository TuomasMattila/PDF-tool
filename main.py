"""
PDF-tool for modifying PDF files in different ways.
This file should be used to run the program.
"""

from pdf_tool.app import App
from pdf_tool.data import Data

if __name__ == "__main__":
    data = Data()
    app = App(data)
    app.mainloop()