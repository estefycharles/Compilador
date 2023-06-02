from directory import Directory
from memory_map import MemoryMap

directory = Directory()

class VirtualMachine:

    def __init__(self):
        self.cuacs = []
        self.mainList = []
        self.cteList = []
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
        
#text file
#funciones
    def execute(self):
        print("----------------------- FRANK O> -----------------------")
        self.memoryMap.set_cte(self.cteList)
        self.memoryMap.set_cte_memory()
        cuacs = self.load_cuacs('pato.txt')
        ip = 0 
        while(ip < len(cuacs)):
            opr, op1, op2, res = cuacs[ip]
            if opr == 'goto':
                #salta a la linea # (res)
                ip = int(res) - 1
            elif opr == '+':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 + value2
                self.memoryMap.set_value(int(res), result)
                ip += 1
            elif opr == '-':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 - value2
                self.memoryMap.set_value(int(res), result)
                ip += 1
            elif opr == '*':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 * value2
                self.memoryMap.set_value(int(res), result)
                ip += 1
            elif opr == '/':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 / value2
                self.memoryMap.set_value(int(res), result)
                ip += 1
            elif opr == '=':
                value = self.memoryMap.get_value(int(op1))
                self.memoryMap.set_value(int(res), value)
                ip += 1
            elif opr == 'output':
                print(self.memoryMap.get_value(int(res)))
                ip += 1
            elif opr == 'input': #se dejo a medias, solo están enteros
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
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 < value2 #bool
                self.memoryMap.set_value(int(res), result)
                ip += 1
            elif opr == '>':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 > value2 #bool
                self.memoryMap.set_value(int(res), result)
                ip += 1
            elif opr == '<=':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 <= value2 #bool
                self.memoryMap.set_value(int(res), result)
                ip += 1
            elif opr == '>=':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 >= value2 #bool
                self.memoryMap.set_value(int(res), result)
                ip += 1
            elif opr == '==':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 == value2 #bool
                self.memoryMap.set_value(int(res), result)
                ip += 1
            elif opr == 'gotoF':
                value1 = self.memoryMap.get_value(int(op1))
                if value1 == True:
                    ip += 1
                else:
                    ip = int(res) - 1
                
            else:
                break

        



