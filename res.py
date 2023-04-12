import numpy as np
import re

np.set_printoptions(precision=2, suppress=True)
#pattern = r'([-+]?\d*)[ ]*([a-zA-Z]\d+)[ ]*([=][-+]?\d+)'
#r'(?<=\s)([-+]?\d*[a-zA-Z]\d*|[-+]?\d+)(?=\s|$)' 

def miVersion(x):
    #matriz de m *n | m = n° de variables | n = n° de restricciones
    pattern = r'([-+]?\d*)\s*([a-zA-Z]\d+)|=\s*(\d+)|([<>])'
   
    lines = x.strip().split('\n')
    print(re.findall(pattern, lines[2]))
    vars = len(re.findall(pattern, lines[0]))
    max =  re.search(r"^\w+", lines[0]).group() == "maximize"
    matriz = np.zeros((len(lines)-1, vars+len(lines)-1))
    i, j = [1,vars]

    #funcion objetivo en la matriz tabular
    
    for match in re.findall(pattern, lines[0]):
        coeff_str, var, Lr, exp = match
        coeff = int(coeff_str) if coeff_str not in ['','+','-'] else 1 if(coeff_str!='-') else -1
        matriz[0][int(var[1:])-1] = -coeff

    #restricciones
    for line in lines[2:]:
        inverted = 1
        for match in reversed(re.findall(pattern, line)):
            coeff_str, var, Lr, exp = match
            if (Lr or exp):
                if(exp=='>'):
                    inverted = -1
                    matriz[i][len(matriz[i])-1] *= -1
                if(Lr):
                    matriz[i][len(matriz[i])-1] = Lr
            else:
                coeff = int(coeff_str) if coeff_str not in ['','+','-'] else 1 if(coeff_str!='-') else -1
                matriz[i][int(var[1:])-1] += coeff*inverted
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

    while(iteracion<2):
        cPivValue = cPiv = fPiv = fPivValue = -1

        if(max):
            for i in range(m):
                if (fPivValue>x[0][i]):
                    fPivValue = x[0][i]
                    fPiv = i
            if(fPiv==-1):
                break
        
        else:
            for i in range(m):
                if (fPivValue<x[0][i]):
                    fPivValue = x[0][i]
                    fPiv = i
            if(fPiv==0):
                break
        
        for i in range(1,n):
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
            
#minimize
input = """maximize 2x1 -3x2 +3x3 = Z
subject to
12x1 +23x2 +20x3>= 15
22x1 -15x2 <= 100
12x1 <= 21
11x1 +23x2 +5x3 <= 60"""

miVersion(input)