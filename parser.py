import ply.yacc as yacc
from lexer import tokens

def p_begin(p):
    ''' begin : BEGIN OPAREN ID CPAREN bloque main end '''
    pass

def p_main(p):
    ''' main : MAIN OPAREN CPAREN OBRACKET bloque CBRACKET '''
    pass

def p_bloque(p):
    ''' bloque : declaracionVarAux estatutoAux
                | estatutoAux  '''
    pass

def p_declaracionVarAux(p):
    ''' declaracionVarAux : declaracionVar 
                        | declaracionVarAux declaracionVarAux'''
    pass 

def p_declaracionVar(p):
    ''' declaracionVar : VAR vars '''
    pass

def p_vars(p):
    ''' vars : tipo var EOF '''
    pass

def p_var(p):
    ''' var : ID 
            | ID COMMA var '''
    pass

def p_tipo(p):
    ''' tipo : INT
            | DEC
            | STRING
            | BOOL '''
    pass

def p_estatutoAux(p):
    ''' estatutoAux : estatuto 
                    | estatutoAux estatutoAux'''
    pass

def p_estatuto(p):
    ''' estatuto : asignacion
                | funcion
                | epsilon '''
    pass 

def p_funcion(p):
    ''' funcion : VOID FX ID OPAREN parametros CPAREN OBRACKET bloque CBRACKET 
                | tipo FX ID OPAREN parametros CPAREN OBRACKET bloque return CBRACKET '''
    pass

def p_return(p):
    ''' return : RETURN ID EOF '''

def p_parametros(p):
    ''' parametros : tipo ID
                    | tipo ID COMMA parametros
                    | epsilon '''

def p_asignacion(p):
    ''' asignacion : ID ASSIGNMENT expresion EOF '''
    pass

def p_expresion(p):
    ''' expresion : exp'''
    pass

def p_exp(p):
    ''' exp : termino 
            | termino PLUS exp
            | termino MINUS exp '''
    pass

def p_termino(p):
    ''' termino : factor
                | factor MULTIPLY termino
                | factor DIVIDE termino '''
    pass

def p_factor(p):
    ''' factor : varCTE 
                | OPAREN expresion CPAREN 
                | PLUS varCTE
                | MINUS varCTE '''
    pass

def p_varCTE(p):
    ''' varCTE : ID 
                | INT
                | DEC
                | STRING
                | BOOL '''
    pass

def p_END(p):
    ''' end : END OPAREN ID CPAREN '''
    pass

def p_epsilon(p):
    ''' epsilon : '''
    pass

#Manejo de error sintactico
def p_error(p):
    print("ERROR: Error de sintaxis: '%s'" % p.value, p)
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