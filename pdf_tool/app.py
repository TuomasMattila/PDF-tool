"""
Contains the GUI of the app.
"""
import customtkinter as ctk
from customtkinter import filedialog as fd

from pdf_tool.data import Data

PADDING = 10
CORNER_RADIUS = 5


class PDFList(ctk.CTkScrollableFrame):
    def __init__(self, master, controller, **kwargs):
        ctk.CTkScrollableFrame.__init__(self, master, **kwargs)
        self.controller = controller
        self.pdf_checkbox_list = []
        self.columnconfigure(0, weight=1)

    def add_pdfs(self, filenames: list):
        for filename in filenames:
            if filename not in [cb.cget('text') for cb in self.pdf_checkbox_list]:
                checkbox = ctk.CTkCheckBox(self, text=filename)
                checkbox.grid(row=len(self.pdf_checkbox_list), column=0, sticky='nw', pady=(0, PADDING))
                checkbox.bind('<Button-1>', self.controller.on_pdf_selected)
                self.pdf_checkbox_list.append(checkbox)

    def remove_selected(self):
        for cb in reversed(self.pdf_checkbox_list):
            if cb.get():
                cb.destroy()
                self.pdf_checkbox_list.remove(cb)
        for row_num, cb in enumerate(self.pdf_checkbox_list):
            cb.grid_forget()
            cb.grid(row=row_num, column=0, sticky='nw', pady=(0, PADDING))

    def get_selected(self):
        return [cb.cget('text') for cb in self.pdf_checkbox_list if cb.get()]

    def toggle_all(self, checked):
        if checked:
            for cb in self.pdf_checkbox_list:
                cb.select()
        else:
            for cb in self.pdf_checkbox_list:
                cb.deselect()


class BookmarkList(ctk.CTkScrollableFrame):
    def __init__(self, master, controller, **kwargs):
        ctk.CTkScrollableFrame.__init__(self, master, **kwargs)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.bookmark_labels = []
        self.current_outline = []

    def update_list(self, bookmarks: list):
        for bookmark in self.bookmark_labels:
            bookmark.destroy()
        self.bookmark_labels = []
        self.current_outline = bookmarks
        self.create_labels(self.current_outline)

    def create_labels(self, outline, level=0):
        for item in outline:
            if isinstance(item, list):
                self.create_labels(item, level=level+1)
            else:
                lbl_bookmark = ctk.CTkLabel(self, text=item['/Title'])
                lbl_bookmark.grid(row=len(self.bookmark_labels), column=0, sticky='nw', padx=(level*PADDING, 0))
                self.bookmark_labels.append(lbl_bookmark)


class App(ctk.CTk):
    """
    Class for the GUI.
    Takes a `Data` object as parameter to create a connection
    between the GUI and the data.
    """
    def __init__(self, data: Data):
        super().__init__()
        ctk.set_appearance_mode('dark') # TODO: This is only temporary, the app should look good with light mode also
        self.title('PDF tool')
        self.geometry('800x600')
        self.data = data
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)


        self.frm_main = ctk.CTkFrame(self)
        self.frm_main.columnconfigure(0, weight=1)
        self.lbl_choose_pdf = ctk.CTkLabel(self.frm_main, text='PDF files')
        self.lbl_choose_pdf.grid(row=0, column=0, pady=(PADDING, 0), sticky='nsew')

        # PDF list section
        self.frm_pdf_list_section = ctk.CTkFrame(self.frm_main)
        self.frm_pdf_list_section.columnconfigure(0, weight=1)

        self.checkbox_select_all = ctk.CTkCheckBox(self.frm_pdf_list_section, text='')
        self.checkbox_select_all.grid(row=0, column=0, sticky='nw', padx=PADDING, pady=PADDING)

        self.btn_browse = ctk.CTkButton(self.frm_pdf_list_section, width=20, height=24, text="Browse", command=self.choose_pdfs)
        self.btn_browse.grid(row=0, column=1, sticky='ne', padx=(0, PADDING), pady=PADDING)

        self.btn_remove = ctk.CTkButton(self.frm_pdf_list_section, width=20, height=24, text="Remove selected")
        self.btn_remove.grid(row=0, column=2, sticky='ne', padx=(0, PADDING), pady=PADDING)

        self.separator = ctk.CTkFrame(self.frm_pdf_list_section, height=2, fg_color='#696969')
        self.separator.grid(row=1, column=0, columnspan=3, sticky='ew', padx=PADDING)

        self.pdf_list = PDFList(self.frm_pdf_list_section, self, fg_color='transparent')
        self.pdf_list.grid(row=2, column=0, columnspan=3, pady=(0, PADDING/2), padx=(PADDING/2-1, PADDING/2+1), sticky='nsew')

        self.checkbox_select_all.configure(command=lambda: self.pdf_list.toggle_all(self.checkbox_select_all.get()))
        self.btn_remove.configure(command=self.remove_pdfs)

        self.frm_pdf_list_section.grid(row=1, column=0, sticky='nsew', padx=PADDING, pady=PADDING)

        # Buttons below PDF list
        self.frm_buttons = ctk.CTkFrame(self.frm_main, fg_color='transparent')
        self.btn_generate_bookmarks = ctk.CTkButton(self.frm_buttons,
                                                 text='Generate bookmarks',
                                                 width=20,
                                                 command=self.generate_bookmarks)
        self.btn_generate_bookmarks.pack(pady=(PADDING, 0))
        self.btn_combine_pdfs = ctk.CTkButton(self.frm_buttons,
                                           text='Combine PDF files',
                                           width=20,
                                           command=self.combine_pdfs)
        self.btn_combine_pdfs.pack(pady=(PADDING, 0))
        self.btn_quit = ctk.CTkButton(self.frm_buttons,
                                   text='Quit',
                                   width=20,
                                   command=self.quit)
        self.btn_quit.pack(pady=(PADDING, 0))
        self.frm_buttons.grid(row=2, column=0, sticky='nsew')

        self.frm_main.grid(row=0, column=0, sticky='nsew', ipadx=PADDING, ipady=PADDING, padx=PADDING, pady=(PADDING, 0))


        # Bookmark list
        self.frm_bookmark_list = ctk.CTkFrame(self)
        self.lbl_bookmarks = ctk.CTkLabel(self.frm_bookmark_list, text='Bookmarks')
        self.lbl_bookmarks.pack(pady=PADDING)
        self.bookmark_list = BookmarkList(self.frm_bookmark_list, self, fg_color='transparent')
        self.bookmark_list.pack(fill='both', expand=True, padx=PADDING/2, pady=(0, PADDING))
        self.frm_bookmark_list.grid(row=0, column=1, sticky='nsew', padx=(0, PADDING), pady=(PADDING, 0))


        # Statusbar
        self.frm_statusbar = ctk.CTkFrame(self)
        self.lbl_status = ctk.CTkLabel(self.frm_statusbar, text="Choose PDF files to begin")
        self.lbl_status.pack()
        self.frm_statusbar.grid(row=1, column=0, sticky='nsew', columnspan=2, ipadx=PADDING, padx=PADDING, pady=PADDING)

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
        self.update_bookmark_list()
        self.update_status("Removed selected files")
    
    def generate_bookmarks(self):
        self.update_status("Generating bookmarks...")
        if self.data.generate_bookmarks(self.pdf_list.get_selected()):
            self.update_status("Bookmarks generated")
            self.update_bookmark_list()
        else:
            self.update_status("Choose PDF files first")

    def combine_pdfs(self):
        self.update_status("Combining PDF files...")
        if self.data.combine_pdfs(self.pdf_list.get_selected()):
            self.update_status('Combined PDF files into Combined.pdf')
        else:
            self.update_status('Failed to combine PDF files, make sure your files are not corrupted')

    def update_status(self, message: str):
        self.lbl_status.configure(text=message)

    def on_pdf_selected(self, event):
        self.update_bookmark_list()

    def update_bookmark_list(self):
        if len(self.pdf_list.get_selected()) == 1:
            selection = self.pdf_list.get_selected()[0]
            bookmarks = self.data.get_bookmarks(selection)[0]
            if bookmarks:
                self.bookmark_list.update_list(bookmarks)
            else:
                self.bookmark_list.update_list([])
        else:
            self.bookmark_list.update_list([])

    def quit(self):
        self.destroy()
