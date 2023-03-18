import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PDF tool')
        self.geometry('500x500')

        self.lbl_choose_pdf = ttk.Label(self, text='Choose PDF file')
        self.lbl_choose_pdf.pack()

        self.btn_browse_pdf = ttk.Button(self, text='Browse')
        self.btn_browse_pdf['command'] = self.select_input_pdf
        self.btn_browse_pdf.pack()

    def select_input_pdf(self):
        print("Clicked button")
        filenames = fd.askopenfilenames(title="Choose PDF file", initialdir='./', filetypes=[('PDF file', '*.pdf')])
        print(filenames)


if __name__ == "__main__":
    app = App()
    app.mainloop()