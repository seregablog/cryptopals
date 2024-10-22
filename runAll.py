from pathlib import Path
import os

result = list(Path("cryptopals").rglob("*.py"))

for file in result:
    fileName = str(file)
    print('Run file:', fileName)
    code = os.system("python3 " + fileName)
    print('Code:', str(code), "\n")
    if code != 0:
        break
