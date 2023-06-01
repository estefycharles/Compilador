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

    def get_cte_list(self):
        return self.cteList
    
    def set_cte_value(self, op1):
        if int(op1) > 9000 and int(op1) < 10000:
            #ir al dirFuncs y traer la variable que este alamacenada en esa dir
            for inner_list in self.cteList:
                if int(op1) in inner_list[1].values():
                    value = inner_list[0]
                    op1I = int(value)
            
        
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
            elif opr == '-':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 - value2
                self.memoryMap.set_value(int(res), result)
            elif opr == '*':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 * value2
                self.memoryMap.set_value(int(res), result)
            elif opr == '/':
                value1 = self.memoryMap.get_value(int(op1))
                value2 = self.memoryMap.get_value(int(op2))
                result = value1 / value2
                self.memoryMap.set_value(int(res), result)
            elif opr == '=':
                value = self.memoryMap.get_value(int(op1))
                self.memoryMap.set_value(int(res), value)
            elif opr == 'output':
                print(self.memoryMap.get_value(int(res)))
                

            if opr != 'goto':
                ip += 1




