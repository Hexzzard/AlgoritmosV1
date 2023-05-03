import numpy as np
import re

VBv = []; VBh = [] #VBv = Variables basicas como string de cada fila, VBh = en cada renglon
VBint = [] #VBint = Indice de variables verticales (tamaño n restricciones) segun se cambie con los pivotes
# (si la primera VB de los renglones se cambia por la primera variable 'x' , el primer valor será ese indice, osea 0 porque es la primera)
rengArr = [] #rengArr es segun las restricciones sean >= o <=, se agregan -1 1 para las var artificiales y 0 para las holguras normales.
iArt = [] #Indice de variables artificiales en VBv
xF = []; matriz = [] #xF es una matriz de los valores de las restricciones, coeficientes, >= o <= y LD, matriz es la matriz
z = []; #Serán los coeficientes de la funcion objetivo + el renglon completo despues

vars = 0; xHuelg = -1
#vars = numero de variables, xHuelg es el indice para incrementar la huelgura

"""Añade huelgura de la funcion objetivo como de las restricciones en una matriz, retornando el renglon correspondiente
Se pide 'renglon', siendo los coeficientes de cada variable, 'h' para saber si es la funcion objetivo o no como tambien 
para ver el indice para poner los -1 1 en las restricciones >= o solo 1 en restricciones <=, y 'rengArr' para ver los 
mismos indices junto con h"""
def añadir_huelgura(renglon, h, rengArr):
    
    """Si h = -1 se agrega a la funcion objetivo 0 y 1 correspondientes de holguras y variables artificiales,
    si h es 0 o mayor, osea son las restricciones, se agrega -1, 1 al indice de la restriccion que sea mayor o igual q,
    1 si es menor o igual que, para que quede como una matriz identidad según sean artificiales o no."""
    if h == -1:
        renglon.extend([0 if i == -1 else 1 if i == 1 else 0 for i in rengArr])
        return renglon

    for j in range(len(rengArr)):
        if h == j:
            if rengArr[j] == -1:
                renglon.extend([-1, 1])
            elif rengArr[j] == 0:
                renglon.append(1)
            continue
        if h + 1 == j:
            if rengArr[h] == -1:
                continue
        renglon.append(0)
    return renglon

"""Funcion que se llama para tener respuestas"""
def miVersion(x):
    hayMayor = False
    tempVBint = -1
    tempVBh = iArtemp = 1
    # matriz de m *n | m = n° de variables | n = n° de restricciones
    # r'([-+]?\d*\.?\d+)\s*([a-zA-Z]\d+)|=\s*([-+]?\d*\.?\d+)|([<>])')
    # r'([-+]?\d*)\s*([a-zA-Z]\d+)|=\s*(\d+)|([<>])'
    pattern = r'([-+]?\d*\.?\d+)\s*([a-zA-Z]\d+)|=\s*([-+]?\d*\.?\d+)|([<>])'
    #patron del hexa XD
    lines = x.strip().split('\n')
    vars = len(re.findall(pattern, lines[0]))
    max = re.search(r"^\w+", lines[0]).group() == "maximize"
    xHuelg = -1
    
    #Añade x1, x2, xn para tener los nombres de las variables en una lista
    for i in range(1, vars + 1):
        VBv.append(f'x{i}')
    
    #hh son los coeficientes de la función objetivo
    hh = re.findall(pattern, lines[0])
    #Se usan para hacer una matriz xF que es la matriz de restricciones pero ordenadas, como 
    #[[10, 5, '<', 500],[...], ...]
    #[[x1, x1, <>, LD], ...]
    for i in range(2, len(lines)):
        y = re.findall(pattern, lines[i])
        tem = 0
        xF.append([float(y[j][0]) if j < vars and y[j][0] != '' else 
                   float(y[j][len(y[0]) - 2]) if j == (len(y) - 1) else 
                   y[j][len(y[0]) - 1] if j == (len(y) - 2) else 0 for j in range(len(y))])

        for j in range(vars):
            if y[j+tem][1] == hh[j][1]:
                continue
            xF[i - 2].insert(j, 0)
            tem -= 1


    """Nombres horizontales y verticales variables básicas, y ademas calcula el numero de variables que tienen 
    mayor o igual que y menor o igual que haciendo un array de numeros que dan cuenta el numero de variables 
    artificiales o holguras
    iArt es el indice de las variables artificiales dentro de la matriz, para luego eliminar las variables"""
    for i in range(len(xF)):
        match xF[i][len(xF[i]) - 2]:
            case '>':
                tempVBint += 2
                rengArr.extend([-1, 1])
                if hayMayor == False:
                    hayMayor = True
                    zArtificial = [0] * vars
                VBv.extend([f'e{tempVBh}', f'a{tempVBh}'])
                VBh.append(f'a{tempVBh}')
                VBint.append(vars + tempVBint)
                iArt.append(vars + iArtemp)
                iArtemp += 2
                tempVBh += 1
            case '<':
                tempVBint += 1
                rengArr.append(0)
                VBv.append(f'h{tempVBh}')
                VBh.append(f'h{tempVBh}')
                VBint.append(vars + tempVBint)
                iArtemp += 1
                tempVBh += 1

    #Z son los coeficientes de la funcion objetivo
    z = [-float(i[0]) if max and hayMayor else -float(i[0]) if not max and not hayMayor else float(i[0]) for i in re.findall(pattern, lines[0])]

    """si zArtificial existe (solo existe si existe un mayor igual, es [0 veces el numero de variables]) se le añade
    huelgura sacando un renglon desde digamos 3 variables [0, 0, 0] y 4 restricciones menor o igual [0,0,0, 0, 0, 0, 0]
    luego se le arregla 0 porque esta lista debe existir en la primera fase del simplex
    z para la segunda fase, ya que tiene los coeficientes de la funcion objetivo que luego se quitaran, o si zArtificial
    no existe se hace el metodo simplex normal solo con z
    """
    try:
        zArtificial = añadir_huelgura(zArtificial, xHuelg, rengArr)
        zArtificial.append(0)
        z = añadir_huelgura(z, xHuelg, rengArr)
        z.append(0)
        xHuelg += 1
        matriz.insert(0, zArtificial)
    except NameError:
        z = añadir_huelgura(z, xHuelg, rengArr)
        z.append(0)
        xHuelg += 1
        matriz.insert(0, z)


    #Se añaden huelguras con añadir_huelguras a cada restriccion de la matriz xF
    for i in range(len(xF)):
        # renglon = [x1, x2, h1, ... , nRestric, LD]
        reng = añadir_huelgura([xF[i][j] for j in range(len(xF[i]) - 2)], xHuelg, rengArr)
        reng.append(xF[i][len(xF[i]) - 1])
        matriz.append(reng)
        if (xF[i][len(xF[i]) - 2]) == '>':
            xHuelg += 2
            continue
        xHuelg += 1

    #Si hay alguna restriccion mayor o igual, se inicia la segunda fase
    if hayMayor:
        return fase12(matriz, vars, z)

    #Si no solo simplex
    return Simplex(matriz, vars)


def fase12(matriz, vars, z):

    #Simple impresion por renglones en la matriz
    print("Fase 1\nMatriz Inicial")
    filas = ["", "Z"] + VBh
    col = VBv + ["LD"]
    Ematriz = np.hstack((np.array([filas]).reshape(-1, 1), np.vstack((col, np.round(matriz, 2)))))
    for fila in Ematriz:
        print(*fila, sep="\t", end="\n")
    print("\n")
    #Termina impresión

    #Se eliminan los 1 de la funcion objetivo de las variables artificiales
    for i in range(len(matriz) - 1):
        if xF[i][len(xF[i]) - 2] == '>':
            matriz[0] = [matriz[0][j] - matriz[i + 1][j] for j in range(len(matriz[i]))]

    #Primer simplex
    matt = Simplex(matriz)
    #Se ponen los indices de las variables en VBh -1 según hayan variables artificiales a su izquierda
    tVBi = [i for i in VBint]
    for i in range(len(iArt)):
        for j in range(len(VBint)):
            print(VBint[j])
            if VBint[j] > iArt[i]:
                tVBi[j] -= 1
    matt[0] = z

    #Se eliminan las variables artificiales de la matriz
    for i in range(len(matt)):
        for j in iArt[::-1]:
            del matt[i][j]

    #Y de la lista de las VBv
    for j in iArt[::-1]:
        del VBv[j]

    #Simple impresion por renglones en la matriz
    print("Fase 2\nMatriz Inicial")
    filas = ["", "Z"] + VBh
    col = VBv + ["LD"]
    Ematriz = np.hstack((np.array([filas]).reshape(-1, 1), np.vstack((col, np.round(matt, 2)))))
    for fila in Ematriz:
        print(*fila, sep="\t", end="\n")
    print("\n")
    #Termina impresion

    #Se borran las variables básicas luego de que se hayan agregado los coeficientes en la segunda fase, las que no sean
    #cero y estén en VBh tienen que ser 0
    for i in range(len(VBint)):
        num = tVBi[i]
        numZ = matt[0][num]
        menosMatriz = [j * numZ for j in matt[i+1]]
        print(menosMatriz)
        matt[0] = [round(matt[0][j] - menosMatriz[j]) if (
                0.000000001 > matt[0][j] - menosMatriz[j] > -0.000000000000000001)
                   else round(matt[0][j] - menosMatriz[j], 8)
        if str(matt[0][j] - menosMatriz[j])[::-1].find('.') > 8
        else matt[0][j] - menosMatriz[j] for j in range(len(matt[0]))]

    matt = Simplex(matt)
    
    LDx = [0] * vars
    for i in range(len(VBint)):
        for j in range(vars):
            if VBint[i] == j:
                LDx[j] = matt[i + 1][len(matt[0]) - 1]


    for i in range(vars):
        print(f'x{i}={LDx[i]}')
    iSombra = sombra = 0
    for i in range(vars, len(matt[0]) - 1):
        if matt[0][i] > sombra:
            sombra = matt[0][i]
            iSombra = i
    print(str(VBv[iSombra]) + " = " + str(sombra))
    return matt


def Simplex(matriz):
    it = 0
    for l in range(99):

        filas = ["", "Z"] + VBh
        col = VBv + ["LD"]
        Ematriz = np.hstack((np.array([filas]).reshape(-1, 1), np.vstack((col, np.round(matriz, 2)))))
        print(f"Iteracion {it}")
        for fila in Ematriz:
            print(*fila, sep="\t", end="\n")
        print("\n")
        it += 1
        pivot = 0; menorLD = 999999


        for i in range(len(matriz[0]) - 1):
            if matriz[0][i] < pivot+0.1:
                pivot = matriz[0][i]
                iVertPiv = i

        #Si el pivote sigue siendo igual a como se planteó al inicio del array se rompe el for loop (no se encontraron -)
        if pivot == 0:
            break

        #Se busca el menor lado derecho haciendo la division entre este y la fila pivote, iHorzPiv es el pivote renglon
        for i in range(1, len(matriz)):
            if matriz[i][iVertPiv] <= 0 or matriz[i][len(matriz[i]) - 1] <= 0:
                continue
            menorLDtest = matriz[i][len(matriz[i]) - 1] / matriz[i][iVertPiv]
            if menorLDtest < menorLD and menorLDtest >= 0:
                menorLD = menorLDtest
                iHorzPiv = i

        #Se pone el valor pivote vertical del renglon pivote en 1 dividiendo toda la lista en ese valor
        matriz[iHorzPiv] = [item / matriz[iHorzPiv][iVertPiv] for item in matriz[iHorzPiv]]

        #Se sacan los valores de arriba y abajo
        for i in range(len(matriz)):
            if i == iHorzPiv:
                continue

            num = matriz[i][iVertPiv]

            menosMatriz = [j * num for j in matriz[iHorzPiv]]
            # REDONDEO matriz, si los valores son casi infinitamente iguales a 0 pero "no lo son" se hacen 0,
            # si tienen muchos numeros despues de la coma, se redondean a menos decimales y si no se deja igual.
            matriz[i] = [round(matriz[i][j] - menosMatriz[j]) if (
                    0.000000001 > matriz[i][j] - menosMatriz[j] > -0.000000000000000001)
                         else round(matriz[i][j] - menosMatriz[j], 8)
            if str(matriz[i][j] - menosMatriz[j])[::-1].find('.') > 8
            else matriz[i][j] - menosMatriz[j] for j in range(len(menosMatriz))]
        if not iHorzPiv:
            print(1)
            break
        #Variable VBh se pone como la variable que se cambio, digamos que el pivote era la primera fila x1 se cambia el
        # nombre de la variable básica renglon pivote a ese x1
        VBh[iHorzPiv - 1] = VBv[iVertPiv]
        #Como tambien se guardan los indices de esos valores
        VBint[iHorzPiv - 1] = iVertPiv

    #Ultimo redondeo, antes se redondeó con 8 numeros y ahora con 5 para acotar la respuesta
    return [[round(xx, 5) for xx in aa] for aa in matriz]


# minimize
input = """maximize 2x1 -3x2 +3x3 = Z
subject to
1.2x1 +23x2 +20x3>= 150
22x1 -15x2 <= 100
12x1 <= 21
11x1 +23x2 +5x3 <= 60"""
input_str2 = """minimize 55x1 + 60x2 + 70x3
subject to
7x1 +4x2 +3x3 >= 600
1x1 +4x2 +2x3 >= 300
1x1 >= 40
1x2 <= 30
"""
input_str3 = """maximize 1500x1 + 1400x2 + 1600x3 + 1450x4
subject to
1x1 + 1x3 >= 40
1x2 + 1x4 >= 70
2x1 - 1x2 + 2x3 - 1x4 <= 0
1x1 + 1x2 <= 180
1x3 + 1x4 <= 45
"""
miVersion(input)
