from sympy import symbols, diff, sympify
from math import sin, cos, tan, fabs, sqrt, pi
import numpy as np

#variables globales
x, y, z = symbols('x y z')

def evaluar_funcion(funcion, variables):
    expr = sympify(funcion)  # Convierte la cadena de la funcion en una expresion sympy
    expr_evaluada = expr.subs(variables)

    return expr_evaluada

def Derivada_analitica(funcion, variable):
    derivada = diff(funcion, variable)
    return derivada

def Gradiente_analitico(funcion, punto=None, retornar_analitico=False):
    #esta funcion calcula el gradiente y tiene 3 modos de operacion:
    #el primer modo es solo ingresando la funcion y retorna el gradiente analitico de una funcion
    #el segundo modo se le ingresa un punto y retorna el gradiente evaluado en dicho punto
    #el tercer modo retorna el gradiente evaluado en dicho punto y el gradiente analitico de la funcion

    gradiente = [] #almacena el gradiente de la funcion
    if punto is not None and retornar_analitico:
        gradiente_analitico = [] #almacenara el gradiente analitico de la funcion
    
    funcion = sympify(funcion) #convertir la expresion a un arreglo de sympy
    variables = sorted([str(variable) for variable in funcion.free_symbols]) #calcula las variables que estan en la funcion, de manera ordenada
    
    if punto is not None: #creamos un diccionario de valores
        diccionario_valores = {} 
        for i in range(len(punto)): 
            diccionario_valores[variables[i]]= punto[i]

    for variable in variables: #iteramos sobre cada elemento en el arreglo de vectores 
        derivada = Derivada_analitica(funcion, variable) #calcula la derivada analitica

        if punto is not None: #si se ingresa un punto evaluamos la derivada en dicho punto
            if punto is not None and retornar_analitico: #si esta activada la opcion de retornar_analitico, almacenamos lo obtenido de forma analitica
                gradiente_analitico.append(derivada)
            
            derivada = float(evaluar_funcion(derivada, diccionario_valores)) #evaluamos la derivada con el diccionario de valores

        gradiente.append(derivada)

    if punto is not None and retornar_analitico: #si esta activada la opcion de gradiente analitico, retornamos ambos arreglos
        return gradiente, gradiente_analitico 
 
    return gradiente

def Matriz_Hessiana_analitica(gradiente, punto=None):
    #esta funcion cuenta con dos modos de operacion
    #el primer modo es solo ingresando la funcion y devuelve la matriz hessiana de forma analitica
    #en el segundo modo se le ingresa un punto y evalua la matriz en dicho punto

    tamaño = len(gradiente) #creamos una matriz de tamaño len(gradiente)xlen(gradiente) de tipo float
    if punto is None: #si se ingresa un punto el tipo de la matriz debe ser float y en caso contrario object
        hessiano = np.ndarray(shape=(tamaño, tamaño), dtype=object)
    else:
        hessiano = np.ndarray(shape=(tamaño, tamaño), dtype=float)
    
    variables = ['x','y','z'] #marcar relacion de 0 a x, 1 a y, 2 a z
    fila = 0
    inferior = 0 #eliminar la diagonal inferior
    for derivada in gradiente:
        for columna in range(inferior,tamaño):
            derivada_parcial = Derivada_analitica(derivada, variables[columna])
                
            if punto is not None: #si se ingresa un punto evaluamos la derivada en dicho punto
                diccionario_valores = {} #utilizamos un diccionario
                for i in range(len(punto)): 
                    diccionario_valores[variables[i]]= punto[i]
                derivada_parcial = evaluar_funcion(derivada_parcial, diccionario_valores)

            if(fila != columna): #si el elemento no pertenece a la diagonal lo guardamos en su homologo
                hessiano[columna][fila]= derivada_parcial
        
            hessiano[fila][columna]= derivada_parcial

        inferior +=1
        fila +=1

    return hessiano

def Gradiente_Descendente_t_fijo(funcion, punto, t, epsilon=1e-2, iteraciones_max=1000):
    punto = np.array(punto) #convertimos el punto a un arreglo para operaciones de vectores con numpy
    iteracion = 0

    while True:
        gradiente = np.array(Gradiente_analitico(funcion, punto)) #obtenemos el gradiente evaluado en el punto

        error = np.linalg.norm(gradiente) #el error esta determinado por la norma de la gradiente o delta_x
        if error < epsilon or iteracion >= iteraciones_max: #el ciclo termina si el error es menor que un epsilon o si se superan el numero maximo de iteraciones
            valor_z = evaluar_funcion(funcion,{x:punto[0], y:punto[1]}) #obtenemos el valor de z, para retornar el punto
            solucion = [punto[0],punto[1],valor_z]
            print(f"Se realizaron {iteracion} iteraciones, Error de {error}")
            print(f"El punto critico mas cercano es {solucion}")
            break

        delta_x = -gradiente #aplicamos formula
        punto = punto + t*delta_x
        iteracion += 1
        print(f"Iteracion {iteracion}: punto {punto}")
        
    return solucion

def Gradiente_Descendente_Barzilai_Borwein(funcion, punto, t_inicial, epsilon=1e-2, iteraciones_max=100):
    punto = np.array(punto) #convertimos el punto a un arreglo para operaciones de vectores con numpy
    
    iteracion = 1 #hacemos la primera iteracion fuera del ciclo y en base a el valor de t_inicial
    gradiente_anterior = np.array(Gradiente_analitico(funcion, punto)) #obtenemos el gradiente evaluado en el punto
    delta_x = -gradiente_anterior #aplicamos formula
    punto_anterior = punto
    punto = punto + np.dot(t_inicial,delta_x)
    print(f"Iteracion {iteracion}: punto {punto}")
    while True:
        
        gradiente = np.array(Gradiente_analitico(funcion, punto))
    
        error = np.linalg.norm(gradiente) #determinamos el error que esta en funcion de la norma del gradiente
        if error < epsilon or iteracion >= iteraciones_max: #el ciclo termina si el error es menor al epsilon o si se supera el numero maximo de iteraciones
            valor_z = evaluar_funcion(funcion,{x:punto[0], y:punto[1]}) #obtenemos el valor de z, para retornar el punto
            solucion = [punto[0],punto[1],valor_z]
            
            print(f"Se realizaron {iteracion} iteraciones, Error de {error}")
            print(f"El punto critico mas cercano es {solucion}")
            break

        delta_x = -gradiente#aplicamos formula
        t = np.abs(np.dot((punto- punto_anterior), (gradiente - gradiente_anterior))) / np.linalg.norm(gradiente - gradiente_anterior)**2

        #actualizamos las variables temporales
        gradiente_anterior = gradiente
        punto_anterior = punto
        punto = punto + np.dot(t,delta_x)
        iteracion += 1 
        print(f"Iteracion {iteracion}: punto {punto}")
        
        
    return solucion

def Gradiente_Descendente_Newton(funcion, punto, t, epsilon=1e-2, max_iterations=100):
    punto = np.array(punto) #convertimos el punto a un arreglo para operaciones de vectores con numpy
    iteracion = 0
    while True:
        #obtenemos el gradiente evaluado en el punto y el gradiente analitico de la funcion
        gradiente_numerico, gradiente_analitico = np.array(Gradiente_analitico(funcion,punto,retornar_analitico=True)) 
        hessiana = Matriz_Hessiana_analitica(gradiente_analitico, punto) #calculamos la matriz hessiana

        punto_nuevo = punto - t*np.dot(np.linalg.inv(hessiana),gradiente_numerico)#aplicamos formula
        print(f"Iteracion {iteracion}: punto {punto_nuevo}")

        error= np.linalg.norm(punto_nuevo -punto) 
        if error <= epsilon or iteracion >= max_iterations: #el ciclo termina cuando el error es inferior al epsilon o si se supera el numero maximo de iteraciones
            valor_z = evaluar_funcion(funcion,{x:punto[0], y:punto[1]}) #obtenemos el valor de z, para retornar el punto
            solucion = [punto[0],punto[1],valor_z]
            print(f"Se realizaron {iteracion} iteraciones, Error de {error}")
            print(f"El punto critico mas cercano es {solucion}")
            break
        
        gradiente_nuevo = np.array(Gradiente_analitico(funcion,punto_nuevo)) #calculamos el gradiente en el nuevo punto
        norma_gradiente_nuevo = np.linalg.norm(gradiente_nuevo)
        norma_gradiente = np.linalg.norm(gradiente_numerico)

        if norma_gradiente_nuevo < norma_gradiente: #aplicamos la correccion 
            g0 = norma_gradiente
            g0_prima = -(norma_gradiente/np.linalg.norm(gradiente_nuevo-gradiente_numerico))
            g1 = norma_gradiente_nuevo
            t_prima = max(-g0_prima/(2*(g1-g0-g0_prima)),1)
            punto_nuevo = (1-t_prima)*punto +t_prima*punto_nuevo
            print(f"arreglo: punto {punto_nuevo}")

        punto = punto_nuevo #actualizamos el punto
        iteracion +=1
        
    return solucion

comun = "x**2 +y**2"
himenblau = "(x**2+y-11)**2+(x+y**2-7)**2"
cubica = "(x-12)**3+(y+8)**3" 

punto = [100000,100000]
t = [0.5,0.5]
t1 = 1

#print(evaluar_funcion(mcCornick,{x:-0.54320519,y:-1.54320173}))
#Gradiente_Descendente_t_fijo(comun, punto, t)
print(Gradiente_Descendente_Barzilai_Borwein(himenblau, punto, t))
print(Gradiente_Descendente_Newton(cubica,punto,t1))
 