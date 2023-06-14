import numpy as np
from scipy.optimize import approx_fprime



def gradient_descent(f, x0, t, threshold=1e-5, max_iterations=100):
    x = np.array(x0)
    iterations = 0
    
    while True:
        gradient = approx_fprime(x, f, epsilon=1e-6)
        delta_x = -gradient
        x_new = x + t * delta_x
        
        if np.linalg.norm(delta_x) < threshold or iterations >= max_iterations:
            break
        
        x = x_new
        iterations += 1
    
    return x_new

# Ejemplo de uso
def f(x):
    return x[0]**2 + x[1]**2

x0 = [1, 1]
t = 0.1
result = gradient_descent(f, x0, t)

print("Resultado: ", result)