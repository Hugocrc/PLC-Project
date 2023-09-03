import ply.lex as lex
import sys

reserved = {
    'int' : 'INT',
    'array' : 'ARRAY',
    'matrix' : 'MATRIX',
    'sum' : 'SUM',
    'subtrac' : 'SUBTRAC',
    'mult' : 'MULT',
    'div' : 'DIV',
    'rem' : 'REM',
    'gt' : 'GT',
    'lt' : 'LT',
    'gte' : 'GTE',
    'lte' : 'LTE',
    'equals' : 'EQUALS',
    'notequals' : 'NOTEQUALS',
    'not' : 'NOT',
    'and' : 'AND',
    'or' : 'OR',
    'write' : 'WRITE',
    'read' : 'READ',
    'while' : 'WHILE',
    'do' : 'DO',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'close' : 'CLOSE'
}


tokens = [
        'NUM',
        'NAME'
] + list(reserved.values())


literals = ['=', '(', ')', '[', ']', ';', ',']


def t_NUM(t):
    r'\d+'
    t.type = "NUM"
    return t


def t_ID(t):
    r'[a-zA-Z]+'
    t.type = reserved.get(t.value, 'NAME')
    return t
    

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def lexer_build():
    lexer = lex.lex()
    return lexer

