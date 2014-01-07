#!/usr/bin/python



class TypeChecker(object):

    ttype = {}

    ttype[('+', 'int', 'int')] = 'int'
    ttype[('-', 'int', 'int')] = 'int'
    ttype[('*', 'int', 'int')] = 'int'
    ttype[('/', 'int', 'int')] = 'int'
    ttype[('%', 'int', 'int')] = 'int'
    ttype[('^', 'int', 'int')] = 'int'
    ttype[('|', 'int', 'int')] = 'int'
    ttype[('&', 'int', 'int')] = 'int'
    ttype[('<', 'int', 'int')] = 'int'    
    ttype[('>', 'int', 'int')] = 'int'    
    ttype[('<=', 'int', 'int')] = 'int'    
    ttype[('>=', 'int', 'int')] = 'int'
    ttype[('==', 'int', 'int')] = 'int'
    ttype[('!=', 'int', 'int')] = 'int'
    ttype[('>>', 'int', 'int')] = 'int'
    ttype[('<<', 'int', 'int')] = 'int'
    ttype[('&&', 'int', 'int')] = 'int'
    ttype[('||', 'int', 'int')] = 'int'

    ttype[('+', 'float', 'float')] = 'float'
    ttype[('-', 'float', 'float')] = 'float'
    ttype[('*', 'float', 'float')] = 'float'
    ttype[('/', 'float', 'float')] = 'float'
    ttype[('<', 'float', 'float')] = 'int'
    ttype[('>', 'float', 'float')] = 'int'
    ttype[('<=', 'float', 'float')] = 'int'
    ttype[('>=', 'float', 'float')] = 'int'
    ttype[('==', 'float', 'float')] = 'int'
    ttype[('!=', 'float', 'float')] = 'int'

    ttype[('+', 'float', 'int')] = 'float'
    ttype[('-', 'float', 'int')] = 'float'
    ttype[('*', 'float', 'int')] = 'float'
    ttype[('/', 'float', 'int')] = 'float'
    ttype[('+', 'int', 'float')] = 'float'
    ttype[('-', 'int', 'float')] = 'float'
    ttype[('*', 'int', 'float')] = 'float'
    ttype[('/', 'int', 'float')] = 'float'

    ttype[('<', 'float', 'int')] = 'int'
    ttype[('>', 'float', 'int')] = 'int'
    ttype[('<=', 'float', 'int')] = 'int'
    ttype[('>=', 'float', 'int')] = 'int'
    ttype[('==', 'float', 'int')] = 'int'
    ttype[('!=', 'float', 'int')] = 'int'
    ttype[('<', 'int', 'float')] = 'int'
    ttype[('>', 'int', 'float')] = 'int'
    ttype[('<=', 'int', 'float')] = 'int'
    ttype[('>=', 'int', 'float')] = 'int'
    ttype[('==', 'int', 'float')] = 'int'
    ttype[('!=', 'int', 'float')] = 'int'

    ttype[('+', 'string', 'string')] = 'string'
    ttype[('*', 'string', 'int')] = 'string'
    ttype[('<', 'string', 'string')] = 'int'
    ttype[('>', 'string', 'string')] = 'int'
    ttype[('<=', 'string', 'string')] = 'int'
    ttype[('>=', 'string', 'string')] = 'int'
    ttype[('!=', 'string', 'string')] = 'int'
    ttype[('==', 'string', 'string')] = 'int'

    tconv = {}
    tconv[('int', 'float')] = True

    def __init__(self):
        self.scope = SymbolTable(None, 'global')
        
    def visit_BinExpr(self, node):
        type1 = node.left.accept(self)
        type2 = node.right.accept(self)
        op    = node.op;
        if type1 is None or type2 is None:
            return None

        try:
            return ttype[(op, type1, type2)]
        except(KeyError):
            print("Cannot evaluate {0} {1} {2} - incompatible types".format(type1, op, type2) 
            return None

    def visit_Fundef(self, node):
        if scope.getDirect(node.name) is None:
            self.scope.put(node.name, node)
        else:
            print("Symbol {0} already defined".format(node.name))

    def visit_Funcall(self, node):
        function = self.scope.get(node.name)
        if function is None:
            print("Function {0} does not exist".format(function.name))
            return None
        # zip reduce
 
    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'


