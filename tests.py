import numpy as np

from operadores import calcular_distancia_recorrido, recorrido_valido


matriz_ejemplo = np.array([
    [0, 3, 5],
    [3, 0, 4],
    [5, 4, 0],
])
recorrido = [0, 1, 2]

assert recorrido_valido(recorrido, 3)
assert not recorrido_valido([0, 0, 2], 3)
assert calcular_distancia_recorrido(recorrido, matriz_ejemplo) == 12

print('Pruebas correctas: recorrido válido y distancia total igual a 12.')
