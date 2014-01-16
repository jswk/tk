#!/usr/bin/python

class Symbol(object):
    pass
    # TODO: Remove

class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymbolTable(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        try:
            return self.symbols[name]
        except(KeyError):
            if self.parent is not None:
                return self.parent.get(name)

    def getDirect(self, name):
        return self.symbols.get(name)

    def getParentScope(self):
        return self.parent





