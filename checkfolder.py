import os
import sys
import hashlib


#TODO: get flat list of all files in folder

class File():
    def __init__(self, name, path, size, contenthash):
        self.name = name
        self.content = contenthash
        self.size = size
        self.path = path
        self

    def __eq__(self, other):
        self.name == other.name and \
            self.size == self.size
