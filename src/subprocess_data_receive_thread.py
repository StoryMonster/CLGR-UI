from threading import Thread


class DataReceiveThread(Thread):
    def __init__(self, subproc, lineHandler):
        super().__init__()
        self.listenProc = subproc
        self.lineHandler = lineHandler

    def terminate(self):
        pass

    def run(self):
        while True:
            line = self.listenProc.readline().decode("utf-8")
            if line.strip() == "": continue
            isLastLine = line.find("Search End! Matched") == 0
            self.lineHandler(line.strip(), isLastLine)
            if isLastLine: break
