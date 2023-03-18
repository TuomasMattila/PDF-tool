from pdf_tool.app import App
from pdf_tool.data import Data

if __name__ == "__main__":
    data = Data()
    app = App(data)
    app.mainloop()