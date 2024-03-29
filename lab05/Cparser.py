#!/usr/bin/python

from scanner import Scanner
import AST



class Cparser(object):


    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print('At end of input\nMost likely you haven\'t included a single instruction')


    def p_program(self, p):
        """program : declarations fundefs instructions"""
        p[0] = AST.AST(p[1], p[2], p[3])


    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        try:
            p[0] = p[1] + [p[2]]
        except IndexError:
            p[0] = []


    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        try:
            p[3]
            p[0] = AST.Declaration(p[1], p[2])
        except IndexError:
            p[0] = AST.Error(p[1])


    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        try:
            p[0] = p[1] + [p[3]]
        except IndexError:
            p[0] = [p[1]]


    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = self.add_pos(AST.Init(self.add_pos(AST.Variable(p[1]), p), p[3]), p)


    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        try:
            p[0] = p[1] + [p[2]]
        except IndexError:
            p[0] = [p[1]]


    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr"""
        p[0] = p[1]


    def p_print_instr(self, p):
        """print_instr : PRINT expression ';'
                       | PRINT error ';' """
        p[0] = AST.Print(p[2])


    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = AST.LabeledInstr(p[1], p[3])


    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AST.Assignment(self.add_pos(AST.Variable(p[1]), p), p[3])


    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        try:
          p[0] = AST.If(p[3], p[5], p[7])
        except IndexError:
          p[0] = AST.If(p[3], p[5], None)


    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.While(p[3], p[5])


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instruction UNTIL condition ';' """
        p[0] = AST.Repeat(p[2], p[4])


    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = self.add_pos(AST.Return(p[2]), p)


    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = self.add_pos(AST.Continue(), p)


    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = self.add_pos(AST.Break(), p)


    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions '}' """
        p[0] = AST.CompoundInstruction(p[2], p[3])


    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]


    def p_const_int(self, p):
        """const : INTEGER"""
        p[0] = self.add_pos(AST.Integer(p[1]), p)

    def p_const_float(self, p):
        """const : FLOAT"""
        p[0] = self.add_pos(AST.Float(p[1]), p)

    def p_const_string(self, p):
        """const : STRING"""
        p[0] = self.add_pos(AST.String(p[1]), p)


    def p_expression_simple(self, p):
        """expression : const
                      | '(' expression ')' """
        try:
            p[0] = p[2]
        except IndexError:
            p[0] = p[1]

    def p_expression_id(self, p):
        """expression : ID """
        p[0] = self.add_pos(AST.Variable(p[1]), p)

    def p_expression_binexpr(self, p):
        """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression """
        p[0] = self.add_pos(AST.BinExpr(p[1], p[2], p[3]), p)

    def p_expression_funcall(self, p):
        """expression : ID '(' expr_list_or_empty ')' """
        p[0] = self.add_pos(AST.Funcall(self.add_pos(AST.Variable(p[1]), p), p[3]), p)

    def p_expression_error(self, p):
        """expression : '(' error ')'
                      | ID '(' error ')' """
        pos = self.get_pos(p, 1)
        try:
            p[4]
            p[0] = AST.Error("Malformed function call {0}({1}) at line:{2} column:{3}".format(p[1], p[3], pos[0], pos[1]))
        except IndexError:
            p[0] = AST.Error("Malformed braced expression ({0}) at line:{1} column:{2}".format(p[2], pos[0], pos[1]))


    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        try:
            p[0] = p[1]
        except IndexError:
            p[0] = []


    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        try:
            p[0] = p[1] + [p[3]]
        except IndexError:
            p[0] = [p[1]]


    def p_fundefs(self, p):
        """fundefs : fundef fundefs
                   |  """
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = []

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = self.add_pos(AST.Fundef(p[2], p[1], p[4], p[6]), p)

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        try:
          p[0] = p[1]
        except IndexError:
          p[0] = []

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        try:
          p[0] = p[1] + [p[3]]
        except IndexError:
          p[0] = [p[1]]

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = self.add_pos(AST.Arg(p[1], p[2]), p)

    def add_pos(self, el, p, i = 1):
        el.pos = self.get_pos(p, i)
        return el

    def get_pos(self, p, i = 1):
        def find_column(input,token):
            last_cr = input.rfind('\n',0,token)
            if last_cr < 0:
                last_cr = 0
            column = (token - last_cr)
            return column
        try:
            out = p[i].pos
        except AttributeError:
            out = (p.lineno(i), find_column(self.scanner.lexer.lexdata, p.lexpos(i)))
        # print("{}:{} -> {}:{}".format(p.slice, i, out[0], out[1]))
        return out



