import parserr
import sys

fkArchive = ['factorial_ciclo.fk', 
         'factorial_recursivo.fk',
         'fibonacci_ciclo.fk',
         'fibonacci_recursivo.fk',
         'fx_return.fk']
if 1<len(sys.argv):
    fkArchive = [str(sys.argv[1])]

for i in fkArchive:
    with open('../Compilador/test/'f'{i}') as f:
        try:
            data = f.read()
            f.close()
            result = parserr.runParser.parse(data)
        except Exception:
            print("Cuack cuack cuack... File does not exist")
            sys.exit(1)