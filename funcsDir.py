class FuncsDir:
    #name       type        dirI        resources        param      vars
    #string     string      int         []               []         []

    def __init__(self):
        self.funcsDir = {}

    def add_function(self, name, type, params):
        self.funcsDir[name] = [type, params]

    def get_function_type(self, name):
        return self.funcsDir.get(name)
    
    def get_function_params(self, name):
        return self.funcsDir.get(name)
    
    def print_dict(self):
        for value in self.funcsDir.items():
            print(value)
    

class TypeDir:
    def __init__(self):
        self.type = []

    def set_type(self,type):
        self.type.append(type)
    
    
    def get_type(self, pos):
        return self.type[pos]
    
    def delete_type(self):
        self.type.clear()

    
class VarsTable:
    #name       type        dir  
    #string     string      int 

    def __init__(self):
        self.varsTable = {}

    def add_var(self, name, type):
        self.varsTable[name] = [type]

    def get_var_type(self, name):
        return self.varsTable.get(name)
    
    def print_dict(self):
        for value in self.varsTable.items():
            print(value)
    

   # def __init__(self):
    #    self.nameF = "nameF"
     #   self.typeF = "typeF"
      #  self.dirI = 0
       # self.resources = list
        #self.params = list
        #self.vars = list

#    def set_nameF(self,nameF):
#        self.nameF = nameF
    
 #   def get_nameF(self):
 #       return self.nameF

 #   def get_type(self):
  #      return self.type

