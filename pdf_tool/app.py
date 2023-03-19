"""
Contains the GUI of the app.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import sv_ttk

from pdf_tool.data import Data


class App(tk.Tk):
    """
    Class for the GUI.
    Takes a `Data` object as parameter to create a connection
    between the GUI and the data.
    """
    def __init__(self, data: Data):
        super().__init__()
        sv_ttk.set_theme("dark")
        self.title('PDF tool')
        self.geometry('500x600')
        self.data = data

        self.frm_main = ttk.Frame(self)

        self.lbl_choose_pdf = ttk.Label(self.frm_main, text='Choose PDF files')
        self.lbl_choose_pdf.pack(pady=10)

        self.list_pdfs = tk.Listbox(self.frm_main)
        self.list_pdfs.bind('<<ListboxSelect>>', self.on_pdf_selected)
        self.list_pdfs.bind('<Double-Button-1>', self.remove_pdf)
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

        self.btn_combine_pdfs = ttk.Button(self.frm_main,
                                           text='Combine PDF files',
                                           width=20,
                                           command=self.combine_pdfs)
        self.btn_combine_pdfs.pack(pady=10)

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

        self.lbl_status = ttk.Label(self.frm_main, text="Choose PDF files")
        self.lbl_status.pack(pady=10)
        
        self.frm_main.pack(fill='both', padx=10, pady=10)

    def choose_pdfs(self):
        self.data.add_pdfs(fd.askopenfilenames(title="Choose PDF files",
                                                initialdir='./',
                                                filetypes=[('PDF file', '*.pdf')]))
        self.list_pdfs.delete(0, 'end')
        self.list_pdfs.insert(0, *self.data.get_filenames())
        if self.list_pdfs.get(0, 'end'):
            self.update_status("Choose what you want to do with the PDF files")
        else:
            self.update_status("Choose PDF files")

    def remove_pdfs(self):
        self.list_pdfs.delete(0, 'end')
        self.data.reset()
        self.update_status("Choose PDF files")

    
    def generate_bookmarks(self):
        self.update_status("Generating bookmarks...")
        if self.data.generate_bookmarks():
            self.update_status("Bookmarks generated")
        else:
            self.update_status("Choose PDF files first")

    def combine_pdfs(self):
        self.update_status("Combining PDF files...")
        if self.data.combine_pdfs():
            self.update_status('Combined PDF files into Combined.pdf')
        else:
            self.update_status('Failed to combine PDF files, make sure your files are not corrupted')

    def on_pdf_selected(self, event):
        if self.list_pdfs.curselection():
            print(self.data.get_bookmarks(self.list_pdfs.get(self.list_pdfs.curselection()[0])))

    def remove_pdf(self, event):
        selection = self.list_pdfs.curselection()[0]
        self.data.remove_pdf(self.list_pdfs.get(selection))
        self.list_pdfs.delete(selection)

    def save_changes(self):
        self.data.save_files()

    def update_status(self, message: str):
        self.lbl_status['text'] = message

    def quit(self):
        self.destroy()
