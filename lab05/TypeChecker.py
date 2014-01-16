#!/usr/bin/python
from SymbolTable import SymbolTable, VariableSymbol

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
        if type(node.left) == str:
            type1 = self.scope.get(node.left).accept(self)
        else:
            type1 = node.left.accept(self)

        if type(node.right) == str:
            type1 = self.scope.get(node.right).accept(self)
        else:
            type2 = node.right.accept(self)
        op = node.operator
        if type1 is None or type2 is None:
            return None

        try:
            return ttype[(op, type1, type2)]
        except(KeyError):
            print("Cannot evaluate {0} {1} {2} - incompatible types".format(type1, op, type2))
        return None

    def visit_If(self, node):
        condition_type = node.condition.accept(self)
        if condition_type != 'int':
            print("Condition must evaluate to integer")
        node.block_if.accept(self)
        node.block_else.accept(self)

    def visit_Fundef(self, node):
        if self.scope.getDirect(node.name) is None:
            self.scope.put(node.name, node)
        else:
            print("Symbol {0} already defined".format(node.name))

        # Create new scope for function
        self.scope = SymbolTable(self.scope, node.name)
        for argument in node.arguments:
            argument.accept(self)
        node.body.accept(self)

        # Get the hell out of function scope, after its done
        self.scope = self.scope.parent
        
    def visit_Arg(self, node):
        self.scope.put(node.id, node)

    def visit_CompoundInstruction(self, node):
        for declaration in node.decls:
            declaration.accept(self)
        for instruction in node.instrs:
            print(type(instruction))
            instruction.accept(self)

    def visit_Funcall(self, node):
        print("Visiting function")
        function = self.scope.get(node.name)
        if function is None:
            print("Function {0} does not exist".format(function.name))
            return None
        
        if len(function.arguments) != len(node.args):
            print("Incorrect number of arguments. {0} requires {1}, {2} provided".format(function.name, len(function.arguments), len(node.args)))
            return None
        # zip reduce
 
    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_AST(self, node):
        for fundef in node.fundef:
            fundef.accept(self)
        for instr in node.instr:
            instr.accept(self)
        
