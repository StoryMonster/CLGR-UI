import subprocess
import sys
import os


class SearchProc:
    def __init__(self, bin, dirs, files, texts, flags):
        self.bin = bin
        self.dirs = dirs
        self.files = files
        self.texts = texts
        self.flags = flags
        self.proc = None

    def run(self):
        if self.proc is not None:
            raise Exception("There is a searching process existing!")
        cmd = [self.bin, "-d"]
        cmd.extend(self.dirs)
        if len(self.files) > 0:
            cmd.append("-f")
            cmd.extend(self.files)
        if len(self.texts) > 0:
            cmd.append("-t")
            cmd.extend(self.texts)
        if len(self.flags) > 0:
            cmd.extend(self.flags)
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    
    def kill(self):
        if self.proc is None: return
        try:
            os.kill(self.proc.pid, 9)
        except PermissionError:
            print(f"The search process({self.proc.pid}) cannot be terminated!")
        self.proc = None

    def readline(self):
        if self.proc is None: return None
        return self.proc.stdout.readline()
