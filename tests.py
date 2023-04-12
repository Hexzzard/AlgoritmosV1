import numpy as np
import re

def miVersion(x):
    #matriz de m *n | m = n° de variables | n = n° de restricciones
    #pattern = r'([-+]?\d*)[ ]*([a-zA-Z]\d+)[ ]*([=][-+]?\d+)'
    Apattern = r'([-+]?\d*)[ ]*([a-zA-Z]\d+)'
    bpattern = r'([=][-+]?\d+)'
    b = re.search(bpattern, "2x1 + 5x2 >= 1")
    print(b)
    lines = x.strip().split('\n')
    matriz = np.zeros((len(lines)-1, 3+len(lines)-2+1))
    i = 0
    for line in lines[2:]:
        for match in re.findall(Apattern, line):
            coeff_str, var = match
            print(coeff_str)
            coeff = int(coeff_str) if coeff_str not in ['','+','-'] else 1 if(coeff_str!='-') else -1
            matriz[i][int(var[1:])-1] = coeff
        i+=1
    return matriz 

input_str = """maximize 2x1 - x2 + 4x3
subject to
x1 + x2 + x3 <= 5
2x1 - x2 + 3x3 >= 0
x1 - x3 <= 2
x1, x2, x3 >= 0"""


print(miVersion(input_str))