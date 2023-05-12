import ply.yacc as yacc
from lexer import tokens

def p_begin(p):
    ''' begin : BEGIN OPAREN ID CPAREN classDef fxDef main end '''
    pass

def p_main(p):
    ''' main : MAIN OPAREN CPAREN OBRACKET body CBRACKET '''
    pass

def p_fxDef(p):
    ''' fxDef : VOID FX ID OPAREN param CPAREN OBRACKET body CBRACKET fxDef
                | simpleType FX ID OPAREN param CPAREN OBRACKET body RETURN ID EOF CBRACKET fxDef
                | epsilon '''
    pass

def p_param(p):
    ''' param : simpleType ID 
            | simpleType ID COMMA param
            | epsilon '''
    pass

def p_paramCall(p):
    ''' paramCall : ID 
                  | ID COMMA paramCall 
                  | epsilon '''
    pass

def p_voidCall(p):
    ''' voidCall : ID OPAREN paramCall CPAREN EOF '''
    pass

def p_body(p):
    ''' body : varsDef body
            | statements body
            | epsilon '''
    pass

def p_statements(p):
    ''' statements : assignmentDef
                   | input
                   | output
                   | voidCall 
                   | whileCycle
                   | ifCond 
                   | classCall '''
    pass

def p_varsDef(p):
    ''' varsDef : VAR objType var EOF 
                | VAR simpleType var EOF '''
    pass

def p_var(p):
    ''' var : varsType 
            | varsType COMMA var '''
    pass

def p_varsType(p):
    ''' varsType : ID
                | arrDef
                | matrixDef '''
    pass

def p_arrDef(p):
    ''' arrDef : ID OSQUAREBR varCte CSQUAREBR '''
    pass

def p_matrixDef(p):
    ''' matrixDef : arrDef OSQUAREBR varCte CSQUAREBR '''
    pass

def p_assignmentDef(p):
    ''' assignmentDef : ID ASSIGNMENT expAssignment '''
    pass

def p_expAssignment(p):
    ''' expAssignment : expRelational EOF
                      | returnCall EOF
                      | classCall '''
    pass

def p_returnCall(p):
    ''' returnCall : ID OPAREN paramCall CPAREN '''
    pass

def p_expRelational(p):
    ''' expRelational : plusMinus 
                    | plusMinus opRelational expRelational '''
    pass

def p_opRelational(p):
    ''' opRelational : EQUAL
                    | DIFFERENT
                    | GREATERTHAN
                    | GREATERTHANEQ 
                    | LESSTHAN 
                    | LESSTHANEQ '''
    pass

def p_plusMinus(p):
    ''' plusMinus : multDiv
                | multDiv PLUS plusMinus
                | multDiv MINUS plusMinus '''
    pass

def p_multDiv(p):
    ''' multDiv : expParen 
                | expParen MULTIPLY multDiv
                | expParen DIVIDE multDiv '''
    pass

def p_expParen(p):
    ''' expParen : OPAREN expRelational CPAREN
                | varCte '''
    pass

def p_classDef(p):
    ''' classDef : CLASS ID OBRACKET ATTRIBUTES COLON varsDef METHODS COLON fxDef CBRACKET classDef
                | epsilon '''
    pass

def p_classCall(p):
    ''' classCall : ID MONEY ID OPAREN paramCall CPAREN EOF '''
    pass

def p_simpleType(p):
    ''' simpleType : INT
                    | STRING
                    | DEC 
                    | BOOL '''
    pass

def p_objType(p):
    ''' objType : ID '''
    pass

def p_varCte(p):
    ''' varCte : INT 
                | DEC
                | STRING
                | ID '''
    pass

def p_whileCycle(p):
    ''' whileCycle : WHILE OPAREN expRelational CPAREN OBRACKET statements CBRACKET '''
    pass

def p_ifCond(p):
    ''' ifCond : IF OPAREN expRelational CPAREN OBRACKET statements CBRACKET 
                | ifCond ELSE OBRACKET statements CBRACKET '''
    pass 

def p_input(p):
    ''' input : INPUT OPAREN ID CPAREN EOF '''
    pass

def p_output(p):
    ''' output : OUTPUT OPAREN expRelational CPAREN EOF '''
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