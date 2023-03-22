"""
Contains the GUI of the app.
"""
import tkinter as tk
from tkinter import filedialog as fd

import customtkinter as ctk

from pdf_tool.data import Data

PADDING = 10
CORNER_RADIUS = 5


class PDFList(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pdf_checkbox_list = []
        self.columnconfigure(0, weight=1)

    def add_pdfs(self, filenames: list):
        for filename in filenames:
            if filename not in [cb.cget('text') for cb in self.pdf_checkbox_list]:
                checkbox = ctk.CTkCheckBox(self, text=filename)
                checkbox.grid(row=len(self.pdf_checkbox_list), column=0, columnspan=3, sticky='nw', pady=(0, PADDING))
                self.pdf_checkbox_list.append(checkbox)

    def remove_selected(self):
        for cb in reversed(self.pdf_checkbox_list):
            if cb.get():
                cb.destroy()
                self.pdf_checkbox_list.remove(cb)
        for row_num, cb in enumerate(self.pdf_checkbox_list):
            cb.grid_forget()
            cb.grid(row=row_num, column=0, columnspan=3, sticky='nw', pady=(0, PADDING))

    def get_selected(self):
        return [cb.cget('text') for cb in self.pdf_checkbox_list if cb.get()]

    def toggle_all(self, checked):
        if checked:
            for cb in self.pdf_checkbox_list:
                cb.select()
        else:
            for cb in self.pdf_checkbox_list:
                cb.deselect()


class App(ctk.CTk):
    """
    Class for the GUI.
    Takes a `Data` object as parameter to create a connection
    between the GUI and the data.
    """
    def __init__(self, data: Data):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.title('PDF tool')
        self.geometry('500x650')
        self.data = data

        self.frm_main = ctk.CTkFrame(self)

        self.lbl_choose_pdf = ctk.CTkLabel(self.frm_main, text='PDF files')
        self.lbl_choose_pdf.pack(pady=(PADDING, 0))

        # PDF list section
        self.frm_pdf_list_section = ctk.CTkFrame(self.frm_main)
        self.frm_pdf_list_section.columnconfigure(0, weight=1)

        self.checkbox_select_all = ctk.CTkCheckBox(self.frm_pdf_list_section, text='')
        self.checkbox_select_all.grid(row=0, column=0, sticky='nw', padx=PADDING, pady=(PADDING, 0))

        self.btn_browse = ctk.CTkButton(self.frm_pdf_list_section, width=20, text="Browse", command=self.choose_pdfs)
        self.btn_browse.grid(row=0, column=1, sticky='ne', padx=(0, PADDING), pady=(PADDING, 0))

        self.btn_remove = ctk.CTkButton(self.frm_pdf_list_section, width=20, text="Remove selected")
        self.btn_remove.grid(row=0, column=2, sticky='ne', padx=(0, PADDING), pady=(PADDING, 0))

        self.pdf_list = PDFList(self.frm_pdf_list_section, fg_color='transparent')
        self.pdf_list.grid(row=1, column=0, columnspan=3, pady=PADDING/2, padx=(PADDING/2-1, PADDING/2+1), sticky='nsew')

        self.checkbox_select_all.configure(command=lambda: self.pdf_list.toggle_all(self.checkbox_select_all.get()))
        self.btn_remove.configure(command=self.pdf_list.remove_selected)

        self.frm_pdf_list_section.pack(fill='both', padx=PADDING, pady=PADDING)


        self.btn_generate_bookmarks = ctk.CTkButton(self.frm_main,
                                                 text='Generate bookmarks',
                                                 width=20,
                                                 command=self.generate_bookmarks)
        self.btn_generate_bookmarks.pack(pady=PADDING)

        self.btn_combine_pdfs = ctk.CTkButton(self.frm_main,
                                           text='Combine PDF files',
                                           width=20,
                                           command=self.combine_pdfs)
        self.btn_combine_pdfs.pack(pady=PADDING)

        self.btn_save_changes = ctk.CTkButton(self.frm_main,
                                           text='Save changes',
                                           width=20,
                                           command=self.save_changes)
        self.btn_save_changes.pack(pady=PADDING)

        self.btn_quit = ctk.CTkButton(self.frm_main,
                                   text='Quit',
                                   width=20,
                                   command=self.quit)
        self.btn_quit.pack(pady=(PADDING, 0))
        
        self.frm_main.pack(fill='both', ipadx=PADDING, ipady=PADDING, padx=PADDING, pady=PADDING)

        self.frm_statusbar = ctk.CTkFrame(self)
        self.lbl_status = ctk.CTkLabel(self.frm_statusbar, text="Choose PDF files to begin")
        self.lbl_status.pack()
        self.frm_statusbar.pack(ipadx=PADDING, padx=PADDING)

    def choose_pdfs(self):
        self.data.add_pdfs(fd.askopenfilenames(title="Choose PDF files",
                                                initialdir='./',
                                                filetypes=[('PDF file', '*.pdf')]))
        self.pdf_list.add_pdfs(self.data.get_filenames())
        if self.data.get_filenames():
            self.update_status("Choose what you want to do with the PDF files")
        else:
            self.update_status("Choose PDF files")

    def remove_pdfs(self):
        selected = self.pdf_list.get_selected()
        self.pdf_list.remove_selected()
        for filename in selected:
            self.data.remove_pdf(filename)
        self.update_status("Removed selected files")

    
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
        if self.data.save_files():
            self.update_status("Changes saved succefully")
        else:
            self.update_status("Choose PDF files first")

    def update_status(self, message: str):
        self.lbl_status.configure(text=message)

    def quit(self):
        self.destroy()
