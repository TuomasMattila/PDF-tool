"""
Contains the GUI of the app.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import sv_ttk

from pdf_tool.data import Data


class App(tk.Tk):
    """Class for the main application."""
    def __init__(self, data: Data):
        super().__init__()
        sv_ttk.set_theme("dark")
        self.title('PDF tool')
        self.geometry('500x500')
        self.data = data

        self.frm_main = ttk.Frame(self)

        self.lbl_choose_pdf = ttk.Label(self.frm_main, text='Choose PDF files')
        self.lbl_choose_pdf.pack(pady=10)

        self.list_pdfs = tk.Listbox(self.frm_main)
        self.list_pdfs.pack(fill='both')

        self.btn_browse_pdf = ttk.Button(self.frm_main,
                                         text='Browse',
                                         width=20,
                                         command=self.choose_pdfs)
        self.btn_browse_pdf.pack(pady=10)

        self.btn_clear_pdfs = ttk.Button(self.frm_main,
                                         text='Clear list',
                                         width=20,
                                         command=self.remove_pdfs)
        self.btn_clear_pdfs.pack(pady=10)

        self.btn_generate_bookmarks = ttk.Button(self.frm_main,
                                                 text='Generate bookmarks',
                                                 width=20,
                                                 command=self.generate_bookmarks)
        self.btn_generate_bookmarks.pack(pady=10)

        self.btn_save_changes = ttk.Button(self.frm_main,
                                           text='Save changes',
                                           width=20,
                                           command=self.save_changes)
        self.btn_save_changes.pack(pady=10)

        self.btn_quit = ttk.Button(self.frm_main,
                                   text='Quit',
                                   width=20,
                                   command=self.quit)
        self.btn_quit.pack(pady=10)
        
        self.frm_main.pack(fill='both', padx=10, pady=10)


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

    def quit(self):
        self.destroy()
