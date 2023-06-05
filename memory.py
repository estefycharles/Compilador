class MemoryAddress:
    def __init__(self):
        self.localInt = 1000
        self.localDec = 2000
        self.localBool = 3000
        self.localString = 4000

        self.localIntTemp = 5000
        self.localDecTemp = 6000
        self.localBoolTemp = 7000
        self.localStringTemp = 8000

        self.constInt = 9000
        self.constDec = 10000
        self.constBool = 11000
        self.constString = 12000

        self.globalInt = 13000
        self.globalDec = 14000
        self.globalBool = 15000
        self.globalString = 16000

    def local_memory(self, varType, varSize):
        if varType == 'int':
            self.localInt += varSize
            if self.localInt > self.localDec:
                print('ERROR: Out of memory')
            else:
                return self.localInt
        elif varType == 'dec':
            self.localDec += varSize
            if self.localDec > self.localBool:
                print('ERROR: Out of memory')
            else:
                return self.localDec
        elif varType == 'bool':
            self.localBool += varSize
            if self.localBool > self.localString:
                print('ERROR: Out of memory')
            else:
                return self.localBool
        elif varType == 'string':
            self.localString += varSize
            if self.localString > self.localIntTemp:
                print('ERROR: Out of memory')
            else:
                return self.localString
    
    def const_memory(self, consType):
        if consType == 'int':
            self.constInt += 1
            if self.constInt > self.constDec:
                print('ERROR: Out of memory')
            else:
                return self.constInt
        elif consType == 'dec':
            self.constDec += 1
            if self.constDec > self.constBool:
                print('ERROR: Out of memory')
            else:
                return self.constDec
        elif consType == 'bool':
            self.constBool += 1
            if self.constBool > self.constString:
                print('ERROR: Out of memory')
            else:
                return self.constBool
        elif consType == 'string':
            self.constString += 1
            if self.constString > self.globalInt:
                print('ERROR: Out of memory')
            else:
                return self.constString
        
    def temp_memory(self, tempType):
        if tempType == 'int':
            self.localIntTemp += 1
            if self.localIntTemp > self.localDecTemp:
                print('ERROR: Out of memory')
            else:
                return self.localIntTemp
        elif tempType == 'dec':
            self.localDecTemp += 1
            if self.localDecTemp > self.localBoolTemp:
                print('ERROR: Out of memory')
            else:
                return self.localDecTemp
        elif tempType == 'bool':
            self.localBoolTemp += 1
            if self.localBoolTemp > self.localStringTemp:
                print('ERROR: Out of memory')
            else:
                return self.localBoolTemp
        elif tempType == 'string':
            self.localStringTemp += 1
            if self.localStringTemp > self.constInt:
                print('ERROR: Out of memory')
            else:
                return self.localStringTemp
            
    def global_memory(self, globalType):
        if globalType == 'int':
            self.globalInt += 1
            if self.globalInt > self.globalDec:
                print('ERROR: Out of memory')
            else:
                return self.globalInt
        elif globalType == 'dec':
            self.globalDec += 1
            if self.globalDec > self.globalBool:
                print('ERROR: Out of memory')
            else:
                return self.globalDec
        elif globalType == 'bool':
            self.globalBool += 1
            if self.globalBool > self.globalString:
                print('ERROR: Out of memory')
            else:
                return self.globalBool
        elif globalType == 'string':
            self.globalString += 1
            if self.globalString > 17000:
                print('ERROR: Out of memory')
            else:
                return self.globalString

    def delete_localMemory(self):
        self.localInt = 1000
        self.localDec = 2000
        self.localBool = 3000
        self.localString = 4000
        self.localIntTemp = 5000
        self.localDecTemp = 6000
        self.localBoolTemp = 7000
        self.localStringTemp = 8000

