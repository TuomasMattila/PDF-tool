"""
Contains the GUI of the app.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from pdf_tool.data import Data


class App(tk.Tk):
    def __init__(self, data: Data):
        super().__init__()
        self.title('PDF tool')
        self.geometry('500x500')
        self.data = data

        self.lbl_choose_pdf = ttk.Label(self, text='Choose PDF files')
        self.lbl_choose_pdf.pack()

        self.list_pdfs = tk.Listbox(self)
        self.list_pdfs.pack(fill='both')

        self.btn_browse_pdf = ttk.Button(self,
                                         text='Browse',
                                         command=self.choose_pdfs)
        self.btn_browse_pdf.pack()

        self.btn_clear_pdfs = ttk.Button(self,
                                         text='Clear list',
                                         command=self.remove_pdfs)
        self.btn_clear_pdfs.pack()

        self.btn_generate_bookmarks = ttk.Button(self,
                                                 text='Generate bookmarks',
                                                 command=self.generate_bookmarks)
        self.btn_generate_bookmarks.pack()

        self.btn_save_changes = ttk.Button(self,
                                           text='Save changes',
                                           command=self.save_changes)
        self.btn_save_changes.pack()


    def choose_pdfs(self):
        print("Clicked button")
        self.data.add_pdfs(fd.askopenfilenames(title="Choose PDF files",
                                                initialdir='./',
                                                filetypes=[('PDF file', '*.pdf')]))
        print(self.data.get_filenames())
        self.list_pdfs.delete(0, len(self.data.get_filenames()))
        self.list_pdfs.insert(0, *self.data.get_filenames())


    def remove_pdfs(self):
        self.list_pdfs.delete(0, len(self.data.get_filenames()))
        self.data.reset()
    

    def generate_bookmarks(self):
        self.data.generate_bookmarks()


    def save_changes(self):
        self.data.save_files()