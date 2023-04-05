import ply.lex as lex

#Tokens
tokens = [
  'PLUS',
  'MINUS',
  'DIVIDE',
  'MULTIPLY',
  'ASSIGNMENT',
  'DIFFERENT',
  'EOF',
  'LP',
  'RP',
  'OBR',
  'CBR',
  'COMMA',
  'EQUAL',
  'GT',
  'GET',
  'LT',
  'LET',
  'NOTES',
]


#Reserved words
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
  'char' : 'CHAR',
  'bool' : 'BOOL',
  'and' : 'AND',
  'or' : 'OR',
  'input' : 'INPUT',
  'output' : 'OUTPUT',
  'true' : 'TRUE',
  'false' : 'FALSE',
}


# Define regular expressions for each token
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_MULTIPLY = r'\*'
t_ASSIGNMENT = r'='
t_DIFFERENT = r'!='
t_EOF = r';'
t_LP = r'\('
t_RP = r'\)'
t_OBR = r'\{'
t_CBR = r'\}'
t_COMMA = r','
t_EQUAL = r'=='
t_GT = r'>'
t_GET = r'>='
t_LT = r'<'
t_LET = r'<='
t_NOTES = r'//'
t_INT = r'\d+'
t_DEC = r'\d+\.\d+'
#t_STRING = r'\"([^\\\"]|\\.)*\"'
t_STRING = r'^\"[^\"]*\"$'


# Define any required helper functions
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Create the lexer
lexer = lex.lex()

# Test the lexer
lexer.input('3 + 4 * 2 - 1')
for token in lexer:
    print(token)
