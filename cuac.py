from semantic_cube import Semantic_cube

class Cuac:
    def __init__(self):
        self.opr = None #operator
        self.op1 = None #left operand 
        self.op2 = None #right operand
        self.res = None #result
        self.cuac = []
        self.count = 1

    def create_cuac(self, opr, op1, op2, res):
        newCuac = [opr, op1, op2, res]
        self.cuac.append(newCuac)
    
    def add_temps(self):
        temp = f't{self.count}'
        self.count += 1
        return temp
    
    def goto(self):
        self.opr = 'GOTO'
        self.op1 = None
        self.op2 = None
        self.res = None
        return self
    
    def gotoF(self, temp):
        self.opr = 'GOTOF'
        self.op1 = temp
        self.op2 = None
        self.res = None
        return self
    
    def output(self, res):
        self.opr = 'PRINT'
        self.op1 = None
        self.op2 = None
        self.res = res
        return self

    def getCuac(self):
        return (self.opr, self.op1, self.op2, self.res)
    
    def print1(self):
        print(self.cuac)
        for s in self.cuac:
            print(*s)




    
