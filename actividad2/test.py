import numpy as np



def main(f, df, p_inicial, t_inicial , tolerancia) :
    x = p_inicial
    t = t_inicial
    prev_x = None
    prev_gradient = None

    while np.linalg.norm(df(f,x[0],x[1])) > tolerancia :
        gradient = df(f,x[0],x[1])
        delta_x = -gradient
        if prev_x is not None:
            delta_gradient = gradient - prev_gradient
            delta_xn = x - prev_x
            tn =np.abs(np.dot(delta_xn, delta_gradient)) / np.linalg.norm(delta_gradient)**2
            X = X + tn * delta_x
            t = tn
        prev_x = x.copy()
        prev_gradient = gradient.copy()
        X = x + t * delta_x
    return X

print(main())