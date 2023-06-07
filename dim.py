import json

class Dimension:
    def __init__(self):
        self.dim = {}

    def set_dim(self, arrName, limInf, limSup):
        add = {'limInf': limInf, 'limSup': limSup}
        self.dim[arrName] = add
    
    def get_limInf(self, arrName):
        return self.dim[arrName]['limInf']
    
    def get_limSup(self, arrName):
        return self.dim[arrName]['limSup']
    
    def print_dim(self):
        print("DIMENSIONES: ")
        print(json.dumps(self.dim, indent = 4))