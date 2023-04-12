import numpy as np
import re

def miVersion(x):
    
    #generar forma tabular
    coeffs = []
    vars = []
    pattern = r'([-+]?\d*)[ ]*([a-zA-Z]\d+)'
    for match in re.findall(pattern, x):
        coeff_str, var = match
        coeff = int(coeff_str) if coeff_str else 1
        coeffs.append(coeff)
        vars.append(var)
    return coeffs, vars

print(miVersion("2x1 -5x2 + 3x3 + x4"))


def parse_input(input_str):
    # Parse problem objective
    lines = input_str.strip().split('\n')
    max_min_str, *obj_str = lines[0].split()
    is_max = (max_min_str.strip().lower() == 'maximize')
    print(obj_str)
    variables = re.findall(r'([-+]?\d*\.)?\d+\s*[xX]\d+', join(obj_str))
    print(variables)
    coeffs = [int(re.findall(r'[+-]?\d+', var)[0]) for var in obj_str.split()]
    
    # Parse problem constraints
    A, b = [], []
    for line in lines[2:]:
        constraint_parts = re.findall(r'[+-]?\s*\d*\s*x\d+|[+-]?\s*\d+', line)
        coeffs = []
        for part in constraint_parts:
            var_match = re.match(r'[+-]?\s*(\d*)\s*(x\d+)', part)
            if var_match:
                coeff, var = var_match.groups()
                coeff = int(coeff + '1') if coeff in ['', '+', '-'] else int(coeff)
                coeffs.append(coeff)
                variables.append(var)
            else:
                coeffs.append(int(part))
        if len(coeffs) != len(variables):
            raise ValueError('Invalid constraint expression: ' + line)
        A.append(coeffs[:-1])
        b.append(coeffs[-1])
    
    # Convert problem to standard form
    if is_max:
        A = [[-coeff for coeff in row] for row in A]
        b = [-coeff for coeff in b]
    return A, b, variables




def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False



# Función para resolver el problema de programación lineal utilizando el método simplex
def simplex_solve(A, b):
    # Agregar variables de holgura
    n_constraints, n_vars = A.shape
    A = np.hstack((A, np.eye(n_constraints)))

    # Crear la función objetivo
    c = np.zeros(n_vars + n_constraints)
    c[:n_vars] = -1

    # Crear matriz aumentada
    T = np.vstack((np.hstack((A, np.atleast_2d(b).T)), np.hstack((c, np.zeros(1)))))

    # Encontrar la columna de pivote inicial
    j = np.argmin(T[-1, :-1])

    while T[:-1, j].min() < 0:
        # Encontrar la fila de pivote
        i = np.argmin(T[:-1, -1] / T[:-1, j])

        # Realizar la operación de pivote
        T[i, :] /= T[i, j]
        for k in range(T.shape[0]):
            if k != i:
                T[k, :] -= T[k, j] * T[i, :]

        # Actualizar la columna de pivote
        j = np.argmin(T[-1, :-1])

    # Obtener la solución óptima
    x = np.zeros(n_vars)
    for i in range(n_constraints):
        if (T[i, :-1] == 0).sum() == 1 and T[i, -1] > 0:
            j = np.argmax(T[i, :-1])
            x[j] = T[i, -1]

    return x

input_str = """maximize 2x1 - x2 + 4x3
subject to
x1 + x2 + x3 <= 5
2x1 - x2 + 3x3 >= 0
x1 - x3 <= 2
x1, x2, x3 >= 0"""

# Parsear la entrada
A, b = parse_input(input_str)

# Resolver el problema de optimización
x = simplex_solve(A, b)

# Imprimir la solución
print(x)