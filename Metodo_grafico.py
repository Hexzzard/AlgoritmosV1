import re
import matplotlib.pyplot as plt

# Pedir al usuario que introduzca la ecuación
rest = [
    "3x+2y<=18",
    "1x+0y<=4",
    "0x+2y<=12",
    "1x+0y>=0",
    "0x+1y>=0"]
f_objetivo = "30000x+50000y=Z" #se pueden incluir decimales, por ejemplo:"2.3" 
tipo = "max" # puede ser de tipo "max" o "min"


def inter(recta1, recta2):
    # Verificar si las rectas son paralelas
  
    if recta1[0] == recta2[0]:
        #print("Las rectas son paralelas y no tienen un punto de intersección.")
        return False
    else:
        # Verificar si alguna de las rectas es vertical
        if recta1[0] is None:
            x = recta1[1]
            y = recta2[0] * x + recta2[1]
            print("cuando es none: ", x, y)
            print("rectas: ", recta1, recta2)
            return x, y
        elif recta2[0] is None:
            x = recta1[1]
            y = recta1[0] * x + recta1[1]
            print("cuando es none: ", x, y)
            print("rectas: ", recta1, recta2)
            return x, y
        else:
            # Encontrar el punto de intersección
            x = (recta2[1] - recta1[1]) / (recta1[0] - recta2[0])
            y = recta1[0] * x + recta1[1]
        #print(f"El punto de intersección es ({x}, {y})")
        return x, y
#############################convertir ecuacion o inecuacion en una funcion############################


#obtiene mediante expresiones literales los coeficientes de una funcion o restriccion con estructura especifica
def coeficientes(input):
    coeficientes = re.findall(r'[-]?\d*\.?\d+', input)
    #terminos = re.findall(r'[a-zA-Z]*', input_str)
    return coeficientes

#convierte los coeficientes extraidos de un string a entero o float.
def str_int(str):
    arr = (coeficientes(str))
    li = []
    for i in range(len(arr)):
        if(arr[i].isdigit()):
            li.append(int(arr[i]))
        else:
            li.append(float(arr[i]))
    if li[1] == 0:
        return [li, True]

    return [li, False]



def funcion(x, coe):
    coe1 = coe[0]
    imagen = []
    pre = []
    if coe[1]:
        for i in range(len(x)):
            imagen.append(x[i])
            pre.append((coe1[2]-(coe1[1]*x[i]))/coe1[0])
        #print(x, imagen)
        return pre, imagen
    for i in range(len(x)):
        imagen.append((coe1[2]-(coe1[0]*x[i]))/coe1[1])
    #print(x, imagen)
    return x, imagen

#determina el la desigualdad
def inecuacion(sig, a, b):
    sign = sig[0]
    if sign == "<=":
        if a <= b:
            return True
        else:
            return False
    elif sign == ">=":
        if a >= b:
            return True
        else:
            return False
    elif sign == ">":
        if a > b:
            return True
        else:
            return False
    elif sign == "<":
        if a < b:
            return True
        else:
            return False
    elif sign == "=":
        if a == b:
            return True
        else:
            return False
    


def region_factible(inter):
    rf = []
    cont = 0
    for j in range(len(inter)):
        for i in range(len(rest)):
            c = str_int(rest[i])
            signo = re.findall(r'[<>]=?|!=', rest[i])

            if inecuacion(signo, c[0][0]*inter[j][0]+c[0][1]*inter[j][1], c[0][2]):
                cont += 1
        if cont == len(rest):
            rf.append(inter[j])
        cont = 0
    return rf


# retorna todas las interseccion entre rectas.
def obtener_inter():
    inte = []
    c = []
    for i in range(len(rest)):
        c.append(str_int(rest[i])[0])
  
    for i in range(len(rest)):
        for j in range(len(rest)-i):
            if encontrar(c[i], c[j+i]) != None:
                # inte.append(interse)
                inte.append(encontrar(c[i], c[j+i]))
    print("Todas las intersecciones encontradas: ", inte)
    return inte


# Genera valores para la variable independiente x
x = [0, 100]


def encontrar(co1, co2):
    # Convertir la primera ecuación a la forma y = mx + b
    a, b, c = map(int, co1)
    if b == 0:
        m1 = None
        b1 = c
    else:
        m1 = -a/b
        b1 = c/b
    # Convertir la segunda ecuación a la forma y = mx + b
    a, b, c = map(int, co2)
    if b == 0:
        m2 = None
        b2 = c
    else:
        m2 = -a/b
        b2 = c/b
    # Calcular la intersección de las dos rectas
    if m2 is None and m1 is None:
        return None
    if m2 is None:
        x = b2
        y = m1 * x + b1
    elif m1 is None:
        x = b1
        y = m2 * x + b2
    elif m1 == m2: #Las rectas son paralelas y no tienen un punto de intersección.
        return None
    else:
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
    return x, y


def f_obj(coe, x, y):
    co = coe[0]
    result = (co[0]*x)+(co[1]*y)
    print("----------valor de f objetivo y interseccion evaluada----------")
    print(result)
    print(x, y)
    return result


#De todas las intersecciones dentro de la region factible obtiene la menor o la mayor dependiendo si es minimo o maximo
def obtener_optimo():
    temp = 0
    mayor = 0
    interseccion_optima = 0, 0
    i_f = region_factible(obtener_inter())
    print("intersecciones dentro de la region factible: ",i_f)

    for i in range(len(i_f)):
        xf, yf = i_f[i]
        if i==0:
            temp = (f_obj(str_int(f_objetivo), xf, yf))
        op = (f_obj(str_int(f_objetivo), xf, yf))
        if tipo=="min":
            if temp >= op:
                mayor = op
                temp = op
                interseccion_optima = xf, yf
            else:
                mayor = temp
        elif tipo=="max":
            if temp <= op:
                mayor = op
                temp = op
                interseccion_optima = xf, yf
            else:
                mayor = temp

    print("valor optimo: ", mayor)
    print("interseccion optima: ", interseccion_optima)
    return mayor, interseccion_optima


# Graficar los ejes x e y
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

# Agregar etiquetas a los ejes
plt.xlabel('Eje x')
plt.ylabel('Eje y')
#grafica todas las rectas generadas a partir de las restricciones y el punto donde esta el optimo
def grafica():
    optimo, interseccion = obtener_optimo()
    #obtenemos los puntos a graficar(rectas)
    for i in range(len(rest)):
        xg, yg = funcion(x, str_int(rest[i]))
        plt.plot(xg, yg)
    #graficamos el punto optimo encontrado
    plt.scatter(interseccion[0], interseccion[1], color='red')
    # Mostrar la gráfica
    plt.show()

grafica()