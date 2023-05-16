import json
class Directory:
    #name       type        dirI        resources        param      vars
    #string     string      int         []               []         []

    def __init__(self):
        self.fx = {}
        self.classes = {}
        self.vars = {}
        self.scope = ''
        self.functionName = ''
        self.className = ''

    #fx scope   class scope     main scope
    def set_scope(self, scope):
        self.scope = scope
    
    def set_functionName(self, name):
        self.functionName = name
        print("ENTREE CON: ", name)
    
    def set_className(self, name):
        self.className = name

    def add_function(self, name, type):
        add = {'fx type':type, 'vars': {}}
        if self.scope == 'fx':
            self.fx[name] = add
        else:
            self.classes[self.className]['fx'][name] = add

    def add_class(self, name):
        self.classes[name] = {'vars':{}, 'fx':{}}

    def add_var(self, name, type, internalScope):
        add = {'type': type}
        if self.scope == 'fx':
            self.fx[self.functionName]['vars'][name] = add
        elif self.scope == 'class':
            if internalScope == 'fx':
                self.classes[self.className]['fx'][self.functionName]['vars'][name] = add
            elif internalScope == 'class':
                self.classes[self.className]['vars'][name] = add

    def print_dict(self):
        #for value in self.fx.items():
        #    print(value)
        print("DICCIONARIO: ")
        #print(json.dumps(self.classes, indent = 4))
        print(json.dumps(self.fx, indent = 4))
    

class TypeDir:
    def __init__(self):
        self.type = []

    def set_type(self,type):
        self.type.append(type)
    
    def get_type(self, pos):
        return self.type[pos]
    
    def delete_type(self):
        self.type.clear()



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

