from sympy import symbols, diff, sympify, E, N, Eq, solve
from math import sin, cos, tan, fabs, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
import argparse

#creamos el argparser
parser = argparse.ArgumentParser(description='Este script cuenta con 6 funciones: determinar el gradiente de una funcion, realizar la grafica de una funcion con respecto a la obtenida a evaluar en f(x+ delta) y utilizando el toerema de Taylor')

#llamada a funciones
parser.add_argument('--CriterioH', action='store_true', help='graficar interpolacion de taylor de una funcion univariante, ingresar la funcion (-fx), el intervalo a graficar (-i), el valor de delta_x (-d) y el valor de t (-t)')

#definicion de parametros
parser.add_argument('-fx', type=str, help='Funcion a determinar')
args = parser.parse_args()

#variables globales
x, y, z = symbols('x y z')

def evaluar_funcion(funcion, variables):
    expr = sympify(funcion)  # Convierte la cadena de la funcion en una expresion sympy
    expr_evaluada = expr.subs(variables)

    return expr_evaluada

def Derivada_analitica(funcion, variable):
    derivada = diff(funcion, variable)
    return derivada

def Gradiente_analitico(funcion):
    gradiente = [] 
    funcion = sympify(funcion)
    #calcular las variables que estan en la funcion, de manera ordenada
    variables = sorted([str(variable) for variable in funcion.free_symbols])
    
    for variable in variables: #iteramos sobre cada elemento en el arreglo de vectores 
        derivada = Derivada_analitica(funcion, variable) #derivada analitica
        gradiente.append(derivada)
    
    return gradiente

def Calcular_Puntos_criticos(gradiente):
    ecuacion1 = Eq(gradiente[0], 0)
    ecuacion2 = Eq(gradiente[1], 0)

    solucion = solve((ecuacion1, ecuacion2), (x, y))
    return solucion

def Matriz_Hessiana_analitica(gradiente, punto=None):
    tamaño = len(gradiente)
    hessiano = np.ndarray(shape=(tamaño, tamaño), dtype=object)

    variables = ['x','y','z'] #marcar relacion de 0 a x, 1 a y, 2 a z
    fila = 0
    inferior = 0 #eliminar la diagonal inferior
    for derivada in gradiente:
        for columna in range(inferior,tamaño):
            derivada_parcial = Derivada_analitica(derivada, variables[columna])

            if punto != None: #si se ingresa un punto evaluamos la derivada en dicho punto
                diccionario_valores = {} #utilizamos un diccionario
                for i in range(len(punto)): 
                    diccionario_valores[variables[i]]= punto[i]
                derivada_parcial = evaluar_funcion(derivada_parcial, diccionario_valores)

            if(fila != columna): #si el elemento no pertenece a la diagonal lo guardamos en su homologo
                hessiano[fila][columna]= derivada_parcial
                hessiano[columna][fila]= derivada_parcial
            else:
                hessiano[fila][columna]= derivada_parcial

        inferior +=1
        fila +=1

    return hessiano


def Criterio_H(funcion):
    gradiente = Gradiente_analitico(funcion)
    hessiano = Matriz_Hessiana_analitica(gradiente)
    puntos_criticos = Calcular_Puntos_criticos(gradiente)

    solucion = "" #almacenara la informacion de cada uno de los puntos criticos
    diccionario_valores = {} #diccionario para evaluar la matriz hessiana
    variables = ['x', 'y'] #relacion de 0 a x y 1 a y

    for punto_critico in puntos_criticos:
        for i in range(len(punto_critico)): #rellenamos el diccionario
            diccionario_valores[variables[i]]= punto_critico[i]

        hessianoxx = evaluar_funcion(hessiano[0][0], diccionario_valores) #evaluamos
        hessianoyy = evaluar_funcion(hessiano[1][1], diccionario_valores)
        hessianoxy = evaluar_funcion(hessiano[0][1], diccionario_valores)

        H = hessianoxx * hessianoyy - hessianoxy**2 #aplicar el criterio de H

        if (H < 0):
            solucion += f"el punto {punto_critico} es un punto de silla\n"
        if ((H > 0) and (hessianoxx < 0)):
            solucion += f"el punto {punto_critico} es un maximo local\n"
        if ((H > 0) and (hessianoxx > 0)):
            solucion += f"el punto {punto_critico} es un minimo local\n"
        if (H == 0):
            solucion += f"no existe informacion suficiente sobre el punto {punto_critico}\n"
    
    print("Gradiente de la funcion:") #imprimir los elementos que se usaron para el calculo
    for elemento in gradiente:
        print(elemento)
    
    print("Matriz Hessiana de la funcion:")
    for fila in hessiano:
        print(*fila, sep="    ", end="\n")

    print(f"los puntos criticos de la funcion son {puntos_criticos}\n")
    
    print(solucion)
    return solucion

funcion = "x**2 +4*y**2 -2*x**2*y+4"
funcion2 = "x**3 - y**2 + x*y +5"

if (args.CriterioH): #llamamos a criterio de H
    fx = args.fx
    Criterio_H(fx)


