
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator



def indent(txt):
    return '\n'.join("| "+line for line in txt.splitlines())

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.BinExpr)
    def printTree(self):
        return "BinExpr"

    @addToClass(AST.Fundef)
    def printTree(self):
        return "Fundef"

    @addToClass(AST.Declaration)
    def printTree(self):
        return "DECL\n"+"\n".join([indent(init.__str__()) for init in self.inits])

    @addToClass(AST.Init)
    def printTree(self):
        return "=\n"+indent(self.name.__str__())+"\n"+indent(self.value.__str__())

    # @addToClass ...
    # ...
