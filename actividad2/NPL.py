import numpy as np

thetha = float(input("introduzca el valor de thetha (aversion de riesgos)"))
delta = float(input("introduzca el valor de delta (varianza)"))
soluciones = []

def fx(x1,x2,thetha):
    Z = (1.2*x1+ 1.16*x2 -thetha*(2*x1**2 + x2**2 +(x1+x2)**2))
    return Z

for i in range(int(5/delta)+1):
    x1 = delta*i
    for j in range(int(5/delta)+1):
        x2 = delta*j
        if(x1+x2 <= 5):
            Z = fx(x1,x2,thetha)
            soluciones.append([x1,x2,Z])

X = np.argmax(np.array(soluciones)[:, 2])

respuesta = f"El maximo se obtiene con el vector ({soluciones[X][0]} , {soluciones[X][1]}), obteniendose un valor de {soluciones[X][2]}"
print(respuesta)
