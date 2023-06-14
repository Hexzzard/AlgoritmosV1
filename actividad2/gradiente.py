from sympy import symbols, diff, sympify, nsimplify, E, N
from math import sin, cos, tan, fabs, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
import argparse

#creamos el argparser
parser = argparse.ArgumentParser(description='Este script cuenta con 2 funciones: determinar el gradiente de una funcion, y realizar la grafica de una funcion con respecto a la obtenida a evaluar en f(x+ delta) y utilizando el toerema de Taylor')

#llamada a funciones
parser.add_argument('--gradiente', action='store_true', help='calcular gradiente de una funcion, ingresar una funcion (-fx), un vector de componentes (-x) y un valor de delta_x (-d)')

#definicion de parametros
parser.add_argument('-fx', type=str, help='Funcion a determinar')
parser.add_argument('-x',  nargs='+', type=float, help='vector de componentes')
parser.add_argument('-d',  nargs='+', type=float, help='delta_x')
args = parser.parse_args()

def evaluar_funcion(funcion, variables, valor):
    x, y, z, t, delta_x = symbols('x y z t delta_x')
    expr = sympify(funcion)  # Convierte la cadena de la funcion en una expresion sympy
    expr_evaluada = expr.subs(variables, valor)

    return expr_evaluada

def Derivada_numerica (funcion,variable, valor, delta):
    delta_fx = evaluar_funcion(funcion,variable,valor+delta) - evaluar_funcion(funcion,variable,valor)
    derivada = delta_fx/delta
    print(f"La derivada de la funcion '{funcion}' con respecto a {variable}={valor} es: {derivada}")
    return derivada

def Gradiente(funcion, x, delta_x):
    gradiente = [] 
    var = ['x','y','z'] #Se define un arreglo con los caracteres x, y, z, esto es para traducir la posicion 0 del arreglo de vectores
                        #como un simbolo de x, y sucesivamente.
    posicion = 0
    for valor in x: #iteramos sobre cada elemento en el arreglo de vectores 

        #realizamos las derivadas parciales, reutilizamos el codigo de la actividad anterior
        derivada = Derivada_numerica(funcion, var[posicion], valor, delta_x[posicion])  
        gradiente.append(N(derivada)) #aplicamos la simplificacion N, para reducir expresiones trigonometricas a numeros
        posicion +=1

    print(f"El gradiente de la {funcion} con respecto a el vector {x} con un delta de {delta_x} es:")
    for elemento in gradiente:
        print(f"{elemento}") #para realizar una impresion como vector columna

    return gradiente

funcion1 = "1.2*x +1.16*y -0.5*(2*x**2+y**2 + (x+y)**2)"
funcion2 = "sin(x) + cos(y)*x +z**3"
funcion3 = "sin(x)*cos(y)*z**5"
funcion4 = "2*z*E**(x*y*z*2)"

x = [2, 2]
delta_x = [0.01,0.01]
x3d = [4, 5,2]
delta_x3d = [0.01,0.01,0.01]

#resultado = Gradiente(funcion4, x3d, delta_x3d)

if (args.gradiente): #funcion que determina el valor de delta X
    fx = args.fx
    x = args.x
    delta_x = args.d
    Gradiente(fx, x, delta_x)






