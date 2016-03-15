#
#    HarryHelp.py
#
#    This file is part of PyHarry.py.
#
#    Copyright (c) 2016 - Larry McCaig (A.K.A. Larz60+)
#
#    Licensed under GNU GENERAL PUBLIC LICENSE
#
import sys
from io import StringIO
import inspect
import importlib

class HarryHelp():
    def __init__(self):
        self.moduleLocation = None
        self.mhelp = None
        self.source = None

        self.modules = None
        self.keywords = None
        self.symbols = None
        self.topics = None

    def prepairLoc(self, loc):
        try:
            x = str(loc)
            x = x[x.rfind("from '"):len(x)]
            self.moduleLocation = x[x.find("'")+1:len(x)-2]
        except:
            self.moduleLocation = None

    def importModule(self, name, verbose=False):
        newname = name
        try:
            loc = importlib.import_module(newname)
            self.prepairLoc(loc)
            if verbose:
                print('imported: {}'.format(self.moduleLocation))
            return True
        except ImportError:
            if "." in newname:
                newname = newname[0:newname.rfind(".")]
                if self.importModule(newname):
                    return True
            if verbose:
                print('Could not import: {}'.format(name))
        return False

    def getSysHelp(self, name):
        newname = name
        try:
            orig = sys.stdout
            helpvar = StringIO()
            sys.stdout = helpvar
            help(newname)
            sys.stdout = orig
            self.mhelp = helpvar.getvalue()
            if self.mhelp.startswith('no Python doc'):
                if "." in newname:
                    newname = newname[0:newname.rfind(".")]
                    self.mhelp = self.getSysHelp(newname)
            return self.mhelp
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return 'No Help found for {}'.format(name)
                
    def inspect_getHelp(self, name):
        newname = name
        try:
            self.mhelp = inspect.getdoc(name)
            # print('found as: {}'.format(newname))
        except:
            if "." in newname:
                newname = newname[0:newname.rfind(".")]
                if self.inspect_getHelp(newname):
                    return newname
            return None
        return newname

    def getHelp(self, name):
        # pdb.set_trace()
        self.importModule(name)
        self.mhelp = None
        self.mhelp = self.getSysHelp(name)
        if self.mhelp:
            return name
        else:
            self.mhelp = 'No help found for {}'.format(name)
            return None

    def getSource(self, name):
        if self.importModule(name):
            filename = self.moduleLocation
            try:
                with open(filename, 'r') as f:
                    self.source = f.read()
                return True
            except:
                return None
        else:
            self.source = 'No Source found for {}'.format(name)
            return None

    def makeList(self, s, *skip):
        if s:
            count = 0
            thelist = []
            tmp1 = s.split('\n')
            for line in tmp1:
                count += 1
                if count < 4:
                    continue
                if line == '':
                    continue
                skipthis = False
                for item in skip:
                    if line.startswith(item):
                        skipthis = True
                if skipthis:
                    continue
                z = line.split()
                for item in z:
                    thelist.append(item)
            return thelist
        else:
            return None

    def getModuleList(self):
        tmp = self.getSysHelp('modules')
        if tmp:
            skips = 'Please wait', 'Enter any', 'for modules'
            self.modules = self.makeList(tmp, skips)
        return self.modules

    def getLicense(self):
        with open('LICENSE', 'r') as f:
            License = f.read()
        return License

    def getKeywordList(self):
        tmp = self.getSysHelp('keywords')
        if(tmp):
            skips = 'Here is'
            self.keywords = self.makeList(tmp, skips)
        return self.keywords

    def getSymbolList(self):
        tmp = self.getSysHelp('symbols')
        if(tmp):
            skips = 'Here is','to. Enter'
            self.symbols = self.makeList(tmp, skips)
        return self.symbols

    def getTopicsList(self):
        tmp = self.getSysHelp('topics')
        if(tmp):
            skips = 'Here is'
            self.topics = self.makeList(tmp, skips)
        return self.topics


    def getAllLists(self):
        self.getModuleList()
        self.getKeywordList()
        self.getSymbolList()
        self.getTopicsList()

        return self.modules, self.keywords, self.symbols, self.topics

if __name__ == '__main__':
    h = HarryHelp()
    modules = h.getModuleList()
    keywords = h.getKeywordList()
    symbols = h.getSymbolList()
    topics = h.getTopicsList()
    GNUlicense = h.getLicense()
    name = 'cmath'
    smodules, skeywords, ssymbols, stopics = h.getAllLists()
    h.getHelp(name)
    print(h.mhelp)
    print('\n=============================\n')
    h.getSource(name)
    print(h.source)
