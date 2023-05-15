import ply.yacc as yacc
from lexer import tokens
from funcsDir import FuncsDir
from funcsDir import TypeDir

funcsDirectory = FuncsDir()
typesDirectory = TypeDir()

pos=1
x=-1

def add_func(x, y):
    return x + y

 # función auxiliar para imprimir el árbol de sintaxis
def print_control(p, nonterminal: str, max_symbols: int):
    print(f"Parsed {nonterminal}  \t\t", end="")
    for i in range(1, max_symbols+1):
        try:
            print(f"{p[i]}", end="\t")
        except:
            pass
    print("")

def p_begin(p):
    ''' begin : BEGIN OPAREN ID CPAREN classDef fxDef main end '''
    print_control(p,"begin",8)

def p_main(p):
    ''' main : MAIN OPAREN CPAREN OBRACKET body CBRACKET '''
    print_control(p,"main",6)


def p_fxDef(p):
    ''' fxDef : VOID FX ID OPAREN param pointFuncParam CPAREN OBRACKET body pointVars CBRACKET pointFuncType fxDef
                | simpleType FX ID OPAREN param pointFuncParam CPAREN OBRACKET body pointVars RETURN ID EOF CBRACKET pointFuncType fxDef
                | epsilon '''
    print_control(p,"fxDef",13)

def p_pointFuncType(p):
    ''' pointFuncType : '''
    typesDirectory.delete_type()

def p_pointFuncParam(p):
    ''' pointFuncParam : '''
    print("NOMBRE_F",p[-3])
    func_name = p[-3]
    func_type = typesDirectory.get_type(0)
    print("TIPO_F", func_type)
    global pos
    global x
    func_param = []
    for a in range(x+1):
        func_param.append(typesDirectory.get_type(pos))
        print("TIPO_P", typesDirectory.get_type(pos))
        pos = pos + 1
    funcsDirectory.add_function(func_name,func_type,func_param)
    typesDirectory.delete_type()
    x = -1
    pos = 1
    print("DICCIONARIO: ", funcsDirectory.print_dict())

def p_pointVars(p):
    ''' pointVars : '''
    

def p_param(p):
    ''' param : simpleType ID 
            | simpleType ID COMMA param
            | epsilon '''
    print_control(p,"param",4)   
    global x
    print("X = ", x)
    x = x + 1
    print("TEST PARAM ", typesDirectory.get_type(x))
    print("X2 = ", x)

 
def p_paramCall(p):
    ''' paramCall : ID 
                  | ID COMMA paramCall 
                  | epsilon '''
    print_control(p,"paramCall",3)


def p_voidCall(p):
    ''' voidCall : ID OPAREN paramCall CPAREN EOF '''
    print_control(p,"voidCall",5)


def p_body(p):
    ''' body : varsDef body
            | statements body
            | epsilon '''
    print_control(p,"body",2)


def p_statements(p):
    ''' statements : assignmentDef
                   | input
                   | output
                   | voidCall 
                   | whileCycle
                   | ifCond 
                   | classCall '''
    print_control(p,"statements",1)


def p_varsDef(p):
    ''' varsDef : VAR objType var EOF 
                | VAR simpleType var EOF '''
    print_control(p,"varsDef",4)


def p_var(p):
    ''' var : varsType 
            | varsType COMMA var '''
    print_control(p,"var",3)


def p_varsType(p):
    ''' varsType : ID
                | arrDef
                | matrixDef '''
    print_control(p,"varsType",1)


def p_arrDef(p):
    ''' arrDef : ID OSQUAREBR varCte CSQUAREBR '''
    print_control(p,"arrDef",4)


def p_matrixDef(p):
    ''' matrixDef : arrDef OSQUAREBR varCte CSQUAREBR '''
    print_control(p,"matrixDef",4)


def p_assignmentDef(p):
    ''' assignmentDef : ID ASSIGNMENT expAssignment '''
    print_control(p,"assignmentDef",3)


def p_expAssignment(p):
    ''' expAssignment : expRelational EOF
                      | returnCall EOF
                      | classCall '''
    print_control(p,"expAssignment",2)

def p_returnCall(p):
    ''' returnCall : ID OPAREN paramCall CPAREN '''
    pass

def p_expRelational(p):
    ''' expRelational : plusMinus 
                    | plusMinus opRelational expRelational '''
    print_control(p,"expRelational",3)

def p_opRelational(p):
    ''' opRelational : EQUAL
                    | DIFFERENT
                    | GREATERTHAN
                    | GREATERTHANEQ 
                    | LESSTHAN 
                    | LESSTHANEQ '''
    print_control(p,"opRelational",1)

def p_plusMinus(p):
    ''' plusMinus : multDiv
                | multDiv PLUS plusMinus
                | multDiv MINUS plusMinus '''
    print_control(p,"plusMinus",3)

def p_multDiv(p):
    ''' multDiv : expParen 
                | expParen MULTIPLY multDiv
                | expParen DIVIDE multDiv '''
    print_control(p,"multDiv",3)

def p_expParen(p):
    ''' expParen : OPAREN expRelational CPAREN
                | varCte '''
    print_control(p,"assignmentDef",3)

def p_classDef(p):
    ''' classDef : CLASS ID OBRACKET ATTRIBUTES COLON varsDef METHODS COLON fxDef CBRACKET classDef
                | epsilon '''
    print_control(p,"classDef",11)

def p_classCall(p):
    ''' classCall : ID MONEY ID OPAREN paramCall CPAREN EOF '''
    print_control(p,"classCall",7)

def p_simpleType(p):
    ''' simpleType : INT
                    | STRING
                    | DEC 
                    | BOOL '''
    fType = p[1]
    typesDirectory.set_type(fType)
    #print("TEST", typesDirectory.get_typeP(x+1))
    #pos = pos + 1
    print_control(p,"simpleType",1)


def p_objType(p):
    ''' objType : ID '''
    print_control(p,"objType",1)

def p_varCte(p):
    ''' varCte : INT 
                | DEC
                | STRING
                | ID '''
    print_control(p,"varCte",1)

def p_whileCycle(p):
    ''' whileCycle : WHILE OPAREN expRelational CPAREN OBRACKET statements CBRACKET '''
    print_control(p,"whileCycle",7)

def p_ifCond(p):
    ''' ifCond : IF OPAREN expRelational CPAREN OBRACKET statements CBRACKET 
                | ifCond ELSE OBRACKET statements CBRACKET '''
    print_control(p,"ifCond",7)

def p_input(p):
    ''' input : INPUT OPAREN ID CPAREN EOF '''
    print_control(p,"ifCond",5)

def p_output(p):
    ''' output : OUTPUT OPAREN expRelational CPAREN EOF '''
    print_control(p,"output",5)

def p_END(p):
    ''' end : END OPAREN ID CPAREN '''
    print_control(p,"END",4)

def p_epsilon(p):
    ''' epsilon : '''
    print_control(p,"epsilon",0)

#Manejo de error sintactico
def p_error(p):
    print("ERROR: Error de sintaxis: '%s'" % p.value, p)
    exit()

yacc.yacc()

#Probar Archivo
try:
    f = open('../Compilador/test/prueba2.dua')
    data = f.read()
    f.close()
except EOFError:
    quit()

yacc.parse(data)
print("CÓDIGO CORRECTO")