import parserr
import sys
import os

folder_path = "../Compilador/test/"  # Specify the path to the folder containing the archives
fkArchive = []

if len(sys.argv) > 1:
    fkArchive.append(str(sys.argv[1]))
else:
    fkArchive = os.listdir(folder_path)

for archive_name in fkArchive:
    archive_path = os.path.join(folder_path, archive_name)
    try:
        with open(archive_path) as f:
            data = f.read()
            result = parserr.runParser.parse(data)
    except FileNotFoundError:
        print("Cuack cuack cuack... File does not exist:", archive_path)
        sys.exit(1)
    except Exception as e:
        print("Cuack cuack cuack... An error occurred while processing the file:", archive_path)
        print("Cuack cuack cuack... Error message:", str(e))
        sys.exit(1)