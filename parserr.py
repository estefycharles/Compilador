import sys
import ply.yacc as yacc
from lexer import tokens
from directory import Directory
from semantic_cube import Semantic_cube
from cuac import Cuac
from memory import MemoryAddress
from virtual_machine import VirtualMachine
from memory_map import MemoryMap
from dim import Dimension

funcsDirectory = Directory()
cube = Semantic_cube()
newCuac = Cuac()
memoryManagement = MemoryAddress()
vm = VirtualMachine()
memMap = MemoryMap()
dim = Dimension()

varType = ''
funcType = ''
funcName = ''
paramType = ''
classVars = ''
objVar = 0
internalScope = ''
scopeNumber = 0
res = 0
numParams = 0 #cont de params para fx calls
numParamsFx = 0 #cont de params de declaración de fx
nombreFx = ''
arrDir = 0 ##address from the index of the array

pOper = ['$'] #operators stack
pOprnd = [] #operands stack 
pTypes = [] #operands types stack
pJumps = [] #jumps on conditionals stack 

# Helper function to add temps
def add_temp(resT):
    temp = memoryManagement.temp_memory(resT)
    #temp = newCuac.add_temps()
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
    ''' begin : BEGIN pointCreateMainCuac OPAREN ID CPAREN classDef fxDef  main end'''
    print_control(p,"begin",8)
    #funcsDirectory.print_dict()
    #newCuac.print1()
    output_file = open("pato.txt", "w") #txt file con lista de cuádruplos
    cuacs_list = newCuac.getCuac()
    for cuac in cuacs_list:
        cuac_str = ','.join(str(x) for x in cuac)  #convierte los elementos a strings
        output_file.write(cuac_str + '\n')
    output_file.close()
    cteList = funcsDirectory.get_cte()
    fxList = funcsDirectory.get_fx()
    globalList = funcsDirectory.get_global()
    vm.set_cte_list(cteList)
    vm.set_fx_list(fxList)
    vm.set_global_list(globalList)
    vm.execute()
    print("-------------------------------------------- <O CUACK --------------------------------------------")

def p_pointCreateMainCuac(p):
    ''' pointCreateMainCuac : '''
    newCuac.create_cuac('goto', 'main', None, 'dest')


#punto neuralgico para identificar el main
def p_pointMain(p):
    ''' pointMain : '''
    funcsDirectory.set_scope('main')
    global internalScope
    internalScope = 'main'
    newCuac.fill(0,newCuac.countCuacs)
    memoryManagement.delete_localMemory()

def p_main(p):
    ''' main : MAIN pointMain OPAREN CPAREN OBRACKET body CBRACKET '''
    print_control(p,"main",6)

def p_fxDef(p):
    ''' fxDef : VOID FX pointFx ID pointFxId OPAREN param CPAREN pointParamCount OBRACKET body CBRACKET pointEndFunc fxDef
                | VOID FX pointFx ID pointFxId OPAREN epsilon CPAREN pointParamCount OBRACKET body CBRACKET pointEndFunc fxDef
                | fxType FX pointFx ID pointFxId OPAREN param CPAREN pointParamCount OBRACKET body RETURN ID pointReturn EOF CBRACKET pointEndFunc fxDef
                | fxType FX pointFx ID pointFxId OPAREN epsilon CPAREN pointParamCount OBRACKET body RETURN ID pointReturn EOF CBRACKET pointEndFunc fxDef
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
    memoryManagement.delete_localMemory()
    

def p_pointFxId(p):
    ''' pointFxId : '''
    global funcName
    funcName = p[-1]
    funcsDirectory.set_functionName(p[-1])
    if funcsDirectory.exists_fx(p[-1]):
        print('Cuack cuack cuack... FX name:', funcName, 'already declared')
        sys.exit(1)
    else:
        dirI = newCuac.countCuacs
        funcsDirectory.add_function(funcName,funcType,dirI)
        funcsDirectory.add_global(funcName, memoryManagement.global_memory(funcType))

def p_pointReturn(p):
    ''' pointReturn : '''
    newCuac.create_cuac('return', None, None, funcsDirectory.get_varDirV(p[-1], internalScope))
    # varType = funcsDirectory.get_varType(p[-1], internalScope)
    # if funcsDirectory.get_fxType(funcName) == varType:
    #     funcsDirectory.add_global(funcName, memoryManagement.global_memory(varType))
    # else:
    #     print('Cuack cuack cuack... Type mismatch in return type :(')

def p_pointParamCount(p):
    ''' pointParamCount : '''
    global numParamsFx
    global funcName
    funcsDirectory.set_fxParams(funcName,numParamsFx)
    numParamsFx = 0 # para reiniciar el cont a 0 cada que acabe de declarar un fx
    
def p_pointEndFunc(p):
    ''' pointEndFunc : '''
    newCuac.create_cuac('endfunc', None, None, None)
    #global numParamsFx
    #global funcName
    #funcsDirectory.set_fxParams(funcName,numParamsFx)
    #numParamsFx = 0 # para reiniciar el cont a 0 cada que acabe de declarar un fx

def p_param(p):
    ''' param : paramType ID pointParam
            | paramType ID pointParam COMMA param '''
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
    global numParamsFx
    numParamsFx += 1
    #funcsDirectory.add_param(paramType, numParamsFx, dirV)
    dirV = memoryManagement.local_memory(paramType,1)
    funcsDirectory.add_param(paramType, numParamsFx, dirV)
    funcsDirectory.add_var(p[-1], paramType, internalScope, dirV,0)

def p_paramCall(p):
    ''' paramCall : ID pointParamCall pointParamNum
                  | ID pointParamCall COMMA paramCall '''
    print_control(p,"paramCall",3)
    p[0] = p[1]
    global numParams
    numParams = 0 #para reiniciar el cont a 0 cuando termine de llamar una fx

#pn para comprobar que el num de parametros que espera la funcion sea el mismo que la llamada manda
def p_pointParamNum(p):
    ''' pointParamNum : '''
    global nombreFx
    global numParams
    if numParams != funcsDirectory.get_fxParams(nombreFx):
        print('Cuack cuack cuack... Expecting different number of parameters in FX:', nombreFx)
        sys.exit(1)

#pn para agregar el cuac de param en las llamadas de fx
def p_pointParamCall(p):
    ''' pointParamCall : '''
    global nombreFx
    global numParams
    numParams += 1
    if numParams != funcsDirectory.get_fxParams(nombreFx):
        print('Cuack cuack cuack... Expecting different number of parameters in FX:', nombreFx)
        sys.exit(1)
    varTypeT = funcsDirectory.get_varType(p[-1], internalScope) #tipo de var que se ingresa como param en la llamada
    paramTypeT = funcsDirectory.get_paramType(nombreFx, numParams) #tipo que la fx espera
    #checar si el tipo del param de la llamada es igual al que la fx recibe
    if varTypeT != paramTypeT:
        print('Cuack cuack cuack... Type mismatch in function call in parameters of FX:', nombreFx)
        sys.exit(1)
    else:
        pOprnd.append(funcsDirectory.get_varDirV(p[-1], internalScope)) #guarda la dirrecion de memoria del param de llamada
        #pOprnd.append(p[-1]) #guarda el id del param de llamada
        param = pOprnd.pop()
        newCuac.create_cuac('param', param, None, numParams)

def p_voidCall(p):
    ''' voidCall : ID pointEra OPAREN paramCall pointGoSub CPAREN EOF
                 | ID pointEra OPAREN epsilon pointParamVacio pointGoSub CPAREN EOF '''
    print_control(p,"voidCall",5)
    p[0] = p[1]

    
def p_pointEra(p):
    ''' pointEra : '''
    newCuac.create_cuac('era', p[-1], None, None)
    global nombreFx
    nombreFx = p[-1]

def p_pointGoSub(p):
    ''' pointGoSub : '''
    dirI = funcsDirectory.get_dirI(p[-4])
    newCuac.create_cuac('gosub', p[-4], None, dirI)

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
    ''' varsType : ID pointID
                | arrDef
                | matrixDef '''
    print_control(p,"varsType",1)
    
def p_pointID(p):
    ''' pointID : '''
    global objVar
    if objVar == 1:
        if funcsDirectory.exists_classVars(p[-1]):
            print('Cuack cuack cuack... CLASSVAR name:', p[-1], 'already declared')
            sys.exit(1)
        else:
            funcsDirectory.add_classVars(p[-1], classVars)
    else:
        if funcsDirectory.exists_var(p[-1], internalScope):
            print('Cuack cuack cuack... VAR name:', p[-1], 'already declared')
            sys.exit(1)
        else:
            dirV = memoryManagement.local_memory(varType,1)
            funcsDirectory.add_var(p[-1], varType, internalScope, dirV, 0)

def p_arrDef(p):
    ''' arrDef : ID OSQUAREBR INT COLON INT CSQUAREBR '''
    print_control(p,"arrDef",4)
    if funcsDirectory.exists_var(p[1], internalScope):
        print('Cuack cuack cuack... VAR name:', p[1], 'already declared')
        sys.exit(1)
    else:
        size = p[5] - p[3] + 1
        dirV = memoryManagement.local_memory(varType, size) #separa el tamaño del arr en memoria
        dirV = (dirV + 1) - size 
        funcsDirectory.add_var(p[1], varType, internalScope, dirV, 1)
        dim.set_dim(p[1], p[3], p[5])
    if funcsDirectory.exists_cte(p[3]): #esto se hace en pointINT pero no queremos agregar int a pOprnd
        dirV = funcsDirectory.get_cteDirV(p[3])
    else:
        dirV = memoryManagement.const_memory('int')
        funcsDirectory.add_cte(p[3], dirV)
    if funcsDirectory.exists_cte(p[5]): 
        dirV = funcsDirectory.get_cteDirV(p[5])
    else:
        dirV = memoryManagement.const_memory('int')
        funcsDirectory.add_cte(p[5], dirV)
        

def p_arr(p): #solo puede haber int y id
    ''' arr : ID OSQUAREBR varCte pointCheckTypeInt CSQUAREBR '''
    p[0] = p[1]
    if funcsDirectory.exists_var(p[1], internalScope):
        global arrDir #address from the index of the array
        limInf = dim.get_limInf(p[1])
        limSup = dim.get_limSup(p[1])
        limInf = funcsDirectory.get_cteDirV(limInf)
        limSup = funcsDirectory.get_cteDirV(limSup)
        newCuac.create_cuac('ver', arrDir, limInf, limSup)
        resTemp = add_temp('int')
        if funcsDirectory.exists_cte(1):
            dirV = funcsDirectory.get_cteDirV(1)
        else:
            dirV = memoryManagement.const_memory('int')
            funcsDirectory.add_cte(1, dirV)
        newCuac.create_cuac('-', arrDir, dirV, resTemp) #s1 - 1
        arrIdDir = funcsDirectory.get_varDirV(p[1], internalScope)
        dirPointer = memoryManagement.pointer_memory()
        pOprnd.append(dirPointer)
        pTypes.append(funcsDirectory.get_varType(p[1], internalScope))
        newCuac.create_cuac('+', resTemp, arrIdDir, dirPointer) #+driB
    else:
        print('Cuack cuack cuack... VAR:', p[1], 'does not exist')
        sys.exit(1)
    

def p_pointCheckTypeInt(p):
    ''' pointCheckTypeInt : '''
    global arrDir
    if isinstance(p[-1], int): #cuando p[-1] es un nuemro
        arrDir = funcsDirectory.get_cteDirV(p[-1])
    elif isinstance(p[-1], float):
        print('Cuack cuack cuack... Array:', p[-3], 'index', p[-1], 'can only be INT')
        sys.exit(1)
    elif funcsDirectory.get_varType(p[-1], internalScope) != 'int': #si entra con ID verifica que type = int
        print('Cuack cuack cuack... Array:', p[-3], 'index', p[-1], 'can only be INT')
        sys.exit(1)
    else:
        arrDir = funcsDirectory.get_varDirV(p[-1], internalScope)

    

def p_matrixDef(p):
    ''' matrixDef : arrDef OSQUAREBR varCte COLON varCte CSQUAREBR '''
    print_control(p,"matrixDef",4)


def p_assignmentDef(p):
    ''' assignmentDef : ID ASSIGNMENT pointPushAssignment expAssignment
                      | arr ASSIGNMENT pointPushAssignment expAssignment '''
    print_control(p,"assignmentDef",3)
    if funcsDirectory.exists_var(p[1], internalScope):
        if funcsDirectory.get_varDim(p[1], internalScope) != 1:
            pTypes.append(funcsDirectory.get_varType(p[1], internalScope))
            pOprnd.append(funcsDirectory.get_varDirV(p[1], internalScope))
            res = pOprnd.pop()
            resT = pTypes.pop()
            op1 = pOprnd.pop()
            opT1 = pTypes.pop()
            opr = pOper.pop()
            if resT == opT1:
                newCuac.create_cuac(opr, op1, None, res)
            else:
                print('Cuack cuack cuack... Type mismatch in VAR:', p[1])
                sys.exit(1)
        else: #si es un arreglo
            op1 = pOprnd.pop()
            opT1 = pTypes.pop()
            res = pOprnd.pop()
            resT = pTypes.pop()
            opr = pOper.pop()
            if resT == opT1:
                newCuac.create_cuac(opr, op1, None, res)
            else:
                print('Cuack cuack cuack... Type mismatch in VAR:', p[1])
                sys.exit(1)
    else:
        print('Cuack cuack cuack... VAR:', p[1], 'does not exist')
        sys.exit(1)

def p_pointPushAssignment(p):
    ''' pointPushAssignment : '''
    pOper.append(p[-1])


def p_expAssignment(p):
    ''' expAssignment : expRelational EOF
                      | returnCall EOF
                      | classCall '''
    print_control(p,"expAssignment",2)

def p_returnCall(p):
    ''' returnCall : ID pointEra OPAREN paramCall pointGoSub CPAREN 
                   | ID pointEra OPAREN epsilon pointParamVacio pointGoSub CPAREN '''
    if funcsDirectory.exists_fx(p[1]):
        pTypes.append(funcsDirectory.get_fxType(p[1]))
        pOprnd.append(funcsDirectory.get_globalDirV(p[1]))
    else:
        print('Cuack cuack cuack... Fuction ' + p[1] + ' does not exist :(')
        sys.exit(1)
    p[0] = p[1]   

def p_pointParamVacio(p):
     ''' pointParamVacio : '''
     if funcsDirectory.exists_fx(p[-4]):
        if numParams != funcsDirectory.get_fxParams(nombreFx):
            print('Cuack cuack cuack... Expecting different number of parameters in FX:', nombreFx)
            sys.exit(1)
     else:
        print('Cuack cuack cuack... Fuction ' + p[-4] + ' does not exist :(')
        sys.exit(1)

def p_expRelational(p):
    ''' expRelational : plusMinus 
                    | plusMinus opRelational expRelational pointCheckOpRel '''
    print_control(p,"expRelational",3)
    p[0] = p[1]

#punto para validar si el top() de poper es > < ...
def p_pointCheckOpRel(p):
    ''' pointCheckOpRel : '''
    if pOper[-1] == '==' or pOper[-1] == '!=' or pOper[-1] == '>' or pOper[-1] == '<' or pOper[-1] == '>=' or pOper[-1] == '<=':
        op2 = pOprnd.pop()
        op2T = pTypes.pop()
        op1 = pOprnd.pop()
        op1T = pTypes.pop()
        opr = pOper.pop()
        resT = cube.cube[op1T][op2T][opr]
        if resT != 'error':
            res = add_temp(resT)
            newCuac.create_cuac(opr, op1, op2, res)
        else:
            print('Cuack cuack cuack... Type mismatch in expression: ' + str(opr))
            sys.exit(1)

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
        op2 = pOprnd.pop()
        op2T = pTypes.pop()
        op1 = pOprnd.pop()
        op1T = pTypes.pop()
        opr = pOper.pop()
        resT = cube.cube[op1T][op2T][opr]
        if resT != 'error':
            res = add_temp(resT)
            newCuac.create_cuac(opr, op1, op2, res)
            #pOprnd.append(res)
            #pTypes.append(resT)
        else:
            print('Cuack cuack cuack... Type mismatch in expression: ' + str(opr))
            sys.exit(1)

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
        op2 = pOprnd.pop()
        op2T = pTypes.pop()
        op1 = pOprnd.pop()
        op1T = pTypes.pop()
        opr = pOper.pop()
        resT = cube.cube[op1T][op2T][opr]
        if resT != 'error':
            res = add_temp(resT)
            newCuac.create_cuac(opr, op1, op2, res)
            #pOprnd.append(res)
            #pTypes.append(resT)
        else:
            print('Cuack cuack cuack... Type mismatch in expression: ' + str(opr))
            sys.exit(1)
            

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
        print('Cuack cuack cuack... CLASS name:', p[-1], 'already declared')
        sys.exit(1)
    else:
        funcsDirectory.add_class(p[-1])

#punto neuralgico para identificar clases
def p_pointClass(p):
    ''' pointClass : '''
    funcsDirectory.set_scope('class')
    global internalScope
    internalScope = 'class'

def p_classCall(p):
    ''' classCall : ID MONEY ID OPAREN paramCall CPAREN EOF
                  | ID MONEY ID OPAREN epsilon CPAREN EOF '''
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
                | TRUE pointBOOL
                | FALSE pointBOOL
                | ID
                | arr '''
    print_control(p,"varCte",1)
    p[0] = p[1]
    if len(p) == 2:
        if funcsDirectory.exists_var(p[1], internalScope):
            if funcsDirectory.get_varDim(p[1], internalScope) != 1:
                pTypes.append(funcsDirectory.get_varType(p[1], internalScope))
                pOprnd.append(funcsDirectory.get_varDirV(p[1], internalScope))
        else:
            print('Cuack cuack cuack... VAR:', p[1], 'does not exist')
            sys.exit(1)
          
def p_pointINT(p):
    ''' pointINT : '''
    pTypes.append('int')
    if funcsDirectory.exists_cte(p[-1]):
        dirV = funcsDirectory.get_cteDirV(p[-1])
        pOprnd.append(dirV)
    else:
        dirV = memoryManagement.const_memory('int')
        funcsDirectory.add_cte(p[-1], dirV)
        pOprnd.append(dirV)


def p_pointDEC(p):
    ''' pointDEC : '''
    pTypes.append('dec')
    if funcsDirectory.exists_cte(p[-1]):
        dirV = funcsDirectory.get_cteDirV(p[-1])
        pOprnd.append(dirV)
    else:
        dirV = memoryManagement.const_memory('dec')
        funcsDirectory.add_cte(p[-1], dirV)
        pOprnd.append(dirV)

def p_pointSTRING(p):
    ''' pointSTRING : '''
    pTypes.append('string')
    if funcsDirectory.exists_cte(p[-1]):
        dirV = funcsDirectory.get_cteDirV(p[-1])
        pOprnd.append(dirV)
    else:
        dirV = memoryManagement.const_memory('string')
        funcsDirectory.add_cte(p[-1], dirV)
        pOprnd.append(dirV)

def p_pointBOOL(p):
    ''' pointBOOL : '''
    pTypes.append('bool')
    if funcsDirectory.exists_cte(p[-1]):
        dirV = funcsDirectory.get_cteDirV(p[-1])
        pOprnd.append(dirV)
    else:
        dirV = memoryManagement.const_memory('bool')
        funcsDirectory.add_cte(p[-1], dirV)
        pOprnd.append(dirV)

def p_whileCycle(p):
    ''' whileCycle : WHILE pointWhile1 OPAREN expRelational CPAREN pointWhile2 OBRACKET body CBRACKET pointWhile3'''
    print_control(p,"whileCycle",7)

def p_pointWhile1(p):
    ''' pointWhile1 : '''
    pJumps.append(newCuac.countCuacs)

def p_pointWhile2(p):
    ''' pointWhile2 : '''
    exp_type = pTypes.pop()
    if (exp_type != 'bool'):
        print('Cuack cuack cuack... Type Mismatch in WHILE')
        sys.exit(1)
    else:
        exp = pOprnd.pop()
        newCuac.create_cuac('gotoF',exp, None, 'dest')
        pJumps.append(newCuac.countCuacs-1)

def p_pointWhile3(p):
    ''' pointWhile3 : '''
    pendingCuac = pJumps.pop()
    whileBegin = pJumps.pop()
    newCuac.create_cuac('goto', None, None, whileBegin)
    newCuac.fill(pendingCuac-1, newCuac.countCuacs)


def p_ifCond(p):
    ''' ifCond : IF OPAREN expRelational CPAREN pointIfCond1 OBRACKET body CBRACKET pointIfCond2
                | IF OPAREN expRelational CPAREN pointIfCond1 OBRACKET body CBRACKET ELSE pointIfCond3 OBRACKET body CBRACKET pointIfCond2 '''
    print_control(p,"ifCond",7)

def p_pointIfCond1(p):
    ''' pointIfCond1 : '''
    exp_type = pTypes.pop()
    if (exp_type != 'bool'):
        print('Cuack cuack cuack... Type Mismatch in IF')
        sys.exit(1)
    else:
        exp = pOprnd.pop()
        newCuac.create_cuac('gotoF',exp, None, 'dest')
        pJumps.append(newCuac.countCuacs-1)

def p_pointIfCond2(p):
    ''' pointIfCond2 : '''
    pendingCuac = pJumps.pop()
    newCuac.fill(pendingCuac-1, newCuac.countCuacs)

def p_pointIfCond3(p):
    ''' pointIfCond3 : '''
    newCuac.create_cuac('goto', None, None, 'dest')
    pendingCuac = pJumps.pop()
    pJumps.append(newCuac.countCuacs - 1)
    newCuac.fill(pendingCuac-1, newCuac.countCuacs)


def p_input(p):
    ''' input : INPUT OPAREN ID CPAREN EOF '''
    print_control(p,"input",5)
    #pTypes.append(funcsDirectory.get_varType(p[3], internalScope))
    pOprnd.append(funcsDirectory.get_varDirV(p[3], internalScope))
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
    print("Cuack cuack cuack... Semantic ERRROR in %s" % p.value)
    sys.exit(1)

#yacc.yacc()
runParser = yacc.yacc()

# comentar para cuando se use archivo fly
# Probar Archivo
# try:
#     f = open('../Compilador/test/array_find.fk')
#     data = f.read()
#     f.close()
# except EOFError:
#     quit()
#comentar para cuando se use archivo fly
#yacc.parse(data)

#print("CÓDIGO CORRECTO")