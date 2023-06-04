class MemoryMap:
     #en esta clase vamos a estar haciendo set y get de valores y seutiliza dentro de la máquina virtual

    def __init__(self):
        self.int = {}
        self.dec = {}
        self.bool = {}
        self.string = {}
        self.intF = {}
        self.decF = {}
        self.boolF = {}
        self.stringF = {}
        self.cteMem = []
        self.fxMem = []
        self.globalMem = []

    
    def get_value(self, dir):
        if (dir >= 1000 and dir < 2000) or (dir >= 5000 and dir < 6000) or (dir >= 9000 and dir < 10000) or (dir >= 13000 and dir <14000): #int
            return self.int[dir]
        elif (dir >= 2000 and dir < 3000) or (dir >= 6000 and dir < 7000) or (dir >= 10000 and dir < 11000) or (dir >= 14000 and dir <15000): #dec
            return self.dec[dir]
        elif (dir >= 3000 and dir < 4000) or (dir >= 7000 and dir < 8000) or (dir >= 11000 and dir < 12000) or (dir >= 15000 and dir <16000): #bool
            return self.bool[dir]
        elif (dir >= 4000 and dir < 5000) or (dir >= 8000 and dir < 9000) or (dir >= 12000 and dir < 13000) or (dir >= 16000 and dir <17000): #string
            return self.string[dir]
        
    def set_value(self, dir, value):
        if (dir >= 1000 and dir < 2000) or (dir >= 5000 and dir < 6000) or (dir >= 9000 and dir < 10000) or (dir >= 13000 and dir <14000): #int
            self.int[dir] = value
        elif (dir >= 2000 and dir < 3000) or (dir >= 6000 and dir < 7000) or (dir >= 10000 and dir < 11000) or (dir >= 14000 and dir <15000):
            self.dec[dir] = value
        elif (dir >= 3000 and dir < 4000) or (dir >= 7000 and dir < 8000) or (dir >= 11000 and dir < 12000) or (dir >= 15000 and dir <16000): #bool
            self.bool[dir] = value
        elif (dir >= 4000 and dir < 5000) or (dir >= 8000 and dir < 9000) or (dir >= 12000 and dir < 13000) or (dir >= 16000 and dir <17000): #string
            self.string[dir] = value

    def get_valueFunc(self, dir):
        if (dir >= 1000 and dir < 2000) or (dir >= 5000 and dir < 6000) or (dir >= 9000 and dir < 10000) or (dir >= 13000 and dir <14000): #int
            return self.intF[dir]
        elif (dir >= 2000 and dir < 3000) or (dir >= 6000 and dir < 7000) or (dir >= 10000 and dir < 11000) or (dir >= 14000 and dir <15000): #dec
            return self.decF[dir]
        elif (dir >= 3000 and dir < 4000) or (dir >= 7000 and dir < 8000) or (dir >= 11000 and dir < 12000) or (dir >= 15000 and dir <16000): #bool
            return self.boolF[dir]
        elif (dir >= 4000 and dir < 5000) or (dir >= 8000 and dir < 9000) or (dir >= 12000 and dir < 13000) or (dir >= 16000 and dir <17000): #string
            return self.stringF[dir]
        
    def set_valueFunc(self, dir, value):
        if (dir >= 1000 and dir < 2000) or (dir >= 5000 and dir < 6000) or (dir >= 9000 and dir < 10000) or (dir >= 13000 and dir <14000): #int
            self.intF[dir] = value
        elif (dir >= 2000 and dir < 3000) or (dir >= 6000 and dir < 7000) or (dir >= 10000 and dir < 11000) or (dir >= 14000 and dir <15000):
            self.decF[dir] = value
        elif (dir >= 3000 and dir < 4000) or (dir >= 7000 and dir < 8000) or (dir >= 11000 and dir < 12000) or (dir >= 15000 and dir <16000): #bool
            self.boolF[dir] = value
        elif (dir >= 4000 and dir < 5000) or (dir >= 8000 and dir < 9000) or (dir >= 12000 and dir < 13000) or (dir >= 16000 and dir <17000): #string
            self.stringF[dir] = value

    def set_cte(self, list):
        self.cteMem = list

    def set_fxMem(self, list):
        self.fxMem = list

    def set_globalMem(self, list):
        self.globalMem = list
    
    def print(self):
        print(self.globalMem)
        print(self.fxMem)

    def get_paramDir(self, fxName, numberParam):
        for item in self.fxMem:
            if item[0] == fxName:
                params = item[1]['params']
                if numberParam in params:
                    dirV = params[numberParam]['dirV']
                    break
        return dirV
    
    def get_returnDir(self, fxName):
        for entry in self.globalMem:
            if entry[0] == fxName:  # Check if the first element matches the name
                dirV = entry[1]['dirV']
                break
        return dirV
    

    def set_cte_memory(self):
        for element in self.cteMem:
            if 'dirV' in element[1]:  # Check if 'dirV' key exists in the dictionary
                dir = element[1]['dirV']
                if dir >= 9000 and dir < 10000: #int
                    value = element[0]
                    self.int[dir] = int(value)
                elif dir >= 10000 and dir < 11000: #dec
                    value = element[0]
                    self.dec[dir] = float(value)
                elif dir >= 11000 and dir < 12000: #bool
                    value = element[0]
                    self.bool[dir] = str(value)
                elif dir >= 12000 and dir < 13000: #string
                    value = element[0]
                    self.string[dir] = str(value)
    
    def set_cte_memoryFx(self):
        for element in self.cteMem:
            if 'dirV' in element[1]:  # Check if 'dirV' key exists in the dictionary
                dir = element[1]['dirV']
                if dir >= 9000 and dir < 10000: #int
                    value = element[0]
                    self.intF[dir] = int(value)
                elif dir >= 10000 and dir < 11000: #dec
                    value = element[0]
                    self.decF[dir] = float(value)
                elif dir >= 11000 and dir < 12000: #bool
                    value = element[0]
                    self.boolF[dir] = str(value)
                elif dir >= 12000 and dir < 13000: #string
                    value = element[0]
                    self.stringF[dir] = str(value)
