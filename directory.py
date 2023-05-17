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
        add = {'fx type':type, 'params': {}, 'vars': {}}
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

    def add_param(self, type, name):
        add = {'type':type}
        #add = type
        print("EL SCOPE ES: ", self.scope)
        print("EL TIPO ES: ", type)
        if self.scope == 'fx':
            self.fx[self.functionName]['params'][name] = add
        elif self.scope == 'class':
            print('SI ENTREEEEE', self.className, self.functionName, type)
            self.classes[self.className]['fx'][self.functionName]['params'][name] = add

    def print_dict(self):
        #for value in self.fx.items():
        #    print(value)
        print("DICCIONARIO: ")
        print(json.dumps(self.classes, indent = 4))
        print(json.dumps(self.fx, indent = 4))
 
