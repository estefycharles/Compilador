from directory import Directory
from memory_map import MemoryMap


class VirtualMachine:

    def __init__(self):
        self.cuacs = []
        self.mainList = []
        self.cteList = []
        self.fxList = []
        self.globalList = []
        self.memoryMap = MemoryMap()
        self.memoryMapCte = MemoryMap()
        self.memoryGlobal = MemoryMap()
        self.memoryStack = []

    def load_cuacs(self, filename):
        with open(filename, 'r') as file:
            cuacs = []
            for line in file:
                str(line)
                line = line.strip()  # Remove leading/trailing whitespace
                if line:
                    cuac = line.split(',')  # Assuming each quadruple is comma-separated
                    cuacs.append(cuac)
            return cuacs
    
    def set_cte_list(self, list):
        self.cteList = list

    def set_fx_list(self, list):
        self.fxList = list
    
    def set_global_list(self, list):
        self.globalList = list

    def find_value(self,op):
        for element in self.cteList:
            if 'dirV' in element[1]: 
                 dir = element[1]['dirV']
                 if dir == int(op):
                     return element[0]
        for element in self.memoryGlobal.get_memory().values():
            if int(op) in element.keys():
                return element[int(op)]           
        for element in self.memoryStack[-1].get_memory().values():
            if int(op) in element.keys():
                return element[int(op)]


#text file
#funciones
    def execute(self):
        print("-------------------------------------------- FRANK O> --------------------------------------------")
        self.memoryMap.set_cte(self.cteList)
        self.memoryMap.set_fxMem(self.fxList)
        self.memoryMap.set_globalMem(self.globalList)
        self.memoryMap.set_cte_memory()
        self.memoryMap.set_memory()
        self.memoryMapCte.set_cte(self.cteList)
        self.memoryMapCte.set_fxMem(self.fxList)
        self.memoryMapCte.set_globalMem(self.globalList)
        self.memoryMapCte.set_cte_memory()
        self.memoryGlobal.set_globalMem(self.globalList)
        cuacs = self.load_cuacs('pato.txt')
        ip = 0 
        param = 0
        fxName = ''
        returnValue = 0
        returnDir = 0
        returnFlag = 0
        bread_crumb = []
        arrFlag = 0
        self.memoryStack.append(self.memoryMap) #memory map inicial
        while(ip < len(cuacs)):
            #print(cuacs[ip])
            opr, op1, op2, res = cuacs[ip]
            if opr == 'goto':
                #salta a la linea # (res)
                ip = int(res) - 1
            elif opr == '+': 
                if arrFlag == 1: #suma la dirBase del arr y calcula la dir del indice
                    value1 = self.find_value(op1)
                    result = value1 + int(op2)
                    self.memoryStack[-1].set_value(int(res), result)
                else:
                    value1 = self.find_value(op1)
                    value2 = self.find_value(op2)
                    result = value1 + value2
                    self.memoryStack[-1].set_value(int(res), result)
                ip += 1
            elif opr == '-':
                value1 = self.find_value(op1)
                value2 = self.find_value(op2)
                result = value1 - value2
                self.memoryStack[-1].set_value(int(res), result)
                ip += 1
            elif opr == '*':
                value1 = self.find_value(op1)
                value2 = self.find_value(op2)
                result = value1 * value2
                self.memoryStack[-1].set_value(int(res), result)
                ip += 1
            elif opr == '/':
                value1 = self.find_value(op1)
                value2 = self.find_value(op2)
                result = value1 / value2
                self.memoryStack[-1].set_value(int(res), result)
                ip += 1
            elif opr == '=':
                if arrFlag == 1:
                    if int(op1) > 17000: #cuando asignas arr a una var
                        dirArr = self.find_value(op1) #trae dir de arr
                        value = self.find_value(dirArr) #trae la dir de lo que esta en esa posicion del arr
                        #value = self.find_value(dirValue)
                        self.memoryStack[-1].set_value(int(res), value)
                    elif int(res) > 17000:
                        dir = self.find_value(res) #trae dir de arr
                        value = self.find_value(op1)
                        self.memoryStack[-1].set_value(dir, value)
                    arrFlag = 0
                else:
                    value = self.find_value(op1)
                    self.memoryStack[-1].set_value(int(res), value)
                ip += 1
            elif opr == 'output':
                print(self.find_value(res))
                ip += 1
            elif opr == 'input': #se dejo a medias, solo están enteros y falta hacer lo de las funciones
               resType = int(res)
               ip += 1
               value = input()
               if (resType >= 1000 and resType < 2000) or (resType >= 5000 and resType < 6000) or (resType >= 9000 and resType < 10000) or (resType >= 13000 and resType <14000):#int
                    try:
                        value = int(value)
                        self.memoryStack[-1].set_value(int(res), value)
                    except Exception:
                        print("Cuack cuack cuack... Type mismatch at input :( Expected INT in " + value)
                        break
               elif (resType >= 2000 and resType < 3000) or (resType >= 6000 and resType < 7000) or (resType >= 10000 and resType < 11000) or (resType >= 14000 and resType <15000):#dec
                    try:
                        value = float(value)
                        self.memoryStack[-1].set_value(int(res), value)
                    except Exception:
                        print("Cuack cuack cuack... Type mismatch at input :( Expected DEC in " + value)
                        break
               elif (resType >= 3000 and resType < 4000) or (resType >= 7000 and resType < 8000) or (resType >= 11000 and resType < 12000) or (resType >= 15000 and resType <16000):#bool
                    if value == 'true' or value == 'false':
                        value = str(value)
                        self.memoryStack[-1].set_value(int(res), value)
                    else: 
                        print("Cuack cuack cuack... Type mismatch at input :( Expected BOOL in " + value)
                        break
               elif (resType >= 4000 and resType < 5000) or (resType >= 8000 and resType < 9000) or (resType >= 12000 and resType < 13000) or (resType >= 16000 and resType <17000):#string
                   if value.isdigit():
                        print("Cuack cuack cuack... Type mismatch at input :( Expected STRING in " + value)
                        break
                   else:
                       value = str(value)
                       self.memoryStack[-1].set_value(int(res), value)
            elif opr == '<':
                value1 = self.find_value(op1)
                value2 = self.find_value(op2)
                result = value1 < value2 #bool
                self.memoryStack[-1].set_value(int(res), result)
                ip += 1
            elif opr == '>':
                value1 = self.find_value(op1)
                value2 = self.find_value(op2)
                result = value1 > value2 #bool
                self.memoryStack[-1].set_value(int(res), result)
                ip += 1
            elif opr == '<=':
                value1 = self.find_value(op1)
                value2 = self.find_value(op2)
                result = value1 <= value2 #bool
                self.memoryStack[-1].set_value(int(res), result)
                ip += 1
            elif opr == '>=':
                value1 = self.find_value(op1)
                value2 = self.find_value(op2)
                result = value1 >= value2 #bool
                self.memoryStack[-1].set_value(int(res), result)
                ip += 1
            elif opr == '==':
                value1 = self.find_value(op1)
                value2 = self.find_value(op2)
                result = value1 == value2 #bool
                self.memoryStack[-1].set_value(int(res), result)
                ip += 1
            elif opr == 'gotoF':
                value1 = self.find_value(op1)
                if value1 == True:
                    ip += 1
                else:
                    ip = int(res) - 1
            elif opr == 'era':
                fxName = op1
                #crear nuevo memory map y hacer append al memory stack
                memStackTemp = MemoryMap()
                self.memoryStack.append(memStackTemp) #agrega un memory map vacío para usarlo durante esta fx
                ip += 1
            elif opr == 'gosub':
                bread_crumb.append(ip)
                ip = int(res) - 1
                param = 0
            elif opr == 'endfunc':
                if len(bread_crumb) > 0: 
                    ip = bread_crumb.pop() + 1
                self.memoryStack.pop()
                if returnFlag == 1:
                    #set a la lista de globales
                    self.memoryGlobal.set_value(returnDir, returnValue)
                    returnFlag  = 0
            elif opr == 'param':
                param = param + 1
                value1 = self.memoryStack[-2].get_value(int(op1))
                paramDir = self.memoryMap.get_paramDir(fxName, param)
                self.memoryStack[-1].set_value(paramDir, value1)
                ip += 1
            elif opr == 'return':
                value = self.find_value(res)
                dir = self.memoryGlobal.get_returnDir(fxName)
                self.memoryGlobal.set_value(dir, value)
                returnValue = value
                returnDir = dir
                returnFlag = 1
                ip += 1 
            elif opr == 'ver':
                arrFlag = 1
                value = self.find_value(op1)
                limInf = self.find_value(op2)
                limSup = self.find_value(res)
                if (value < limInf) or (value > limSup):
                    print("Cuack cuack cuack... Index out of range with value: " + str(value))
                    break
                ip += 1 
            else:
                break
        
        
        



