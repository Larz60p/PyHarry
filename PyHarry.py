#
#    PyHarry.py
#
#    This file is part of PyHarry.py.
#
#    Copyright (c) 2016 - Larry McCaig (A.K.A. Larz60+)
#
#    Licensed under GNU GENERAL PUBLIC LICENSE
#
import importlib
import HarryGui

class ImportModule:
    def __init__(self):
        self.moduleLocation = None

    def prepare_loc(self, loc):
        try:
            x = str(loc)
            x = x[x.rfind("from '"):len(x)]
            self.moduleLocation = x[x.find("'")+1:len(x)-2]
        except None:
            self.moduleLocation = None

    def import_module(self, name, verbose=False):
        newname = name
        try:
            loc = importlib.import_module(newname)
            self.prepare_loc(loc)
            if verbose:
                print('imported: {}'.format(self.moduleLocation))
            return True
        except ImportError:
            if "." in newname:
                newname = newname[0:newname.rfind(".")]
                if self.import_module(newname):
                    return True
            if verbose:
                print('Could not import: {}'.format(name))
        return False


def main():
    gb = HarryGui.HarryGui()
    gb.create_widgets()
    gb.loadtree()
    gb.mainloop()

if __name__ == '__main__':
    main()
