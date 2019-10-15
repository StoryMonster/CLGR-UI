from tkinter import Frame, Label, Button, Entry, StringVar, Checkbutton, IntVar
from tkinter import LEFT, RIGHT, TOP, BOTH, X
from tkinter.filedialog import askdirectory
import os

class DirItem(Frame):
    SEPARARE_CHARACTOR = ";"
    def __init__(self, parent):
        super().__init__(parent)
        self.lbl = Label(self, text="Search Path")
        self.strInput = StringVar()
        self.input = Entry(self, textvariable=self.strInput)
        self.browser = Button(self, text="OPEN", command=self.openFileBrowser)
        self.lbl.pack(side=LEFT)
        self.input.pack(side=LEFT, fill=X,  expand=True)
        self.browser.pack(side=LEFT)
    
    def openFileBrowser(self):
        dir = askdirectory()
        self.strInput.set(dir + DirItem.SEPARARE_CHARACTOR + self.strInput.get())

    def getDirs(self):
        items = self.strInput.get().split(DirItem.SEPARARE_CHARACTOR)
        dirs = []
        for item in items:
            dir = item.strip()
            if len(dir) > 0 and os.path.isdir(dir):
                dirs.append(dir)
        return dirs
    
    def reset(self):
        self.strInput.set("")

class KeywordItem(Frame):
    SEPARARE_CHARACTOR = ";"
    def __init__(self, parent, name):
        super().__init__(parent)
        self.lbl = Label(self, text=name)
        self.strInput = StringVar()
        self.input = Entry(self, textvariable=self.strInput)
        self.lbl.pack(side=LEFT)
        self.input.pack(side=LEFT, fill=X, expand=True)

    def getKeywords(self):
        items = self.strInput.get().split(KeywordItem.SEPARARE_CHARACTOR)
        keywords = []
        for item in items:
            keyword = item.strip()
            if len(keyword) > 0:
                keywords.append(keyword)
        return keywords

    def reset(self):
        self.strInput.set("")


class OperatePanel(Frame):
    def __init__(self, parent, searchCallback, resetCallback):
        super().__init__(parent)
        self.icSelected = IntVar()
        self.mwwSelected = IntVar()
        self.urSelected = IntVar()
        self.ifnSelected = IntVar()
        self.searchCallback = searchCallback
        self.resetCallback = resetCallback
        self.searchBtn = Button(self, text="Search", command=self.onClickSearch, padx=3)
        self.resetBtn = Button(self, text="Reset", command=self.onClickReset, padx=3)
        self.icBtn = Checkbutton(self, text="Ignore Case", command=self.onSelectIgnoreCase, variable=self.icSelected)
        self.mwwBtn = Checkbutton(self, text="Match Whole Word", command=self.onSelectMatchWholeWord, variable=self.mwwSelected)
        self.urBtn = Checkbutton(self, text="Use Regular", command=self.onSelectUseRegular, variable=self.urSelected)
        self.ifnBtn = Checkbutton(self, text="Ignore Folder Name", variable=self.ifnSelected)
        self.icBtn.grid(row=0, column=0, sticky="W")
        self.mwwBtn.grid(row=0, column=1, sticky="W")
        self.ifnBtn.grid(row=1, column=0, sticky="W")
        self.urBtn.grid(row=1, column=1, sticky="W")
        self.resetBtn.grid(row=2, column=0)
        self.searchBtn.grid(row=2, column=1)

    def getFlags(self):
        flags = []
        if self.icSelected.get() == 1:
            flags.append("-ic")
        if self.mwwSelected.get() == 1:
            flags.append("-mww")
        if self.urSelected.get() == 1:
            flags.append("-r")
        if self.ifnSelected.get() == 1:
            flags.append("-ifn")
        return flags
   
    def onClickSearch(self):
        if self.searchCallback is not None:
            self.searchCallback()

    def onClickReset(self):
        self.urSelected.set(0)
        self.icSelected.set(0)
        self.mwwSelected.set(0)
        self.ifnSelected.set(0)
        if self.resetCallback is not None:
            self.resetCallback()
    
    def onSelectIgnoreCase(self):
        self.urSelected.set(0)

    def onSelectMatchWholeWord(self):
        self.urSelected.set(0)

    def onSelectUseRegular(self):
        self.icSelected.set(0)
        self.mwwSelected.set(0)

class ControlPanel(Frame):
    def __init__(self, parent, doSearch=None):
        super().__init__(parent, bd=10)
        self.doSearch = doSearch
        self.dirSelector = DirItem(self)
        self.fileKeywordsPanel = KeywordItem(self, "Keywords of Filename")
        self.textKeywordsPanel = KeywordItem(self, "Keywords of Text")
        self.operatePanel = OperatePanel(self, self.onClickSearch, self.onClickReset)
        self.dirSelector.pack(side=TOP, expand=True, fill=BOTH)
        self.fileKeywordsPanel.pack(side=TOP, expand=True, fill=BOTH)
        self.textKeywordsPanel.pack(side=TOP, expand=True, fill=BOTH)
        self.operatePanel.pack(side=TOP, expand=True, fill=BOTH)
        self.strNotice = StringVar()
        self.noticeLbl = Label(self, textvariable=self.strNotice)
        self.noticeLbl.pack(side=TOP, expand=True, fill=X)
    
    def onClickSearch(self):
        dirs = self.dirSelector.getDirs()
        fileKeywords = self.fileKeywordsPanel.getKeywords()
        textKeywords = self.textKeywordsPanel.getKeywords()
        flags = self.operatePanel.getFlags()
        if self.doSearch is not None:
            self.strNotice.set("Searching...")
            self.doSearch("./bin/clgr.exe", dirs, fileKeywords, textKeywords, flags)

    def onClickReset(self):
        self.fileKeywordsPanel.reset()
        self.textKeywordsPanel.reset()
        self.dirSelector.reset()

    def setStatusNotice(self, notice):
        self.strNotice.set(notice)
