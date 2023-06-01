class MemoryMap:
     #en esta clase vamos a estar haciendo set y get de valores y seutiliza dentro de la máquina virtual

    def __init__(self):
        self.int = {}
        self.dec = {}
        self.cteMem = []

    
    def get_value(self, dir):
        if (dir >= 1000 and dir < 2000) or (dir >= 5000 and dir < 6000) or (dir >= 9000 and dir < 10000): #int
            return self.int[dir]
        elif (dir >= 2000 and dir < 3000) or (dir >= 6000 and dir < 7000) or (dir >= 10000 and dir < 11000): #dec
            return self.dec[dir]
        
    def set_value(self, dir, value):
        if (dir >= 1000 and dir < 2000) or (dir >= 5000 and dir < 6000) or (dir >= 9000 and dir < 10000): #int
            self.int[dir] = value
        elif (dir >= 2000 and dir < 3000) or (dir >= 6000 and dir < 7000) or (dir >= 10000 and dir < 11000):
            self.dec[dir] = value

    def set_cte(self, list):
        self.cteMem = list

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
