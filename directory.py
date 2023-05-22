import json
class Directory:
    #name       type        dirI        resources        param      vars
    #string     string      int         []               []         []

    def __init__(self):
        self.fx = {}
        self.classes = {}
        self.main = {}
        self.classVars = {}
        self.scope = ''
        self.functionName = ''
        self.className = ''

    #fx scope   class scope     main scope
    def set_scope(self, scope):
        self.scope = scope
    
    def set_functionName(self, name):
        self.functionName = name
    
    def set_className(self, name):
        self.className = name

    def add_function(self, name, type):
        add = {'fx type':type, 'params': {}, 'vars': {}}
        if self.scope == 'fx':
            self.fx[name] = add
        else:
            self.classes[self.className]['fx'][name] = add

    def add_class(self, name):
        self.classes[name] = {'vars':{}, 'fx':{}}

    def add_var(self, name, type, internalScope):
        add = {'type': type}
        if self.scope == 'main':
            self.main[name] = add
        elif self.scope == 'fx':
            self.fx[self.functionName]['vars'][name] = add
        elif self.scope == 'class':
            if internalScope == 'fx':
                self.classes[self.className]['fx'][self.functionName]['vars'][name] = add
            elif internalScope == 'class':
                self.classes[self.className]['vars'][name] = add

    def add_param(self, type, name):
        add = {'type':type}
        if self.scope == 'fx':
            self.fx[self.functionName]['params'][name] = add
        elif self.scope == 'class':
            self.classes[self.className]['fx'][self.functionName]['params'][name] = add

    def add_classVars(self, name, className):
        add = {'className' : className}
        self.classVars[name] = add

    def exists_fx(self, name): 
        if self.scope == 'class':  
            return name in self.classes[self.className]['fx']
        else:
            return name in self.fx
        
    def exists_class(self, name): 
        return name in self.classes
    
    def exists_classVars(self, name):
        return name in self.classVars
    
    def exists_var(self, name, internalScope):
        if self.scope == 'main':
            return name in self.main
        elif self.scope == 'fx':
            return name in self.fx[self.functionName]['vars']
        elif self.scope == 'class':
            if internalScope == 'fx':
                return name in self.classes[self.className]['fx'][self.functionName]['vars']
            elif internalScope == 'class':
                return name in self.classes[self.className]['vars']
            
    def get_varType(self, name, internalScope):
        if self.scope == 'main':
            return self.main[name]['type']
        elif self.scope == 'fx':
            return self.fx[self.functionName]['vars']['type']
        elif self.scope == 'class':
            if internalScope == 'fx':
                return self.classes[self.className]['fx'][self.functionName]['vars']['type']
            elif internalScope == 'class':
                return self.classes[self.className]['vars']['type']
            

    def print_dict(self):
        print("DICCIONARIO: ")
        print(json.dumps(self.classes, indent = 4))
        print(json.dumps(self.fx, indent = 4))
        print(json.dumps(self.main, indent = 4))
        print(json.dumps(self.classVars, indent = 4))
 
