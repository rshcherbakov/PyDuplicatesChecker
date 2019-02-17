import os
import sys
import hashlib
import filecmp

#TODO: get flat list of all files in folder

class FileUnit():
    def __init__(self, fname, dirpath):
        path = os.path.join(fname, dirpath)
        self.name = fname
        self.path = path
        self.size = os.path.getsize(path)

    def __eq__(self, other):
        return self.name == other.name and \
            self.size == self.size and \
            filecmp._do_cmp(self.path, other.path)

class CheckDir():
    def __init__(self,path):
        self.path = path
        self.filelist = []
        self.collect()
        print(self.filelist)

    def collect(self):
        for subdir, dirs, files in os.walk(self.path):
            self.filelist += [os.path.join(subdir,fname) for fname in files]

    def scan(self):
        pass




if __name__ == "__main__":
    dir = CheckDir(os.path.curdir)
