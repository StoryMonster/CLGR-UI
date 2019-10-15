from tkinter import Tk, Frame, Scrollbar, scrolledtext
from tkinter import RIGHT, LEFT, X, BOTTOM, TOP, BOTH, HORIZONTAL
from control_panel import ControlPanel
from search_process import SearchProc
from subprocess_data_receive_thread import DataReceiveThread
from listbox_panel import ListBoxPanel
from text_reader import TextReader

class LeftSidePanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.controlPanel = ControlPanel(self, self.doSearch)
        self.listbox = ListBoxPanel(self, parent.rightPanel)
        self.controlPanel.pack(side=TOP, fill=BOTH)
        self.listbox.pack(side=BOTTOM, expand=True, fill=BOTH)
        self.proc = None
        self.receiveThread = None
        self.tempFile = None
    
    def doSearch(self, bin, dirs, filekeywords, textkeywords, flags):
        self.listbox.clear()
        self.proc = SearchProc(bin, dirs, filekeywords, textkeywords, flags)
        self.proc.run()
        # 开启新线程查询子进程数据
        if len(textkeywords) == 0:
            self.listbox.setSearchMode("FileSearch")
            self.receiveThread = DataReceiveThread(self.proc, self.receivedLineWhenFileSearch)
        else:
            self.tempFile = open("./temp/temp_result.data", "w")
            self.listbox.setSearchMode("TextSearch")
            self.receiveThread = DataReceiveThread(self.proc, self.receivedLinesWhenTextSearch)
        self.receiveThread.start()
    
    def receivedLineWhenFileSearch(self, line, isLastLine):
        if not isLastLine:
            self.listbox.insert(line)
        else:
            self.controlPanel.setStatusNotice(line)

    def receivedLinesWhenTextSearch(self, line, isLastLine):
        if not isLastLine:
            if line.find(">>>") == 0:
                self.listbox.insert(line[3:-1])
            if self.tempFile is not None:
                self.tempFile.write(line.rstrip()+"\n")
        else:
            self.controlPanel.setStatusNotice(line)
            if self.tempFile is not None:
                self.tempFile.close()
                self.tempFile = None
    
    def onClose(self):
        if self.tempFile is not None:
            self.tempFile.close()
            self.tempFile = None
        if self.receiveThread is not None:
            self.receiveThread.terminate()
        if self.proc is not None:
            self.proc.kill()
            self.proc = None

class MainWindow(Tk):
    def __init__(self, context):
        Tk.__init__(self)
        self.context = context
        self.title("CLGR")
        self.rightPanel = TextReader(self)
        self.rightPanel.grid(row=0, column=1, sticky="nsew")
        self.leftPanel = LeftSidePanel(self)
        self.leftPanel.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.onClose)
    
    def onClose(self):
        self.leftPanel.onClose()
        self.destroy()
