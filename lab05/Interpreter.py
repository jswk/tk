
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class Interpreter(object):

    binary_operations = {
        '+': (lambda x, y: x + y),
        '-': (lambda x, y: x - y),
        '*': (lambda x, y: x * y),
        '/': (lambda x, y: x / y),
        '<': (lambda x, y: 1 if x < y else 0),
        '<=': (lambda x, y: 1 if x <= y else 0),
        '==': (lambda x, y: 1 if x == y else 0),
        '>': (lambda x, y: 1 if x > y else 0),
        '>=': (lambda x, y: 1 if x >= y else 0),
        '!=': (lambda x, y: 1 if x != y else 0),
        '&&': (lambda x, y: 1 if x and y else 0),
        '||': (lambda x, y: 1 if x or y else 0),
        '<<': (lambda x, y: x << y),
        '>>': (lambda x, y: x >> y),
        '|': (lambda x, y: x | y),
        '&': (lambda x, y: x & y),
        '^': (lambda x, y: x ^ y),
        '%': (lambda x, y: x % y)
    }

    def __init__(self):
        self.memory_stack = MemoryStack(Memory('global'))

    @on('node')
    def visit(self, node):
        pass

    @when(AST.AST)
    def visit(self, node):
        for declaration in node.decl:
            declaration.accept666(self)
        for fundef in node.fundef:
            fundef.accept666(self)
        for instruction in node.instr:
            instruction.accept666(self)

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept666(self)
        r2 = node.right.accept666(self)

        return Interpreter.binary_operations[node.operator](r1, r2)

    @when(AST.Declaration)
    def visit(self, node):
        for init in node.inits:
            init.accept666(self)

    @when(AST.Init)
    def visit(self, node):
        value = node.value.accept666(self)
        self.memory_stack.put(node.name.name, value)

    @when(AST.CompoundInstruction)
    def visit(self, node):
        for declaration in node.decls:
            declaration.accept666(self)
        for instruction in node.instrs:
            instruction.accept666(self)

    @when(AST.LabeledInstr)
    def visit(self, node):
        node.instr.accept666(self)

    @when(AST.Assignment)
    def visit(self, node):
        value = node.expr.accept666(self)
        self.memory_stack.put(node.id.name, value)

    @when(AST.Fundef)
    def visit(self, node):
        self.memory_stack.put(node.name, node)

    @when(AST.Funcall)
    def visit(self, node):
        function = self.memory_stack.get(node.name.name)
        memory = Memory(function.name)
        self.memory_stack.push(memory)
        # evaluate argument values
        # zip reduce ftw
        pairs = zip(function.arguments, node.args)
        for pair in pairs:
            name = pair[0].id
            value = pair[1].accept666(self)
            self.memory_stack.put(name, value)

        returned_value = None
        try:
            function.body.accept666(self)
        except ReturnException, e:
            returned_value = e.value
        self.memory_stack.pop()
        return returned_value

    @when(AST.Variable)
    def visit(self, node):
        value = self.memory_stack.get(node.name)
        return value

    @when(AST.Print)
    def visit(self, node):
        expression_value = node.expr.accept666(self)
        print(expression_value)

    @when(AST.Const)
    def visit(self, node):
        return node.value

    # This stuff needs to be here, otherwise visitor implementation returns list containing value of AST.Const.visit instead of single number
    @when(AST.Integer)
    def visit(self, node):
        return node.value

    @when(AST.Float)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value[1:-1] # Trim quotes


    @when(AST.If)
    def visit(self, node):
        shall_you_pass = node.condition.accept666(self) != 0
        if not shall_you_pass:
            # run you fools!
            if node.block_else is not None:
                node.block_else.accept666(self)
        else:
            node.block_if.accept666(self)

    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        while node.condition.accept666(self) != 0:
            try:
                node.body.accept666(self)
            except(BreakException):
                return None
            except(ContinueException):
                pass

    @when(AST.Repeat)
    def visit(self, node):
        try:
            try:
                node.body.accept666(self)
            except(ContinueException):
                pass
            while node.condition.accept666(self) == 0:
                try:
                    node.body.accept666(self)
                except(ContinueException):
                    pass
        except(BreakException):
            pass

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Return)
    def visit(self, node):
        value = node.expr.accept666(self)
        raise ReturnException(value)
