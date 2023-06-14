from sympy import symbols, diff, sympify, E, N
from math import sin, cos, tan, fabs, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
import argparse

#creamos el argparser
parser = argparse.ArgumentParser(description='Este script cuenta con 5 funciones: determinar el gradiente de una funcion, realizar la grafica de una funcion con respecto a la obtenida a evaluar en f(x+ delta) y utilizando el toerema de Taylor')

#llamada a funciones
parser.add_argument('--taylor', action='store_true', help='graficar interpolacion de taylor de una funcion univariante, ingresar la funcion (-fx), el intervalo a graficar (-i), el valor de delta_x (-d) y el valor de t (-t)')

#definicion de parametros
parser.add_argument('-fx', type=str, help='Funcion a determinar')
parser.add_argument('-d', type=float, help='delta_x')
parser.add_argument('-i', nargs='+', type=float, help='intervalo')
parser.add_argument('-t', type=float, help='t')
args = parser.parse_args()

def evaluar_funcion(funcion, variables, valor):
    x, y, z, t, delta_x = symbols('x y z t delta_x')
    expr = sympify(funcion)  # Convierte la cadena de la funcion en una expresion sympy
    expr_evaluada = expr.subs(variables, valor)

    return expr_evaluada

def Derivada_analitica(funcion, variable):
    x = symbols(variable)
    derivada = diff(funcion, x)
    return derivada

def TeoremaTaylor(funcion, intervalo, delta_x, t):
    x = symbols('x') #Esta funcion trabaja con funciones univariables, por lo que nos basta con solo definir X
    funcion = sympify(funcion) #convertimos el string en una expresion de sympy
    primera_derivada = Derivada_analitica(funcion, 'x') #determinar primer derivada, esta se calcula de forma analitica, es decir como una funcion
    segunda_derivada = Derivada_analitica(primera_derivada, 'x') #determinar segunda derivada

    #Generamos una expresion de sympy equivalente al teorema de taylor
    interpolacion_Taylor= funcion + primera_derivada*delta_x + (delta_x*evaluar_funcion(segunda_derivada, 'x', x + t*delta_x)*delta_x)/2
    print(f"La interpolacion de la funcion {funcion} con respecto a el teorema de taylor, con un valor de Δx = {delta_x} y t = {t} es: {interpolacion_Taylor}")

    puntos_Taylor = [] #determinamos los puntos a graficar
    puntos_funcion_original = []
    puntos_a_graficar = 100
    puntos_intervalo = np.linspace(intervalo[0], intervalo[1], puntos_a_graficar)
    
    #iteramos sobre cada uno de los puntos a graficar
    for punto in puntos_intervalo:
        
        punto_taylor = evaluar_funcion(interpolacion_Taylor, 'x', punto)
        #en el teorema la funcion original es evaluada sobre f(x + Δx)
        punto_funcion_original = evaluar_funcion(funcion, 'x', punto+ delta_x)

        puntos_Taylor.append(punto_taylor) #añadimos los puntos al arreglo
        puntos_funcion_original.append(punto_funcion_original)

    #graficamos
    print(puntos_funcion_original[0])
    fig, ax = plt.subplots()
    try:    #se genera un error en el caso de que la funcion no sea univariable
        ax.plot(puntos_intervalo, puntos_Taylor, label=f"Interpolacion de Taylor", color="blue")
        ax.plot(puntos_intervalo, puntos_funcion_original, label="Funcion original", color="red")

    except:
        print("Error: hay mas de una variable")

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Comparacion del teorema de Taylor con la funcion original') 
    plt.grid(True)
    plt.legend()
    plt.show()

    return interpolacion_Taylor

funcion1 = "x**2 - cos(x)"
funcion2 = 'x'
funcion3 = "x**4 - cos(x)*sin(x) + x**2"
funcion4 = "2*E**(x*2)"
funcion5 = "2*E**(x*sin(x)) - cos(x)*sin(x)*x**2"

if (args.taylor): #funcion que determina el valor de delta X
    fx = args.fx
    intervalo = args.i
    delta_x = args.d
    t = args.t
    TeoremaTaylor(fx,intervalo,delta_x,t)
