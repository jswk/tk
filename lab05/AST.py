
class Node(object):

    def accept(self, visitor):
        className = self.__class__.__name__
        method = getattr(visitor, 'visit_' + className, None)
        if method != None:
            return method(self)

    def __str__(self):
        return self.printTree()


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    def __init__(self, value):
        Const.__init__(self, int(value))


class Float(Const):
    def __init__(self, value):
        Const.__init__(self, float(value))


class String(Const):
    pass


class Arg(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id

class BinExpr(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Fundef(Node):
    def __init__(self, name, return_type, arguments, body):
        self.name = name
        self.return_type = return_type
        self.arguments = arguments
        self.body = body

class Funcall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits

class Init(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class If(Node):
    def __init__(self, condition, block_if, block_else):
        self.condition = condition
        self.block_if = block_if
        self.block_else = block_else

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Repeat(Node):
    def __init__(self, body, until):
        self.body = body
        self.until = until

class Error(Node):
    def __init__(self, message):
        self.message = message

class CompoundInstruction(Node):
    def __init__(self, decls, instrs):
        self.decls = decls
        self.instrs = instrs

class Assignment(Node):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

class Print(Node):
    def __init__(self, expr):
        self.expr = expr

class LabeledInstr(Node):
    def __init__(self, label, instr):
        self.label = label
        self.instr = instr

class Return(Node):
    def __init__(self, expr):
        self.expr = expr

class Continue(Node):
    pass

class Break(Node):
    pass

class AST(Node):
    def __init__(self, decl, fundef, instr):
        self.decl = decl
        self.fundef = fundef
        self.instr = instr

# ...


