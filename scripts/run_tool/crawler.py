import os
import logging
#(lang,test) = abs PATH to test

def get_ignore_list(path):
    ignorelist = []
    ignorefile = path + os.sep + "ignore.txt"
    if os.path.isfile(ignorefile):
        with open(ignorefile) as f:
            for line in f:
                ignoredir = line.strip()
                ignorelist.append(ignoredir)
    return ignorelist

def findname(dir_entry_obj):
    rename_file = dir_entry_obj.path + os.sep + "rename.txt"
    if os.path.isfile(rename_file):
        with open(rename_file) as f:
            return f.read().strip()
    else:
        return dir_entry_obj.name

class Crawler:
    def __init__(self, rootpath):
        self.dict = {}
        ignorelang = get_ignore_list(rootpath) #list of ignored languages
        for lang in os.scandir(rootpath):
            if lang.is_dir() and (lang.name[0] != '.') and (lang.name not in ignorelang):
                langname = findname(lang)
                logging.debug("Discovered language: " + langname)
                #lang and bench are DirEntry objects wih its own library methods
                ignoretest = get_ignore_list(lang.path) # list of ignored tests
                for bench in os.scandir(lang.path):
                    if bench.is_dir() and (bench.name[0] != '.') and \
                       (bench.name not in ignoretest):
                        testname = findname(bench)
                        logging.debug("Discovered benchmark " + testname + " in " + langname)
                        self.dict[(langname, testname)] = bench.path

    def get_dict(self):
        return self.dict

