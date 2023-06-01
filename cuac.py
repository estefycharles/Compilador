from semantic_cube import Semantic_cube

class Cuac:
    def __init__(self):
        self.opr = None #operator
        self.op1 = None #left operand 
        self.op2 = None #right operand
        self.res = None #result
        self.cuac = []
        self.countTemps = 1
        self.countCuacs = 1

    def create_cuac(self, opr, op1, op2, res):
        newCuac = [opr, op1, op2, res]
        self.cuac.append(newCuac)
        self.countCuacs += 1

    def add_temps(self):
        temp = f't{self.countTemps}'
        self.countTemps += 1
        return temp
    
    def fill(self, pendingCuac, dest):
        self.cuac[pendingCuac][3] = dest
    
    def getCuac(self):
        #return [self.opr, self.op1, self.op2, self.res]
        return self.cuac
    
    def print1(self):
        #print(self.cuac)
        x = 1
        for s in self.cuac:
            print(str(x)+'.',*s)
            x+=1




    
