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

    @staticmethod
    def conversion_possible(type1, type2):
        return TypeChecker.tconv.get((type1, type2)) is not None

    def get_value_scoped(self, value):
        '''
        Sometimes we have strings as nodes.
        It means they are symbol ids, so we have
        to retrieve it from our scope then.
        '''
        return self.scope.get(value) if type(value) == str else value

    def __init__(self):
        self.scope = SymbolTable(None, 'global')

    def visit_BinExpr(self, node):
        type1 = type2 = None

        type1 = node.left.accept(self)

        type2 = node.right.accept(self)

        op = node.operator

        if type1 is None or type2 is None:
            return None

        try:
            return TypeChecker.ttype[(op, type1, type2)]
        except(KeyError):
            print("Cannot evaluate {0} {1} {2} - incompatible types".format(type1, op, type2))
        return None

    def visit_Variable(self, node):
        value = self.scope.get(node.name)

        if value != None:
            return value.type
        else:
            print("Undefined variable {0} at {1}:{2}".format(node.name, node.pos[0], node.pos[1]))
            return None


    def visit_If(self, node):
        condition_type = node.condition.accept(self)
        if condition_type != 'int':
            print("Condition must evaluate to integer at {0}:{1}".format(node.condition.pos[0], node.condition.pos[1]))
        node.block_if.accept(self)
        if node.block_else != None:
            node.block_else.accept(self)

    def visit_While(self, node):
        condition_type = node.condition.accept(self)
        if condition_type != 'int':
            print("Condition must evaluate to integer")
        node.body.accept(self)

    def visit_Repeat(self, node):
        condition_type = node.condition.accept(self)
        if condition_type != 'int':
            print("Condition must evaluate to integer")
        node.body.accept(self)

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
        return node.type

    def visit_Declaration(self, node):
        for init in node.inits:
            init.type = node.type
            self.scope.put(init.name.name, init.value)
            init_type = init.accept(self)
            if init_type != node.type and not TypeChecker.conversion_possible(init_type, node.type):
                print("Cannot convert {0} to {1} at {2}:{3}".format(init_type, node.type, init.pos[0], init.pos[1]))

    def visit_Init(self, node):
        declaration = self.scope.get(node.name.name)
        if declaration is None:
            print("Undefined variable {0} at {1}:{2}".format(node.name, node.name.pos[0], node.name.pos[1]))
            return None

        value_type = node.value.accept(self)
        return value_type

    def visit_CompoundInstruction(self, node):
        for declaration in node.decls:
            declaration.accept(self)
        for instruction in node.instrs:
            instruction.accept(self)

    def visit_Funcall(self, node):
        function = self.scope.get(node.name.name)

        if function is None:
            print("Function {0} does not exist at {1}:{2}".format(node.name, node.name.pos[0], node.name.pos[1]))
            return None
        elif function.type != "function":
            print("Cannot call as function an ordinary variable {0} at {1}:{2}".format(node.name, node.name.pos[0], node.name.pos[1]))
            return None

        if len(function.arguments) != len(node.args):
            print("Incorrect number of arguments. {0} requires {1}, {2} provided at {3}:{4}".format(function.name, len(function.arguments), len(node.args), node.pos[0], node.pos[1]))
            return None

        # zip reduce because map reduce is for suckers
        arg_pairs = zip(node.args, function.arguments)
        for pair in arg_pairs:
            passed_argument = self.get_value_scoped(pair[0])
            defined_argument = pair[1]
            if passed_argument is None:
                print("Undefined variable {0}".format(pair[0]))
                return None
            passed_argument_type = passed_argument.accept(self)
            if passed_argument_type != defined_argument.type and not TypeChecker.conversion_possible(passed_argument_type, defined_argument.type):
                print("Cannot convert {0} to {1} at {2}:{3}".format(passed_argument_type, defined_argument.type, passed_argument.pos[0], passed_argument.pos[1]))
                return None
        return function.return_type

    def visit_Assignment(self, node):
        variable = self.scope.get(node.id.name)
        if variable is None:
            print("Undefined variable {0} at {1}:{2}".format(node.id, node.id.pos[0], node.id.pos[1]))
            return None
        elif variable.type == "function":
            print("Cannot assign to function {0} at {1}:{2}".format(node.id, node.id.pos[0], node.id.pos[1]))

        expression_node = self.get_value_scoped(node.expr)

        if expression_node is None:
            print("Undefined variable {0}".format(node.id))
            return None

        assigned_type = expression_node.accept(self)
        if assigned_type is None:
            return None

        if assigned_type != variable.type and not TypeChecker.conversion_possible(assigned_type, variable.type):
            print("Cannot assign {0} to {1} at {2}:{3}".format(assigned_type, variable.type, node.id.pos[0], node.id.pos[1]))
            return None
        return assigned_type

    # def visit_Return(self, node):
    #     if not self.funcall:
    #         print("Return must be used inside a function")

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_AST(self, node):
        for decl in node.decl:
            decl.accept(self)
        for fundef in node.fundef:
            fundef.accept(self)
        for instr in node.instr:
            instr.accept(self)

