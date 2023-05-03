import numpy as np
import re

VBv = []; VBh = []; VBintT = []; VBint = []; rengArr = []; iArt = []; xF = []; z = []; matriz = []
vars = max = 0; xHuelg = -1

def añadir_huelgura(renglon, h, rengArr):
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

def miVersion(x):
    hayMayor = False
    tempVBh = 1
    tempVBint = -1
    newTemp = 1
    # matriz de m *n | m = n° de variables | n = n° de restricciones
    # r'([-+]?\d*\.?\d+)\s*([a-zA-Z]\d+)|=\s*([-+]?\d*\.?\d+)|([<>])')
    # r'([-+]?\d*)\s*([a-zA-Z]\d+)|=\s*(\d+)|([<>])'
    pattern = r'([-+]?\d*\.?\d+)\s*([a-zA-Z]\d+)|=\s*([-+]?\d*\.?\d+)|([<>])'
    # [ numero (decimal), letra (x1, x2), LD, > o <]

    lines = x.strip().split('\n')
    vars = len(re.findall(pattern, lines[0]))
    max = re.search(r"^\w+", lines[0]).group() == "maximize"
    xHuelg = -1

    for i in range(1, vars + 1):
        VBv.append(f'x{i}')

    hh = re.findall(pattern, lines[0])
    for i in range(2, len(lines)):
        y = re.findall(pattern, lines[i])
        tem = 0
        xF.append([float(y[j][0]) if j < vars and y[j][0] != '' else float(y[j][len(y[0]) - 2]) if j == (
                    len(y) - 1) else y[j][len(y[0]) - 1] if j == (len(y) - 2) else 0 for j in range(len(y))])

        for j in range(vars):
            if tem > 0:
                tem -= 1
                continue
            if y[j][1] == hh[j][1]:
                continue
            for k in range(j, vars):
                if y[j][1] == hh[k][1]:
                    break
                xF[i - 2].insert(k, 0)
                tem += 1

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
                VBintT.append(vars + newTemp)
                newTemp += 1
                tempVBh += 1
            case '<':
                tempVBint += 1
                rengArr.append(0)
                VBv.append(f'h{tempVBh}')
                VBh.append(f'h{tempVBh}')
                VBint.append(vars + tempVBint)
                newTemp += 1
                tempVBh += 1

    z = [-float(i[0]) if max and hayMayor else -float(i[0]) if not max and not hayMayor else float(i[0]) for i in re.findall(pattern, lines[0])]

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

    for i in range(len(rengArr)):
        if rengArr[i] == 1:
            iArt.append(vars + i)

    for i in range(len(xF)):
        # renglon = [x1, x2, h1, ... , nRestric, LD]
        reng = añadir_huelgura([xF[i][j] for j in range(len(xF[i]) - 2)], xHuelg, rengArr)
        reng.append(xF[i][len(xF[i]) - 1])
        matriz.append(reng)
        if (xF[i][len(xF[i]) - 2]) == '>':
            xHuelg += 2
            continue
        xHuelg += 1

    if hayMayor:
        return fase12(matriz, vars, z)


    return Simplex(matriz, vars)


def fase12(matriz, vars, z):
    print("Fase 1\nMatriz Inicial")
    filas = ["", "Z"] + VBh
    col = VBv + ["LD"]
    Ematriz = np.hstack((np.array([filas]).reshape(-1, 1), np.vstack((col, np.round(matriz, 2)))))
    for fila in Ematriz:
        print(*fila, sep="\t", end="\n")
    print("\n")

    for i in range(len(matriz) - 1):
        if xF[i][len(xF[i]) - 2] == '>':
            matriz[0] = [matriz[0][j] - matriz[i + 1][j] for j in range(len(matriz[i]))]

    matt = Simplex(matriz, vars)
    tem = 1
    tVBi = []
    
    for i in range(len(VBintT)):
        for j in range(len(VBint)):
            if VBint[j] >= VBintT[i]:
                tVBi.append(VBint[j] - tem)
            else:
                tVBi.append(VBint[j])
        tem += 1
    
    for i in tVBi:
        VBint.pop(0)
        VBint.append(i)

    matt[0] = z
    for i in range(len(matt)):
        for j in iArt[::-1]:
            del matt[i][j]

    for j in iArt[::-1]:
        del VBv[j]

    print("Fase 2\nMatriz Inicial")
    filas = ["", "Z"] + VBh
    col = VBv + ["LD"]
    Ematriz = np.hstack((np.array([filas]).reshape(-1, 1), np.vstack((col, np.round(matt, 2)))))
    for fila in Ematriz:
        print(*fila, sep="\t", end="\n")
    print("\n")

    #Se borran las variables básicas luego de que
    for i in range(1, len(VBintT) + 2):
        num = tVBi[i - 1]
        numZ = matt[0][num]
        menosMatriz = [j * numZ for j in matt[i]]
        matt[0] = [round(matt[0][j] - menosMatriz[j]) if (
                0.000000001 > matt[0][j] - menosMatriz[j] > -0.000000000000000001)
                   else round(matt[0][j] - menosMatriz[j], 8)
        if str(matt[0][j] - menosMatriz[j])[::-1].find('.') > 8
        else matt[0][j] - menosMatriz[j] for j in range(len(matt[0]))]

    matt = Simplex(matt, vars)
    LDx = [0] * vars
    for i in range(len(VBint)):
        for j in range(vars):
            if VBint[i] == j:
                LDx[j] = matt[i+1][len(matt[0])-1]

    print(LDx)
    iSombra = sombra = 0
    for i in range(vars, len(matt[0])-1):
        if matt[0][i] > sombra:
            sombra = matt[0][i]
            iSombra = i
    print(sombra, VBv[iSombra])
    return matt


def Simplex(matriz, vars):
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
        pivot = 0
        menorLD = 999999
        if l == 0:
            for i in range(vars):
                if matriz[0][i] < pivot:
                    pivot = matriz[0][i]
                    iVertPiv = i
        else:
            for i in range(len(matriz[0]) - 1):
                if matriz[0][i] < 0 and matriz[0][i] < pivot:
                    pivot = matriz[0][i]
                    iVertPiv = i

        if pivot == 0:
            break

        for i in range(1, len(matriz)):
            if matriz[i][iVertPiv] <= 0:
                continue
            menorLDtest = matriz[i][len(matriz[i]) - 1] / matriz[i][iVertPiv]
            if menorLDtest < menorLD:
                menorLD = menorLDtest
                iHorzPiv = i

        matriz[iHorzPiv] = [item / matriz[iHorzPiv][iVertPiv] for item in matriz[iHorzPiv]]

        for i in range(len(matriz)):
            if i == iHorzPiv:
                continue

            num = matriz[i][iVertPiv]

            menosMatriz = [j * num for j in matriz[iHorzPiv]]
            # REDONDEO matriz
            matriz[i] = [round(matriz[i][j] - menosMatriz[j]) if (
                    0.000000001 > matriz[i][j] - menosMatriz[j] > -0.000000000000000001)
                         else round(matriz[i][j] - menosMatriz[j], 8)
            if str(matriz[i][j] - menosMatriz[j])[::-1].find('.') > 8
            else matriz[i][j] - menosMatriz[j] for j in range(len(matriz[i]))]
        if not iHorzPiv:
            print(0)
            break

        VBh[iHorzPiv - 1] = VBv[iVertPiv]
        VBint[iHorzPiv - 1] = iVertPiv
        print(VBh)
        print(VBint)
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

miVersion(input_str2)
