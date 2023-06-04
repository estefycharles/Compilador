from directory import Directory
from memory_map import MemoryMap

directory = Directory()

class VirtualMachine:

    def __init__(self):
        self.cuacs = []
        self.mainList = []
        self.cteList = []
        self.fxList = []
        self.globalList = []
        self.memoryMap = MemoryMap()

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
    
    def set_main_list(self, list): #trae el directorio de variables del main
        self.mainList = list

    def set_cte_list(self, list):
        self.cteList = list

    def set_fx_list(self, list):
        self.fxList = list
    
    def set_global_list(self, list):
        self.globalList = list

#text file
#funciones
    def execute(self):
        print("----------------------- FRANK O> -----------------------")
        self.memoryMap.set_cte(self.cteList)
        self.memoryMap.set_fxMem(self.fxList)
        self.memoryMap.set_globalMem(self.globalList)
        self.memoryMap.print()
        self.memoryMap.set_cte_memory()
        self.memoryMap.set_cte_memoryFx()
        cuacs = self.load_cuacs('pato.txt')
        ip = 0 
        param = 0
        func = 0
        fxName = ''
        while(ip < len(cuacs)):
            opr, op1, op2, res = cuacs[ip]
            if opr == 'goto':
                #salta a la linea # (res)
                ip = int(res) - 1
            elif opr == '+':
                if func != 1:
                    value1 = self.memoryMap.get_value(int(op1))
                    value2 = self.memoryMap.get_value(int(op2))
                    result = value1 + value2
                    self.memoryMap.set_value(int(res), result)
                else:
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    value2 = self.memoryMap.get_valueFunc(int(op2))
                    result = value1 + value2
                    self.memoryMap.set_valueFunc(int(res), result)
                ip += 1
            elif opr == '-':
                if func != 1:
                    value1 = self.memoryMap.get_value(int(op1))
                    value2 = self.memoryMap.get_value(int(op2))
                    result = value1 - value2
                    self.memoryMap.set_value(int(res), result)
                else:
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    value2 = self.memoryMap.get_valueFunc(int(op2))
                    result = value1 - value2
                    self.memoryMap.set_valueFunc(int(res), result)
                ip += 1
            elif opr == '*':
                if func != 1:
                    value1 = self.memoryMap.get_value(int(op1))
                    value2 = self.memoryMap.get_value(int(op2))
                    result = value1 * value2
                    self.memoryMap.set_value(int(res), result)
                else:
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    value2 = self.memoryMap.get_valueFunc(int(op2))
                    result = value1 * value2
                    self.memoryMap.set_valueFunc(int(res), result)
                ip += 1
            elif opr == '/':
                if func != 1:
                    value1 = self.memoryMap.get_value(int(op1))
                    value2 = self.memoryMap.get_value(int(op2))
                    result = value1 / value2
                    self.memoryMap.set_value(int(res), result)
                else:
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    value2 = self.memoryMap.get_valueFunc(int(op2))
                    result = value1 / value2
                    self.memoryMap.set_valueFunc(int(res), result)
                ip += 1
            elif opr == '=':
                if func != 1:
                    value = self.memoryMap.get_value(int(op1))
                    self.memoryMap.set_value(int(res), value)
                else:
                    value = self.memoryMap.get_valueFunc(int(op1))
                    self.memoryMap.set_valueFunc(int(res), value)
                ip += 1
            elif opr == 'output':
                if func != 1:
                    print(self.memoryMap.get_value(int(res)))
                else:
                    print(self.memoryMap.get_valueFunc(int(res)))
                ip += 1
            elif opr == 'input': #se dejo a medias, solo están enteros y falta hacer lo de las funciones
               resType = int(res)
               ip += 1
               value = input()
               if (resType >= 1000 and resType < 2000) or (resType >= 5000 and resType < 6000) or (resType >= 9000 and resType < 10000):
                    try:
                        value = int(value)
                        self.memoryMap.set_value(int(res), value)
                    except Exception:
                        print("ERROR: El valor esperado tiene que ser INT")
                        break
            elif opr == '<':
                if func != 1:
                    value1 = self.memoryMap.get_value(int(op1))
                    value2 = self.memoryMap.get_value(int(op2))
                    result = value1 < value2 #bool
                    self.memoryMap.set_value(int(res), result)
                else:
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    value2 = self.memoryMap.get_valueFunc(int(op2))
                    result = value1 < value2 #bool
                    self.memoryMap.set_valueFunc(int(res), result)
                ip += 1
            elif opr == '>':
                if func != 1:
                    value1 = self.memoryMap.get_value(int(op1))
                    value2 = self.memoryMap.get_value(int(op2))
                    result = value1 > value2 #bool
                    self.memoryMap.set_value(int(res), result)
                else:
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    value2 = self.memoryMap.get_valueFunc(int(op2))
                    result = value1 > value2 #bool
                    self.memoryMap.set_valueFunc(int(res), result)
                ip += 1
            elif opr == '<=':
                if func != 1:
                    value1 = self.memoryMap.get_value(int(op1))
                    value2 = self.memoryMap.get_value(int(op2))
                    result = value1 <= value2 #bool
                    self.memoryMap.set_value(int(res), result)
                else: 
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    value2 = self.memoryMap.get_valueFunc(int(op2))
                    result = value1 <= value2 #bool
                    self.memoryMap.set_valueFunc(int(res), result)
                ip += 1
            elif opr == '>=':
                if func != 0:
                    value1 = self.memoryMap.get_value(int(op1))
                    value2 = self.memoryMap.get_value(int(op2))
                    result = value1 >= value2 #bool
                    self.memoryMap.set_value(int(res), result)
                else:
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    value2 = self.memoryMap.get_valueFunc(int(op2))
                    result = value1 >= value2 #bool
                    self.memoryMap.set_valueFunc(int(res), result)
                ip += 1
            elif opr == '==':
                if func != 1:
                    value1 = self.memoryMap.get_value(int(op1))
                    value2 = self.memoryMap.get_value(int(op2))
                    result = value1 == value2 #bool
                    self.memoryMap.set_value(int(res), result)
                else:
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    value2 = self.memoryMap.get_valueFunc(int(op2))
                    result = value1 == value2 #bool
                    self.memoryMap.set_valueFunc(int(res), result)
                ip += 1
            elif opr == 'gotoF':
                if func != 1:
                    value1 = self.memoryMap.get_value(int(op1))
                    if value1 == True:
                        ip += 1
                    else:
                        ip = int(res) - 1
                else:
                    value1 = self.memoryMap.get_valueFunc(int(op1))
                    if value1 == True:
                        ip += 1
                    else:
                        ip = int(res) - 1
            elif opr == 'era':
                func = 1
                fxName = op1
                ip += 1
            elif opr == 'gosub':
                bread_crumb = ip
                ip = int(res) - 1
                param = 0
            elif opr == 'endfunc':
                ip = bread_crumb + 1
                func = 0
            elif opr == 'param':
                param = param + 1
                value1 = self.memoryMap.get_value(int(op1))
                paramDir = self.memoryMap.get_paramDir(fxName, param)
                self.memoryMap.set_valueFunc(paramDir, value1)
                ip += 1
            elif opr == 'return':
                value = self.memoryMap.get_valueFunc(int(res))
                dir = self.memoryMap.get_returnDir(fxName)
                self.memoryMap.set_value(dir, value)
                fxName = ''
                ip += 1
            else:
                break

        



