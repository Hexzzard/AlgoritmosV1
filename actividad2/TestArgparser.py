import argparse
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, fabs

#creamos el argparser
parser = argparse.ArgumentParser(description='Determinar si una funcion es concava o convexa en un intervalo [xa,xb]')
parser.add_argument('-fx', type=str, help='Funcion a determinar')
parser.add_argument('-xa', type=float, help='Valor minimo de x')
parser.add_argument('-xb', type=float, help='Valor maximo de x')
parser.add_argument('-l', type=float, help='Valor de lambda, entre 0 y 1')
args = parser.parse_args()

def evaluar_funcion(x, fx): #funcion que evalua el punto ingresado en la funcion
    return eval(fx)

def Concavidad(xa, xb, L, fx):
    convexo = concavo = False #indicaran si la funcion es concava o convexa
    estricto = solucion = True #indicaran si la solucion existe y si es estricta

    puntos_interpolacion = [] #almacenar el valor obtenido para graficar
    puntos_recta = []
    intervalo = []

    #Se evalua en el intervalo (0,1) sin incluir los extremos
    for i in np.arange(L, 1, L):
        interpolacion = evaluar_funcion(i*xa+ (1-i)*xb, fx) #aplicar formula
        recta = i*evaluar_funcion(xa, fx) +(1-i)*evaluar_funcion(xb, fx)

        intervalo.append(xb - i*(xb-xa)) #el intervalo estara invertido, ya que la formula grafica de Xb a Xa
        puntos_interpolacion.append(interpolacion)
        puntos_recta.append(recta)

        if (interpolacion > recta): #si en el punto la interpolacion es mayor que el de la recta, se dice que es concavo
            if(not convexo):
                concavo = True
            else: 
                solucion = False #si se encuentra que la grafica es concava y convexa a la vez, diremos que no se puede determinar
            
        if (interpolacion < recta): #si en el punto la interpolacion es menor que el de la recta, se dice que es convexo
            if(not concavo):
                convexo = True
            else:
                solucion = False

        if (interpolacion == recta): #si en el punto la interpolacion es igual que el de la recta, ya no es estricamente concavo o convexo
            estricto = False
            
    #devolvemos segun corresponda
    if (not solucion):
        out ="no se puede determinar"
    else:
        if estricto:
            if convexo:
                out = "es estrictamente convexa"
            else:
                out = "es estrictamente concava"
        else:
            if convexo:
                out = "es convexa"
            else:
                out = "es concava"
    print(out)

    #Para graficar deberemos incluir los extremos
    puntos_interpolacion.insert(0, evaluar_funcion(xb, fx)) #extremo izquierdo
    puntos_recta.insert(0, evaluar_funcion(xb, fx))
    intervalo.insert(0,xb)

    puntos_interpolacion.append(evaluar_funcion(xa, fx)) #extremo derecho
    puntos_recta.append(evaluar_funcion(xa, fx))
    intervalo.append(xa)

    #determinamos los puntos a graficar con respecto a la funcion original
    rango = fabs(xb - xa)
    funcion_ejeX = np.linspace(xa - float(rango/2), xb + float(rango/2), 100)
    funcion_ejeY = [evaluar_funcion(x, fx) for x in funcion_ejeX]
    fig, ax = plt.subplots()
    
    ax.plot(funcion_ejeX, funcion_ejeY, label=f"fx={fx}", color="black")
    ax.plot(intervalo, puntos_interpolacion, label="Interpolacion: f(λxa + (1 + λ)xb)", color="blue")
    ax.plot(intervalo, puntos_recta, label="Recta: λf(xa) + (1 + λ)f(xb)", color="red")

    ax.set_xlim(xa - float(rango/2), xb + float(rango/2))  #definimos los limites de la visualizacion en el eje x

    #definimos el valores maximos mostrado en la grafica para el eje Y
    maximo_grafica = max(puntos_interpolacion) + (max(funcion_ejeY)- min(puntos_interpolacion))/10 
    minimo_grafica = min(puntos_interpolacion) - (max(funcion_ejeY)- min(puntos_interpolacion))/10 
    ax.set_ylim(minimo_grafica, maximo_grafica)
    # graficamos el limite izquierdo y derecho con respecto al rango
    ax.plot([xa,xa], [minimo_grafica, puntos_interpolacion[len(puntos_interpolacion)-1]], color="green", linestyle='--') 
    ax.plot([xb,xb], [minimo_grafica, puntos_interpolacion[0]], color="green", linestyle='--')
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'La funcion {out}') #el titulo del grafico sera la respuesta definida anteriormente
    plt.grid(True)
    plt.legend()
    plt.show()

    return True

#rescatamos los valores del argparser y llamamos a la funcion
L = args.l
xa = args.xa
xb = args.xb
f = args.fx
Concavidad(xa, xb, L, f)
