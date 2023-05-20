def Determinar_error(x,fx,dx,E): #deltaX = derivada manual - derivada metodo
    print(f"dx = {dx}")
    fdx = str(sp.diff(fx, sp.symbols('x')))
    Temp_delta = 1
    Temp_dx = evaluar_funcion(x+Temp_delta, fdx) 
    error = fabs(dx -Temp_dx)
    delta_revisor = 1
    print(sqrt(E)*dx)
    while error > E:
        Δx = evaluar_funcion(x+Temp_delta, fdx)
        error = fabs(dx -Temp_dx)
        print(f"delta de ={Temp_delta}")
        print(f"dx de ={Temp_dx}")
        print(f"error de ={error}")

        delta_revisor= delta_revisor/2
        if (Temp_dx > dx):
            Temp_delta -= delta_revisor
            (print("baja\n"))
        else:
            Temp_delta =+ delta_revisor
            (print("crece\n"))

    return Temp_delta