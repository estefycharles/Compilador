import ply.lex as lex

#Tokens
tokens = [
  'PLUS',
  'MINUS',
  'DIVIDE',
  'MULTIPLY',
# 'EXP',
  'ASSIGNMENT',
  'EOF',
  'MONEY',
  'COLON',
  'OPAREN',
  'CPAREN',
  'OBRACKET',
  'CBRACKET',
  'OSQUAREBR',
  'CSQUAREBR',
  'COMMA',
  'EQUAL',
  'DIFFERENT',
  'GREATERTHAN',
  'GREATERTHANEQ',
  'LESSTHAN',
  'LESSTHANEQ',
  'ID',
]

#Palabras reservadas
reserved = {
  'begin' : 'BEGIN',
  'end' : 'END',
  'fx' : 'FX',
  'return' : 'RETURN',
  'void' : 'VOID',
  'var' : 'VAR',
  'int' : 'INT',
  'dec' : 'DEC',
  'string' : 'STRING',
  'bool' : 'BOOL',
  #'and' : 'AND',
  #'or' : 'OR',
  'input' : 'INPUT',
  'output' : 'OUTPUT',
  #'for': 'FOR',
  'if': 'IF',
  'else': 'ELSE',
  #'do': 'DO',
  'while': 'WHILE',
  'main' : 'MAIN',
  'class' : 'CLASS',
  'methods' : 'METHODS',
  'attributes' : 'ATTRIBUTES'
}

t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_MULTIPLY = r'\*'
t_ASSIGNMENT = r'\='
t_EOF = r'\;'
t_MONEY = r'\$'
t_COLON = r'\:'
t_OPAREN = r'\('
t_CPAREN = r'\)'
t_OBRACKET = r'\{'
t_CBRACKET = r'\}'
t_OSQUAREBR = r'\['
t_CSQUAREBR = r'\]'
t_COMMA = r','
#t_EQUAL = r'=='
t_DIFFERENT = r'!='
t_GREATERTHAN = r'>'
t_GREATERTHANEQ = r'>='
t_LESSTHAN = r'<'
t_LESSTHANEQ = r'<='

tokens = tokens + list(reserved.values())

#Expresiones Regulares
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_EQUAL(t):
    r'=='
    return t

def t_BOOL(t):
    r'True|False'
    t.type = reserved.get(t.value, 'BOOL')
    if t.value == 'False':
        t.value=0
    t.value = bool(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.type = reserved.get(t.value, 'STRING')
    t.value = (t.value, 'string')
    return t

def t_DEC(t):
     r'[0-9]+\.[0-9]+'
     t.type = reserved.get(t.value, 'DEC')
     t.value = float(t.value)    
     return t

def t_INT(t):
     r'[0-9]+'
     t.type = reserved.get(t.value, 'INT')
     t.value = int(t.value)    
     return t

def t_notes(t):
    r'//(.)*?\n'
    t.lexer.lineno += 1

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)

t_ignore  = ' \t'
 
#Manejo de error lexico
def t_error(t):
     print("ERROR: Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

lexer = lex.lex()

#Leer archivo
f = open('../Compilador/test/prueba1.dua')
data = f.read()
f.close()
lexer.input(data)
for token in lexer:
   print(token)