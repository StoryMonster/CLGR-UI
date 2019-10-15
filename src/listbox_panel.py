from tkinter import Frame, Listbox, Scrollbar, scrolledtext, Menu
from tkinter import RIGHT, X, Y, TOP, BOTH, BOTTOM, HORIZONTAL, END

class PopupMenu(Menu):
    def __init__(self, parent=None):
        Menu.__init__(self, parent, tearoff=0)

    def show(self, x, y):
        self.post(x=x, y=y)

    def register(self, name, callback):
        self.add_command(label=name, command=callback)


class ListBoxPanel(Frame):
    def __init__(self, parent, displayArea):
        super().__init__(parent)
        yscrollbar = Scrollbar(self)
        yscrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar = Scrollbar(self, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)
        self.listBox = Listbox(self, yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar, selectmode="single")
        yscrollbar.config(command=self.listBox.yview)
        xscrollbar.config(command=self.listBox.xview)
        self.listBox.pack(side=BOTTOM, expand=True, fill=BOTH)
        self.displayArea = displayArea
        self.popupMenu = PopupMenu(self)
        self.popupMenu.register("Open", self.openSelectedFile)
        self.listBox.bind("<ButtonPress-3>", self.rightClick)
        self.listBox.bind("<ButtonPress-1>", self.leftClick)
        self.mode = "FileSearch"

    def setSearchMode(self, mode):
        self.mode = mode

    def insert(self, data="", pos=END):
        self.listBox.insert(pos, data)

    def clear(self):
        self.listBox.delete(0, self.listBox.size())

    def openSelectedFile(self):
        indexs = self.listBox.curselection()
        if len(indexs) == 0: return
        filename = self.listBox.get(indexs[0])
        with open(filename, "r", encoding="utf-8") as fd:
            lines = fd.readlines()
            self.displayArea.clear()
            self.displayArea.appendLines(lines)

    def rightClick(self, event):
        if self.listBox.size() == 0: return
        self.popupMenu.show(event.x_root, event.y_root)

    def leftClick(self, event):
        if self.mode == "FileSearch": return
        indexs = self.listBox.curselection()
        if len(indexs) == 0: return
        filename = self.listBox.get(indexs[0])
        expectFilenameLine = ">>>" + filename + ":"
        expectLines = []
        if len(indexs) == 0: return
        with open("./temp/temp_result.data", "r") as fd:
            while True:
                line = fd.readline()
                if not line: break
                if len(expectLines) > 0 and line.find(">>>") == 0: break
                if (expectFilenameLine == line.rstrip() and len(expectLines) == 0) or len(expectLines) > 0:
                    expectLines.append(line.rstrip())
            self.displayArea.clear()
            self.displayArea.appendLines(expectLines)