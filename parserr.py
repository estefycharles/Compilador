import ply.yacc as yacc
from lexer import tokens
from directory import Directory
from semantic_cube import Semantic_cube
from cuac import Cuac

funcsDirectory = Directory()
cube = Semantic_cube()
newCuac = Cuac()

varType = ''
funcType = ''
funcName = ''
paramType = ''
classVars = ''
objVar = 0
internalScope = ''
scopeNumber = 0
res = 0

pOper = ['$'] #operators stack
pOprnd = [] #operands stack 
pTypes = [] #operands types stack
pTemps = [] #temporal vars stack
pTempsTypes = [] #temporal vars types stack

# Helper function to add temps
def add_temp(op1, op2, resT, opr):
    temp = newCuac.add_temps()
    #pTempsTypes.append(resT)
    #pTemps.append(temp)
    pOprnd.append(temp)
    pTypes.append(resT)
    #newCuac.create_cuac(opr, op1, op2, temp)
    return temp

 # función auxiliar para imprimir el árbol de sintaxis
def print_control(p, nonterminal: str, max_symbols: int):
    #print(f"Parsed {nonterminal}  \t\t", end="")
    #for i in range(1, max_symbols+1):
    #    try:
    #        print(f"{p[i]}", end="\t")
    #    except:
    #        pass
    #print("")
    x=1

def p_begin(p):
    ''' begin : BEGIN OPAREN ID CPAREN classDef fxDef  main end '''
    print_control(p,"begin",8)
    funcsDirectory.print_dict()
    newCuac.print1()

#punto neuralgico para identificar el main
def p_pointMain(p):
    ''' pointMain : '''
    funcsDirectory.set_scope('main')
    global internalScope
    internalScope = 'main'

def p_main(p):
    ''' main : MAIN pointMain OPAREN CPAREN OBRACKET body CBRACKET '''
    print_control(p,"main",6)

def p_fxDef(p):
    ''' fxDef : VOID FX pointFx ID pointFxId OPAREN param CPAREN OBRACKET body CBRACKET fxDef
                | fxType FX pointFx ID pointFxId OPAREN param CPAREN OBRACKET body RETURN ID EOF CBRACKET fxDef
                | epsilon '''
    print_control(p,"fxDef",13)

def p_fxType(p):
    ''' fxType : INT
                | STRING
                | DEC
                | BOOL '''
    global funcType
    funcType = p[1]


#punto neuralgico para identificar funciones
def p_pointFx(p):
    ''' pointFx : '''
    if scopeNumber == 0:
        funcsDirectory.set_scope('fx')
    else:
        funcsDirectory.set_scope('class')
    global internalScope
    internalScope = 'fx'

def p_pointFxId(p):
    ''' pointFxId : '''
    global funcName
    funcName = p[-1]
    funcsDirectory.set_functionName(p[-1])
    if funcsDirectory.exists_fx(p[-1]):
        print('ERROR: FX name:', funcName, 'already declared')
    else:
        funcsDirectory.add_function(funcName,funcType)
    

def p_param(p):
    ''' param : paramType ID pointParam
            | paramType ID pointParam COMMA param
            | epsilon '''
    print_control(p,"param",4)   

def p_paramType(p):
    ''' paramType : INT
                | STRING
                | DEC
                | BOOL '''
    global paramType
    paramType = p[1]
 
def p_pointParam(p):
    ''' pointParam : '''
    funcsDirectory.add_param(paramType, p[-1])
    

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
                | VAR varSimpleType var EOF '''
    print_control(p,"varsDef",4)

def p_varSimpleType(p):
    ''' varSimpleType : INT
                      | STRING
                      | DEC
                      | BOOL '''
    global varType
    varType = p[1]


def p_var(p):
    ''' var : varsType 
            | varsType COMMA var '''
    print_control(p,"var",3)


def p_varsType(p):
    ''' varsType : ID
                | arrDef
                | matrixDef '''
    print_control(p,"varsType",1)
    global objVar
    if objVar == 1:
        if funcsDirectory.exists_classVars(p[1]):
            print('ERROR: CLASSVAR name:', p[1], 'already declared')
        else:
            funcsDirectory.add_classVars(p[1], classVars)
    else:
        if funcsDirectory.exists_var(p[1], internalScope):
            print('ERROR: VAR name:', p[1], 'already declared')
        else:
            funcsDirectory.add_var(p[1], varType, internalScope)


def p_arrDef(p):
    ''' arrDef : ID OSQUAREBR varCte CSQUAREBR '''
    print_control(p,"arrDef",4)


def p_matrixDef(p):
    ''' matrixDef : arrDef OSQUAREBR varCte CSQUAREBR '''
    print_control(p,"matrixDef",4)


def p_assignmentDef(p):
    ''' assignmentDef : ID ASSIGNMENT pointPushAssignment expAssignment '''
    print_control(p,"assignmentDef",3)
    if funcsDirectory.exists_var(p[1], internalScope):
        pTypes.append(funcsDirectory.get_varType(p[1], internalScope))
        pOprnd.append(p[1])
        print('ASSIG1',pOprnd)
        res = pOprnd.pop()
        resT = pTypes.pop()
        op1 = pOprnd.pop()
        opT1 = pTypes.pop()
        opr = pOper.pop()
        print('ASSIG2',pOprnd)
        if resT == opT1:
            newCuac.create_cuac(opr, op1, None, res)
        else:
            print('ERROR: Type mismatch')
    else:
        print('ERROR: var does not exist')

def p_pointPushAssignment(p):
    ''' pointPushAssignment : '''
    pOper.append(p[-1])


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
                    | plusMinus opRelational expRelational pointCheckOpRel '''
    print_control(p,"expRelational",3)
    p[0] = p[1]

#punto para validar si el top() de poper es > < ...
def p_pointCheckOpRel(p):
    ''' pointCheckOpRel : '''
    if pOper[-1] == '==' or pOper[-1] == '!=' or pOper[-1] == '>' or pOper[-1] == '<' or pOper[-1] == '>=' or pOper[-1] == '<=':
        print('REL1',pOprnd)
        print('REL1',pOper)
        op2 = pOprnd.pop()
        op2T = pTypes.pop()
        op1 = pOprnd.pop()
        op1T = pTypes.pop()
        opr = pOper.pop()
        print('REL2',pOprnd)
        resT = cube.cube[op1T][op2T][opr]
        if resT != 'error':
            res = add_temp(op1, op2, resT,opr)
            newCuac.create_cuac(opr, op1, op2, res)
        else:
            print('ERROR: Type mismatch')

def p_opRelational(p):
    ''' opRelational : EQUAL
                    | DIFFERENT
                    | GREATERTHAN
                    | GREATERTHANEQ 
                    | LESSTHAN 
                    | LESSTHANEQ '''
    print_control(p,"opRelational",1)
    pOper.append(p[1])

def p_plusMinus(p):
    ''' plusMinus : multDiv pointCheckPlusMinus
                | multDiv pointCheckPlusMinus PLUS pointPushPlusMinus plusMinus
                | multDiv pointCheckPlusMinus MINUS pointPushPlusMinus plusMinus '''
    print_control(p,"plusMinus",3)
    p[0] = p[1]

#punto para validar si el top() de poper es + -
def p_pointCheckPlusMinus(p):
    ''' pointCheckPlusMinus : '''
    if pOper[-1] == '+' or pOper[-1] == '-':
        print('PLUSMINUS1',pOprnd)
        op2 = pOprnd.pop()
        op2T = pTypes.pop()
        op1 = pOprnd.pop()
        op1T = pTypes.pop()
        opr = pOper.pop()
        print('PLUSMINUS2',pOprnd)
        resT = cube.cube[op1T][op2T][opr]
        if resT != 'error':
            res = add_temp(op1, op2, resT, opr)
            newCuac.create_cuac(opr, op1, op2, res)
            #pOprnd.append(res)
            #pTypes.append(resT)
        else:
            print('ERROR: Type mismatch')

#punto para hacer push del +- en pOper
def p_pointPushPlusMinus(p):
    ''' pointPushPlusMinus : '''
    pOper.append(p[-1])

def p_multDiv(p):
    ''' multDiv : expParen pointCheckMultDiv
                | expParen pointCheckMultDiv MULTIPLY pointPushMultDiv multDiv
                | expParen pointCheckMultDiv DIVIDE pointPushMultDiv multDiv '''
    print_control(p,"multDiv",3)
    p[0] = p[1]

#punto para validar si el top() de poper es */
def p_pointCheckMultDiv(p):
    ''' pointCheckMultDiv : '''
    if pOper[-1] == '*' or pOper[-1] == '/':
        print('MULTDIV1',pOprnd)
        op2 = pOprnd.pop()
        op2T = pTypes.pop()
        op1 = pOprnd.pop()
        op1T = pTypes.pop()
        opr = pOper.pop()
        print('MULTDIV2',pOprnd)
        resT = cube.cube[op1T][op2T][opr]
        if resT != 'error':
            res = add_temp(op1, op2, resT, opr)
            newCuac.create_cuac(opr, op1, op2, res)
            #pOprnd.append(res)
            #pTypes.append(resT)
        else:
            print('ERROR: Type mismatch')
            

#punto para hacer push del */ en pOper
def p_pointPushMultDiv(p):
    ''' pointPushMultDiv : '''
    pOper.append(p[-1])

def p_expParen(p):
    ''' expParen : OPAREN pointFakeBackground expRelational CPAREN pointRemoveFakeBackground
                | varCte '''
    print_control(p,"expParen",3)
    p[0] = p[1]

def p_pointFakeBackground(p):
    ''' pointFakeBackground : '''
    pOper.append(p[-1])


def p_pointRemoveFakeBackground(p):
    ''' pointRemoveFakeBackground : ''' 
    pOper.pop()

def p_classDef(p):
    ''' classDef : CLASS pointClass ID pointClassName OBRACKET ATTRIBUTES COLON pointAtt METHODS COLON pointScopeClass fxDef pointScopeClass2 CBRACKET classDef
                | epsilon '''
    print_control(p,"classDef",11)

def p_pointAtt(p):
    ''' pointAtt : varsDef 
                | varsDef pointAtt '''

def p_pointScopeClass(p):
    ''' pointScopeClass : '''
    global scopeNumber
    scopeNumber = 1

def p_pointScopeClass2(p):
    ''' pointScopeClass2 : '''
    global scopeNumber
    scopeNumber = 0

def p_pointClassName(p):
    ''' pointClassName : '''
    funcsDirectory.set_className(p[-1])
    if funcsDirectory.exists_class(p[-1]):
        print('ERROR: CLASS name:', p[-1], 'already declared')
    else:
        funcsDirectory.add_class(p[-1])

#punto neuralgico para identificar clases
def p_pointClass(p):
    ''' pointClass : '''
    funcsDirectory.set_scope('class')
    global internalScope
    internalScope = 'class'

def p_classCall(p):
    ''' classCall : ID MONEY ID OPAREN paramCall CPAREN EOF '''
    print_control(p,"classCall",7)

def p_objType(p):
    ''' objType : ID '''
    print_control(p,"objType",1)
    global classVars
    classVars = p[1]
    global objVar
    objVar = 1

def p_varCte(p):
    ''' varCte : INT pointINT
                | DEC pointDEC
                | STRING pointSTRING
                | ID '''
    print_control(p,"varCte",1)
    p[0] = p[1]
    if funcsDirectory.exists_var(p[1], internalScope):
        pTypes.append(funcsDirectory.get_varType(p[1], internalScope))
        pOprnd.append(p[1])
    
def p_pointINT(p):
    ''' pointINT : '''
    pTypes.append('int')
    pOprnd.append(p[-1])

def p_pointDEC(p):
    ''' pointDEC : '''
    pTypes.append('dec')
    pOprnd.append(p[-1])

def p_pointSTRING(p):
    ''' pointSTRING : '''
    pTypes.append('string')
    pOprnd.append(p[-1])

def p_whileCycle(p):
    ''' whileCycle : WHILE OPAREN expRelational CPAREN OBRACKET body CBRACKET '''
    print_control(p,"whileCycle",7)

def p_ifCond(p):
    ''' ifCond : IF OPAREN expRelational CPAREN OBRACKET body CBRACKET 
                | ifCond ELSE OBRACKET body CBRACKET '''
    print_control(p,"ifCond",7)

def p_input(p):
    ''' input : INPUT OPAREN ID CPAREN EOF '''
    print_control(p,"input",5)
    pOprnd.append(p[3])
    res = pOprnd.pop()
    newCuac.create_cuac('input', None, None, res)

def p_output(p):
    ''' output : OUTPUT OPAREN expRelational CPAREN EOF '''
    print_control(p,"output",5)
    res = pOprnd.pop()
    newCuac.create_cuac('output', None, None, res)

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
    f = open('../Compilador/test/pruebaCuac.dua')
    data = f.read()
    f.close()
except EOFError:
    quit()

yacc.parse(data)
print("CÓDIGO CORRECTO")