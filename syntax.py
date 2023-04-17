import ply.yacc as yacc
from lexer import tokens

def p_programa(p):
    ''' programa : BEGIN OPAREN ID CPAREN bloque'''
#Manejo de error sintactico
def p_error(p):
    print("ERROR: Error de sintaxis: '%s'" % p.value)
    exit()

yacc.yacc()

#Probar Archivo
try:
    f = open('../Compilador/test/prueba1.dua')
    data = f.read()
    f.close()
except EOFError:
    quit()

yacc.parse(data)
print("CÓDIGO CORRECTO")