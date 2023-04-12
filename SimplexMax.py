import numpy as np
import re

np.set_printoptions(precision=2, suppress=True)

def miVersion(x):
    #matriz de m *n | m = n° de variables | n = n° de restricciones
    #pattern = r'([-+]?\d*)[ ]*([a-zA-Z]\d+)[ ]*([=][-+]?\d+)'
    #r'(?<=\s)([-+]?\d*[a-zA-Z]\d*|[-+]?\d+)(?=\s|$)' 
    pattern = r'([-+]?\d*)\s*([a-zA-Z]\d+)|=\s*(\d+)'
    lines = x.strip().split('\n')
    vars = len(re.findall(pattern, lines[0]))
    max = False
    matriz = np.zeros((len(lines)-1, vars+len(lines)))
    i, j = [1,vars+1]

    print(vars)
    #funcion objetivo en la matriz tabular
    matriz[0][0]=1
    
    for match in re.findall(pattern, lines[0]):
        coeff_str, var, Lr = match
        coeff = int(coeff_str) if coeff_str not in ['','+','-'] else 1 if(coeff_str!='-') else -1
        matriz[0][int(var[1:])] = -coeff
        vars +=1


    #restricciones
    for line in lines[2:]:
        for match in re.findall(pattern, line):
            coeff_str, var, Lr = match
            if (Lr):
                matriz[i][len(matriz[i])-1] = Lr
            else:
                coeff = int(coeff_str) if coeff_str not in ['','+','-'] else 1 if(coeff_str!='-') else -1
                matriz[i][int(var[1:])] += coeff
        matriz[i][j] = 1
        i+=1
        j+=1
    print("Matriz inicial")
    print(matriz)
    Simplex(matriz, max)
    return matriz 

def Simplex(x,max):
    m = len(x[0])
    n = len(x)

    iteracion = 0
    while(True):
        fPiv = 0
        fPivValue = 0
        cPiv = 0
        cPivValue = -1

        if(max):
            for i in range(m):
                if (fPivValue>x[0][i]):
                    fPivValue = x[0][i]
                    fPiv = i
            if(fPiv==0):
                break
        
        else:
            for i in range(m):
                if (fPivValue<x[0][i]):
                    fPivValue = x[0][i]
                    fPiv = i
            if(fPiv==0):
                break
    
        for i in range(n):
            if (x[i][fPiv]>0):
                if(cPivValue>x[i][fPiv] or cPivValue<0):
                    cPivValue=x[i][m-1]/(x[i][fPiv])
                    cPiv = i
                
        Piv =x[cPiv][fPiv]
        for i in range(m):
            x[cPiv][i]= x[cPiv][i]/Piv

        for i in range(n):
            tPiv = x[i][fPiv]
            if (i != cPiv):
                for j in range(m):  
                    x[i][j]= x[i][j]-(x[cPiv][j]*tPiv)
        
        
        iteracion+=1
        print("iteracion numero",iteracion)
        print(x)
            

input_str = """maximize 2x1 - x2 
subject to
12x1 + 23x2  <= 15
22x1 -15x2 >= 100
12x1 <= 21
11x1 + 23x2 <= 60"""

miVersion(input_str)