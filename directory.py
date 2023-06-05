import json
class Directory:
    #name       type        dirV        resources        param      vars
    #string     string      int         []               []         []

    def __init__(self):
        self.fx = {}
        self.classes = {}
        self.main = {}
        self.classVars = {}
        self.scope = ''
        self.functionName = ''
        self.className = ''
        self.fxParams = {}
        self.cte = {}
        self.globalVar ={}

    #fx scope   class scope     main scope
    def set_scope(self, scope):
        self.scope = scope
    
    def set_functionName(self, name):
        self.functionName = name
    
    def set_className(self, name):
        self.className = name

    def set_fxParams(self, name, fxParams):
        self.fxParams[name] = fxParams

    def get_fxParams(self, name):
        return self.fxParams[name] 

    def add_function(self, name, type, dirI):
        add = {'fx type':type, 'params': {}, 'vars': {}, 'dirI': dirI}
        if self.scope == 'fx':
            self.fx[name] = add
        else:
            self.classes[self.className]['fx'][name] = add

    def add_class(self, name):
        self.classes[name] = {'vars':{}, 'fx':{}}

    def add_var(self, name, type, internalScope, dirV, dim):
        add = {'type': type, 'dirV': dirV, 'dim': dim}
        if self.scope == 'main':
            self.main[name] = add
        elif self.scope == 'fx':
            self.fx[self.functionName]['vars'][name] = add
        elif self.scope == 'class':
            if internalScope == 'fx':
                self.classes[self.className]['fx'][self.functionName]['vars'][name] = add
            elif internalScope == 'class':
                self.classes[self.className]['vars'][name] = add

    #numparam se refiere al numero de parametro, esto para poder identificarlo
    def add_param(self, type, numParam, dirV):
        add = {'type':type, 'dirV': dirV}
        if self.scope == 'fx':
            self.fx[self.functionName]['params'][numParam] = add
        elif self.scope == 'class':
            self.classes[self.className]['fx'][self.functionName]['params'][numParam] = add

    def add_classVars(self, name, className):
        add = {'className' : className}
        self.classVars[name] = add

    def add_cte(self, value, dirV):
        add = {'dirV':dirV}
        self.cte[value] = add 
    
    def add_global(self, fxName, dirV):
        add = {'dirV':dirV}
        self.globalVar[fxName] = add 

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
        
    def exists_cte(self, value):
        return value in self.cte
            
    def get_varType(self, name, internalScope):
        if self.scope == 'main':
            return self.main[name]['type']
        elif self.scope == 'fx':
            return self.fx[self.functionName]['vars'][name]['type']
        elif self.scope == 'class':
            if internalScope == 'fx':
                return self.classes[self.className]['fx'][self.functionName]['vars'][name]['type']
            elif internalScope == 'class':
                return self.classes[self.className]['vars'][name]['type']

    def get_fxType(self, name):
        return self.fx[name]['fx type']

    def get_dirI(self, name): #gets the direction where a fx starts
        return self.fx[name]['dirI']
    
    def get_paramType(self, name, numParam):
        return self.fx[name]['params'][numParam]['type']
            
    def get_varDirV(self, name, internalScope):
        if self.scope == 'main':
            return self.main[name]['dirV']
        elif self.scope == 'fx':
            return self.fx[self.functionName]['vars'][name]['dirV']
        elif self.scope == 'class':
            if internalScope == 'fx':
                return self.classes[self.className]['fx'][self.functionName]['vars'][name]['dirV']
            elif internalScope == 'class':
                return self.classes[self.className]['vars'][name]['dirV']
            
    def get_cteDirV(self, value):
        return self.cte[value]['dirV']
    
    def get_globalDirV(self, fxName):
        return self.globalVar[fxName]['dirV']

    def get_main(self): #genera el diccionario de main en una lista
        list = [] 
        for key, val in self.main.items(): 
            list.append([key, val]) 
        return list
    
    def get_cte(self): #genera el diccionario de constantes en una lista
        list = [] 
        for key, val in self.cte.items(): 
            list.append([key, val]) 
        return list
    
    def get_fx(self): #genera el diccionario de constantes en una lista
        list = [] 
        for key, val in self.fx.items(): 
            list.append([key, val]) 
        return list
    
    def get_global(self): #genera el diccionario de constantes en una lista
        list = [] 
        for key, val in self.globalVar.items(): 
            list.append([key, val]) 
        return list


    def print_dict(self):
        print("DIRECTORIO: ")
        #print(json.dumps(self.classes, indent = 4))
        print(json.dumps(self.fx, indent = 4))
        print(json.dumps(self.main, indent = 4))
        #print(json.dumps(self.classVars, indent = 4))
        print(json.dumps(self.cte, indent = 4))
        print(json.dumps(self.globalVar, indent = 4))

 
