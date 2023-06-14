import numpy as np

thetha = 0.00006
delta = 200
soluciones = []

def fx(x1,x2,thetha):
    Z = (1.2*x1+ 1.16*x2 -thetha*(2*x1**2 + x2**2 +(x1+x2)**2))
    return Z

for i in range(int(5000/delta)+1):
    x1 = delta*i
    for j in range(int(5000/delta)+1):
        x2 = delta*j
        if(x1+x2 <= 5000):
            Z = fx(x1,x2,thetha)
            soluciones.append([x1,x2,Z])

X = np.argmax(np.array(soluciones), axis=0)[2]

respuesta = f"El maximo se obtiene con el vector ({soluciones[X][0]} , {soluciones[X][1]}), obteniendose un valor de {soluciones[X][2]}"
print(respuesta)



#print(soluciones)