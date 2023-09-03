import ply.yacc as yacc
from lexer import tokens
from lexer import lexer_build
import sys


start = 'Program'


def p_Program_Decls(p):
    'Program : Decls Body'
    p[0] = p[1] + "START\n" + p[2] + "STOP\n"


def p_Program_noDecls(p):
    'Program : Body'
    p[0] = "START\n" + p[1] + "STOP\n"


def p_Decls_multiple(p):
    'Decls : Decls Decl'
    p[0] = p[1] + p[2]


def p_Decls_single(p):
    'Decls : Decl'
    p[0] = p[1]


def p_Decl_Int(p):
    "Decl : INT NAME ';'"
    if p[2] not in p.parser.fp:
        p.parser.fp.update({p[2]: p.parser.gp})
        p[0] = "PUSHI 0\n"
        p.parser.gp += 1
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[2]} already declared!")
        raise SyntaxError


def p_Decl_Array(p):
    "Decl : ARRAY '[' NUM ']' NAME ';'"
    if p[5] not in p.parser.fp:
        p.parser.fp.update({p[5]: (p.parser.gp, int(p[3]))})
        p[0] = f"PUSHN {p[3]}\n"
        p.parser.gp += int(p[3])
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[5]} already declared!")
        raise SyntaxError


def p_Decl_Matrix(p):
    "Decl : MATRIX '[' NUM ']' '[' NUM ']' NAME ';'"
    if p[8] not in p.parser.fp:
        p.parser.fp.update({p[8]: (p.parser.gp, int(p[3]), int(p[6]))})
        n = int(p[3]) * int(p[6])
        p[0] = f"PUSHN {str(n)}\n"
        p.parser.gp += n
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[8]} already declared!")
        raise SyntaxError


def p_Body_multiple(p):
    'Body : Body Process'
    p[0] = p[1] + p[2]


def p_Body_single(p):
    'Body : Process'
    p[0] = p[1]


def p_Process(p):
    '''Process : Ite
               | WhileLoop
               | Write
               | Assign'''
    p[0] = p[1]


def p_Ite_then(p):
    'Ite : IF condition THEN Body CLOSE'
    p[0] = p[2] + f'JZ l{p.parser.labels}\n' + p[4] + f'l{p.parser.labels}: NOP\n'
    p.parser.labels += 1


def p_Ite_then_else(p):
    'Ite : IF condition THEN Body ELSE Body CLOSE'
    p[0] = p[2] + f'JZ l{p.parser.labels}\n' + p[4] + f'JUMP l{p.parser.labels}f\nl{p.parser.labels}: NOP\n' + p[6] + f'l{p.parser.labels}f: NOP\n'
    p.parser.labels += 1


def p_WhileLoop(p):
    'WhileLoop : WHILE condition DO Body CLOSE'
    p[0] = f'l{p.parser.labels}c: NOP\n' + p[2] + f'JZ l{p.parser.labels}f\n' + p[4] + f'JUMP l{p.parser.labels}c\nl{p.parser.labels}f: NOP\n'
    p.parser.labels += 1


def p_Write_var(p):
    "Write : WRITE NAME ';'"
    if p[2] in p.parser.fp:
        var = p.parser.fp.get(p[2])

        if type(var) == tuple:
            if len(var) == 2:
                array = f'PUSHS "[ "\nWRITES\n'
                for i in range(var[1]):
                    array += f'PUSHGP\nPUSHI {var[0]}\nPADD\nPUSHI {i}\nLOADN\nWRITEI\nPUSHS " "\nWRITES\n'
                array += f'PUSHS "]"\nWRITES\n'
                p[0] = array + 'PUSHS "\\n"\nWRITES\n'

            elif len(var) == 3:
                matrix = ""
                for i in range(var[1]):
                    matrix += f'PUSHS "[ "\nWRITES\n'
                    for j in range(var[2]):
                        matrix += f'PUSHGP\nPUSHI {var[0]}\nPADD\nPUSHI {var[2] * i + j}\nLOADN\nWRITEI\nPUSHS " "\nWRITES\n'
                    matrix += 'PUSHS "]\\n"\nWRITES\n'
                p[0] = matrix

        else:
            p[0] = f'PUSHG {p.parser.fp.get(p[2])}\nWRITEI\nPUSHS "\\n"\nWRITES\n'

    else:
        print(f"Error, line {p.lineno(2)}: variable {p[2]} does not exists!")
        raise SyntaxError


def p_Write_Expr(p):
    "Write : WRITE Expr ';'"
    p[0] = p[2] + 'WRITEI\nPUSHS "\\n"\nWRITES\n'


def p_Assign_Matrix(p):
    "Assign : NAME '[' Expr ']' '[' Expr ']' '=' Expr ';'"
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 3:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n{p[3]}PUSHI {var[2]}\nMUL\n{p[6]}ADD\n{p[9]}STOREN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Matrix.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assign_Read_Matrix(p):
    "Assign : NAME '[' Expr ']' '[' Expr ']' '=' READ ';'"
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 3:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + f'PUSHI {var[2]}\nMUL\n' + p[6] + f'ADD\nREAD\nATOI\nSTOREN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Matrix.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assign_Array(p):
    "Assign : NAME '[' Expr ']' '=' Expr ';'"
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 2:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + p[6] + 'STOREN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Array.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assign_Read_Array(p):
    "Assign : NAME '[' Expr ']' '=' READ ';'"
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 2:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + f'READ\nATOI\nSTOREN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Array.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assign_Expr(p):
    "Assign : NAME '=' Expr ';'"
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if type(var) == int:
            p[0] = p[3] + f'STOREG {var}\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Int.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assign_Read(p):
    "Assign : NAME '=' READ ';'"
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if type(var) == int:
            p[0] = f'READ\nATOI\nSTOREG {var}\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Int.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_condition_gt(p):
    "condition : GT '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'SUP\n'


def p_condition_gte(p):
    "condition : GTE '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'SUPEQ\n'


def p_condition_lt(p):
    "condition : LT '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'INF\n'


def p_condition_lte(p):
    "condition : LTE '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'INFEQ\n'


def p_condition_equals(p):
    "condition : EQUALS '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'EQUAL\n'


def p_condition_notequals(p):
    "condition : NOTEQUALS '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'EQUAL\nNOT\n'


def p_condtion_not(p):
    "condition : NOT '(' Expr ')'"
    p[0] = p[3] + 'NOT\n'


def p_condition_and(p):
    "condition : AND '(' condition ',' condition ')'"
    p[0] = p[3] + p[5] + 'ADD\nPUSHI 2\nEQUAL\n'


def p_condition_or(p):
    "condition : OR '(' condition ',' condition ')'"
    p[0] = p[3] + p[5] + 'ADD\nPUSHI 1\nSUPEQ\n'


def p_condition_base(p):
    "condition : '(' condition ')'"
    p[0] = p[2]


def p_Expr_condition(p):
    'Expr : condition'
    p[0] = p[1]


def p_Expr_Num(p):
    'Expr : NUM'
    p[0] = f'PUSHI {p[1]}\n'


def p_Expr_Var(p):
    'Expr : Var'
    p[0] = p[1]


def p_Expr_sum(p):
    "Expr : SUM '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'ADD\n'


def p_Expr_subtrac(p):
    "Expr : SUBTRAC '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'SUB\n'


def p_Expr_mult(p):
    "Expr : MULT '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'MUL\n'


def p_Expr_div(p):
    "Expr : DIV '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'DIV\n'


def p_Expr_rem(p):
    "Expr : REM '(' Expr ',' Expr ')'"
    p[0] = p[3] + p[5] + 'MOD\n'


def p_Expr_base(p):
    "Expr : '(' Expr ')'"
    p[0] = p[2]


def p_Var_Int(p):
    'Var : NAME'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if type(var) == int:
            p[0] = f'PUSHG {var}\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Int.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} doesn't exists.")
        raise SyntaxError


def p_Var_Array(p):
    "Var : NAME '[' Expr ']'"
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 2:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + 'LOAD\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Array.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} doesn't exists.")
        raise SyntaxError


def p_Var_Matrix(p):
    "Var : NAME '[' Expr ']' '[' Expr ']'"
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 3:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + f'PUSHI {var[2]}\nMUL\n' + p[6] + 'ADD\nLOADN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Matrix.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} doesn't exists.")
        raise SyntaxError


def p_error(p):
    print(f"Syntax error: token {p.value} on line {p.lineno}.")


def build_parser():
    lexer_build()
    parser = yacc.yacc()
    parser.fp = dict()
    parser.labels = 0
    parser.gp = 0

    return parser