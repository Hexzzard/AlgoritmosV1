import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Leer y graficar una función')
parser.add_argument('-f', '--funcion', type=str, help='Función a graficar')
parser.add_argument('-xa', type=float, help='Valor mínimo de x')
parser.add_argument('-xb', type=float, help='Valor máximo de x')
parser.add_argument('-l', '--lamda', type=float, help='Valor máximo de x')
args = parser.parse_args()

lamda = args.lamda
xa = args.xa
xb = args.xb
f = args.funcion

def evaluar_funcion(x):
    return eval(args.funcion)

def Concavidad():

    for i in np.arange(0,1,args.lamda):
        izquierda = evaluar_funcion(i*xa+ (1-i)*xb)
        derecha = i*evaluar_funcion(xa) +(1-i)*evaluar_funcion(xb)
        if (izquierda >= derecha):
            concavidad = "la funcion es convexa"
            continue
        elif (izquierda <= derecha):
            concavidad = "la funcion es concava"
        else:
            concavidad = "no se puede determinar"

    return print(concavidad)

def Graficar():
    x_vals = np.linspace(args.xa, args.xb+10, 100)
    y_vals = [evaluar_funcion(x) for x in x_vals]
    fig, ax = plt.subplots()
    x2_vals = []
    y2_vals = []
    y3_vals = []
    for i in np.linspace(0, 1, int(1/lamda+1)):
        y2_vals.append(i*evaluar_funcion(xa) +(1-i)*evaluar_funcion(xb))
        x2_vals.append(i*(xb-xa)+xa)
        y3_vals.append(evaluar_funcion(i*xa+ (1-i)*xb))
    ax.plot(x2_vals, y2_vals,label="red")
    ax.plot(x_vals, y_vals, label="blue")
    ax.plot(x2_vals, y3_vals, label="blue")
    print(x2_vals)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Gráfica de la función')
    plt.grid(True)
    plt.show()
    
Concavidad()
Graficar()

def Gradiente_Descendente_Barzilai_Borwein(funcion, punto, t_inicial, epsilon=1e-5, max_iterations=10):
    punto = np.array(punto)

    iteracion = 1 #hacemos la primera iteracion fuera del ciclo y en base a el valor de t_inicial
    gradiente_anterior = np.array(Gradiente_analitico(funcion, punto)) 
    delta_x = -gradiente_anterior
    punto_anterior = punto
    punto = punto + np.dot(t_inicial,delta_x)

    while True:
        print(f"Iteracion {iteracion}: punto {punto}")
        gradiente = np.array(Gradiente_analitico(funcion, punto))
        error = np.linalg.norm(gradiente) #determinamos el error que esta en funcion de la norma del gradiente
        if error < epsilon or iteracion >= max_iterations:
            print(f"Se realizaron {iteracion} iteraciones, Error de {error}")
            break
        delta_x = -gradiente
        t = np.abs(np.dot((punto- punto_anterior), (gradiente - gradiente_anterior))) / np.linalg.norm(gradiente - gradiente_anterior)**2
        print(delta_x)
        print(np.dot(t,delta_x))
        #actualizamos las variables temporales
        gradiente_anterior = gradiente
        punto_anterior = punto
        punto = punto + np.dot(t,delta_x)
        iteracion += 1 
        
    return punto
