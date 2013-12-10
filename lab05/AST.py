
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
    pass 


# ...


