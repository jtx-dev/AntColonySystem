from pathlib import Path

import numpy as np

from acs import ParametrosACS, ejecutar_acs
from operadores import (
    actualizar_feromona_global,
    actualizar_feromona_local,
    calcular_distancia_recorrido,
    calcular_distancias,
    calcular_heuristica,
    construir_recorrido,
    inicializar_feromonas,
    leer_datos,
    recorrido_valido,
)


def probar_lectura_berlin52():
    entrada = Path(__file__).parent / 'datos' / 'instancia.txt'
    coordenadas, n = leer_datos(entrada)
    distancias = calcular_distancias(coordenadas, n)
    assert n == 52
    assert distancias.shape == (52, 52)
    assert distancias[0, 1] == 666
    assert np.array_equal(distancias, distancias.T)


def probar_recorrido_y_distancia():
    matriz = np.array([
        [0, 3, 5],
        [3, 0, 4],
        [5, 4, 0],
    ])
    assert recorrido_valido([0, 1, 2], 3)
    assert not recorrido_valido([0, 0, 2], 3)
    assert calcular_distancia_recorrido([0, 1, 2], matriz) == 12


def probar_feromonas_y_construccion():
    matriz = np.array([
        [0, 3, 5],
        [3, 0, 4],
        [5, 4, 0],
    ])
    tau0 = 0.1
    feromonas = inicializar_feromonas(3, tau0)
    heuristica = calcular_heuristica(matriz)
    assert np.all(np.diag(feromonas) == 0)

    feromonas[0, 1] = feromonas[1, 0] = 0.2
    actualizar_feromona_local(feromonas, 0, 1, 0.1, tau0)
    assert np.isclose(feromonas[0, 1], 0.19)
    assert feromonas[0, 1] == feromonas[1, 0]

    recorrido = construir_recorrido(
        feromonas, heuristica, tau0, 0.1, 2.0, 0.9, np.random.default_rng(7)
    )
    assert recorrido_valido(recorrido, 3)

    antes = feromonas[recorrido[0], recorrido[1]]
    actualizar_feromona_global(feromonas, recorrido, 12, 0.1)
    despues = feromonas[recorrido[0], recorrido[1]]
    assert np.isclose(despues, 0.9 * antes + 0.1 / 12)


def probar_reproducibilidad():
    matriz = np.array([
        [0, 2, 9, 10],
        [2, 0, 6, 4],
        [9, 6, 0, 3],
        [10, 4, 3, 0],
    ])
    parametros = ParametrosACS(4, 8, 0.1, 2.0, 0.8, 123)
    recorrido_1, costo_1, historial = ejecutar_acs(matriz, parametros)
    recorrido_2, costo_2, _ = ejecutar_acs(matriz, parametros)
    assert recorrido_1 == recorrido_2
    assert costo_1 == costo_2
    costos = [registro['mejor_costo'] for registro in historial]
    assert costos == sorted(costos, reverse=True)

probar_lectura_berlin52()
probar_recorrido_y_distancia()
probar_feromonas_y_construccion()
probar_reproducibilidad()
print('Pruebas correctas.')
