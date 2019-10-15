from tkinter import Frame, Scrollbar, scrolledtext
from tkinter import HORIZONTAL, TOP, BOTH, X, BOTTOM


class TextReader(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        scrollbar= Scrollbar(self, orient=HORIZONTAL)
        self.textArea = scrolledtext.ScrolledText(self, bd=5, wrap="none", xscrollcommand=scrollbar.set)
        scrollbar.config(command=self.textArea.xview)
        self.textArea.pack(side=TOP, expand=True, fill=BOTH)
        scrollbar.pack(side=BOTTOM, fill=X)

    def appendLines(self, lines):
        for line in lines:
            self.textArea.insert("end", line.rstrip()+"\n")

    def clear(self):
        self.textArea.delete(1.0, "end")