import argparse
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, fabs, sqrt

#creamos el argparser
parser = argparse.ArgumentParser(description='Este script cuenta con 3 funciones: determinar concavidad en un intervalo, calcular la derivada de una funcion, determinar el valor de delta X utilizado para calcular la derivada')

#llamada a funciones
parser.add_argument('--concavidad', action='store_true', help='calcular concavidad, ingresar lambda (-l), la funcion (-fx), valor minimo (-xa), valor maximo (-xb)')
parser.add_argument('--derivar', action='store_true', help='calcular derivada, ingresar el punto en donde se evaluara (-x), el valor de delta (-d) y la funcion (-fx)')
parser.add_argument('--delta_x', action='store_true', help='calcular delta X, ingresar el punto en donde se evaluara, (-x), la funcion (-fx), el valor de la derivada (-dx) y un valor de error abosuluto epsilon (-e)')

#definicion de parametros
parser.add_argument('-l', type=float, help='Valor de lambda, entre 0 y 1')
parser.add_argument('-fx', type=str, help='Funcion a determinar')
parser.add_argument('-xa', type=float, help='Valor minimo de x')
parser.add_argument('-xb', type=float, help='Valor maximo de x')

parser.add_argument('-x', type=float, help='punto a evaluar') #nuevos
parser.add_argument('-d', type=float, help='Valor de delta')
parser.add_argument('-dx', type=float, help='Valor de la derivada de la funcion')
parser.add_argument('-e', type=float, help='Valor de epsilon (valor de error absoluto)')
args = parser.parse_args()

#funcion que evalua el punto ingresado en la funcion
def evaluar_funcion(x, fx): 
    return eval(fx)

#funcion que determina si una funcion es concava o convexa en un rango determinado
#y posteriormente grafica la interpolacion y la recta formada
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

#esta funcion calcula la derivada en funcion de la pendiente formada entre dos rectas
def Derivada (x, delta, fx): 
    dx = (evaluar_funcion(x+delta, fx) - evaluar_funcion(x, fx))/delta #aplicamos la formula de la pendiente
    print(f"la derivada de la funcion es de: {dx}")
    return dx

#esta funcion determina el valor de delta x utilizado para calcular la derivada
def Determinar_delta(x,fx,dx,E): 
    Temp_delta = 1 #inicializamos en 1, esto debido a que los valores de delta solo iran en descenso

    while True:
        Temp_dx = (evaluar_funcion(x+Temp_delta,fx) - evaluar_funcion(x,fx))/Temp_delta #aplicamos la formula
        error = fabs(dx -Temp_dx)

        if (error <= E): #si el error del calculo es menor al epsilon termina el ciclo
            break

        #O si se supera el valor minimo procesado, el cual debe ser inferior a 2.22e-16, 
        #El cual es aproximadamente el minimo valor que procesa python en los float
        if Temp_delta < 1e-10: 
            print(f"Por capacidad de computo se detuvo la operacion, hay un error de {error}")
            break

        #En caso contrario, se disminuye el valor del delta, y continua el ciclo
        Temp_delta = Temp_delta/((1 + error)) 

        
    #finalmente se imprime y retorna el valor obtenido.
    print(f"el valor de delta utilizado en la funcion es de: {Temp_delta}")

    return Temp_delta

#llamada a las funciones principales, las cuales se activan si se ha seleccionado dicha opcion dentro del argparser

if (args.concavidad): #Funcion de concavidad
    L = args.l
    xa = args.xa
    xb = args.xb
    f = args.fx
    Concavidad(xa, xb, L, f)

if (args.derivar): #Funcion de derivar
    x = args.x
    fx = args.fx
    delta = args.d
    Derivada(x,delta,fx)

if (args.delta_x): #funcion que determina el valor de delta X
    x = args.x
    fx = args.fx
    dx = args.dx
    epsilon = args.e
    Determinar_delta(x,fx,dx,epsilon)


