import argparse
import numpy as np
from math import sin, cos, fabs, sqrt
import sympy as sp


def evaluar_funcion(x, fx): #funcion que evalua el punto ingresado en la funcion
    return eval(fx)

def Derivada (x, delta, fx):
    up = evaluar_funcion(x+delta, fx) - evaluar_funcion(x, fx)
    dx = up/delta
    return dx

def Determinar_delta(x,fx,dx,E): #deltaX = derivada manual - derivada metodo
    Temp_delta = sqrt(E)*dx
    Temp_dx = (evaluar_funcion(x+Temp_delta,fx) - evaluar_funcion(x,fx))/Temp_delta
    error = fabs(dx -Temp_dx)
    print(error)

    while error > E:
        Temp_delta = Temp_delta/(1 + error)
        Temp_dx = (evaluar_funcion(x+Temp_delta,fx) - evaluar_funcion(x,fx))/Temp_delta
        error = fabs(dx -Temp_dx)

    print(f"delta de ={Temp_delta}")

    return Temp_delta
        
x = 2 
fx = "x**3"
delta = 0.1
dx = Derivada(x,delta,fx) #3*x**2 = 12
print(dx) #12.61
print(f"delta x ={Determinar_delta(x, fx, 12, 0.0001)}")