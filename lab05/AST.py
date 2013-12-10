
class Node(object):

    def __str__(self):
        return self.printTree()


class Const(Node):
    pass


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):
    pass


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

# ...


