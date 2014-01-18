
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
        return self.operator+"\n"+indent(str(self.left)+"\n"+str(self.right))

    @addToClass(AST.Fundef)
    def printTree(self):
        return "FUNDEF\n"+"\n".join([indent(str(el)) for el in [self.name, "RET "+self.return_type] + self.arguments]) + "\n" + indent(str(self.body))

    @addToClass(AST.Declaration)
    def printTree(self):
        return "DECL\n"+"\n".join([indent(str(init)) for init in self.inits])

    @addToClass(AST.Init)
    def printTree(self):
        return "=\n"+indent(str(self.name))+"\n"+indent(str(self.value))

    @addToClass(AST.CompoundInstruction)
    def printTree(self):
        return "\n".join([str(el) for el in self.decls + self.instrs])

    @addToClass(AST.Arg)
    def printTree(self):
        return "ARG " + str(self.id)

    @addToClass(AST.Const)
    def printTree(self):
        return str(self.value)

    @addToClass(AST.If)
    def printTree(self):
        out = "IF\n"+indent(str(self.condition)+"\n"+str(self.block_if))
        if self.block_else != None:
            out = out+"\n"+"ELSE\n"+indent(str(self.block_else))
        return out

    @addToClass(AST.Assignment)
    def printTree(self):
        return "=\n"+indent(str(self.id)+"\n"+str(self.expr))

    @addToClass(AST.Funcall)
    def printTree(self):
        return "FUNCALL\n"+indent("\n".join([str(el) for el in [self.name]+self.args]))

    @addToClass(AST.Print)
    def printTree(self):
        return "PRINT\n"+indent(str(self.expr))

    @addToClass(AST.Return)
    def printTree(self):
        return "RETURN\n"+indent(str(self.expr))

    @addToClass(AST.While)
    def printTree(self):
        return "WHILE\n"+indent("\n".join([str(el) for el in [self.condition, self.body]]))

    @addToClass(AST.Repeat)
    def printTree(self):
        return "REPEAT-UNTIL\n" + indent(str(self.condition)) + "\n" + indent("\n".join([str(el) for el in self.body]))

    @addToClass(AST.Break)
    def printTree(self):
        return "BREAK"

    @addToClass(AST.Continue)
    def printTree(self):
        return "CONTINUE"

    @addToClass(AST.LabeledInstr)
    def printTree(self):
        return "LABELED-INSTR\n" + indent(self.label) + "\n" + indent(str(self.instr))

    @addToClass(AST.Error)
    def printTree(self):
        return "ERROR"

    @addToClass(AST.Variable)
    def printTree(self):
        return self.name

    @addToClass(AST.AST)
    def printTree(self):
        return "\n".join([str(decl)   for decl   in p[1]]+
                         [str(fundef) for fundef in p[2]]+
                         [str(instr)  for instr  in p[3]])
