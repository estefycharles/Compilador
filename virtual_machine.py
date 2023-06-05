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
        print("----------------------- FRANK O> -----------------------")
        self.memoryMap.set_cte(self.cteList)
        self.memoryMap.set_fxMem(self.fxList)
        self.memoryMap.set_globalMem(self.globalList)

        #self.memoryMap.print()
        self.memoryMap.set_cte_memory()
        self.memoryMap.set_memory()
        #print(self.cteList)
        #print(self.globalList)
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
        self.memoryStack.append(self.memoryMap) #memory map inicial
        while(ip < len(cuacs)):
            #print(cuacs[ip])
            opr, op1, op2, res = cuacs[ip]
            if opr == 'goto':
                #salta a la linea # (res)
                ip = int(res) - 1
            elif opr == '+':
                #value1 = self.memoryMap.get_value(int(op1))
                #value1 = self.memoryStack[-1].get_value(int(op1))   
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
                value = self.find_value(op1)
                #print('MEMORIA1', self.memoryStack[-1].get_memory())
                self.memoryStack[-1].set_value(int(res), value)
                #print('MEMORIA2', self.memoryStack[-1].get_memory())
                ip += 1
            elif opr == 'output':
                print(self.find_value(res))
                ip += 1
            elif opr == 'input': #se dejo a medias, solo están enteros y falta hacer lo de las funciones
               resType = int(res)
               ip += 1
               value = input()
               if (resType >= 1000 and resType < 2000) or (resType >= 5000 and resType < 6000) or (resType >= 9000 and resType < 10000):
                    try:
                        value = int(value)
                        self.memoryStack[-1].set_value(int(res), value)
                    except Exception:
                        print("ERROR: El valor esperado tiene que ser INT")
                        break
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
                #self.memoryMap.reset()
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
                    # globalListTemp = {returnValue, returnDir}
                    # self.globalList.append(globalListTemp)
                    #print('holaaaaaaa', returnValue, returnDir)
                    #self.memoryStack[-1].set_value(returnDir, returnValue)
                    returnFlag  = 0
            elif opr == 'param':
                param = param + 1
                value1 = self.memoryStack[-2].get_value(int(op1))
                paramDir = self.memoryMap.get_paramDir(fxName, param)
                self.memoryStack[-1].set_value(paramDir, value1)
                ip += 1
            elif opr == 'return':
                # if returnFlag > 1:
                #     value = self.memoryStack[-2].get_value(int(res))
                # else:
                
                value = self.find_value(res)
                #print("ENTREE RETURN", res)
                #print('MEMORIA3', self.memoryGlobal.get_memory())
                #print('MEMORIA3', self.memoryStack[-1].get_memory())
                #value = self.memoryStack[-2].get_value(int(res))
                #print("Fxname", fxName)
                # dir = self.memoryGlobal.get_returnDir(fxName)
                dir = self.memoryGlobal.get_returnDir(fxName)
                self.memoryGlobal.set_value(dir, value)
                #print('MEMORIA4', self.memoryGlobal.get_memory())
                #value = self.find_value(res)
                #print("VALUE", value)
                #dir = self.memoryMap.get_returnDir(fxName)
                returnValue = value
                returnDir = dir
                returnFlag = 1
                #self.memoryStack[-1].set_value(dir, value)
                #fxName = ''
                ip += 1 
            else:
                break
        
        
        



