from pathlib import Path

import numpy as np

from acs import ParametrosACS, ejecutar_acs
from operadores import (
    actualizar_feromona_local,
    actualizar_feromonas,
    actualizar_mejor_solucion,
    calcular_feromona_inicial,
    calcular_heuristica,
    calcular_makespan,
    calcular_rpd,
    construir_secuencia,
    inicializar_feromonas,
    leer_instancia,
    secuencia_valida,
)

DATOS = Path(__file__).parent / 'datos'

# 3 trabajos x 2 máquinas: tiempos[trabajo, maquina]
EJEMPLO = np.array([
    [3, 2],
    [1, 4],
    [2, 1],
])


def probar_lectura_taillard():
    tiempos, cota = leer_instancia(DATOS / 'tai20_5.txt')
    assert tiempos.shape == (20, 5)
    assert cota == 1278
    # Primera fila de ta001 (máquina 1) y primer valor de la máquina 2.
    assert list(tiempos[:10, 0]) == [54, 83, 15, 71, 77, 36, 53, 38, 27, 87]
    assert tiempos[0, 1] == 79

    for nombre, forma, cota_esperada in [
        ('tai50_10.txt', (50, 10), 2991),
        ('tai100_10.txt', (100, 10), 5770),
    ]:
        tiempos, cota = leer_instancia(DATOS / nombre)
        assert tiempos.shape == forma
        assert cota == cota_esperada
        assert tiempos.min() >= 1 and tiempos.max() <= 99


def probar_makespan_calculado_a_mano():
    # Secuencia 1-2-3:          Secuencia 2-1-3:
    #   M1: 3, 4, 6               M1: 1, 4, 6
    #   M2: 5, 9, 10              M2: 5, 7, 8
    assert calcular_makespan([0, 1, 2], EJEMPLO) == 10
    assert calcular_makespan([1, 0, 2], EJEMPLO) == 8
    # Con una sola máquina, C_max es la suma de los tiempos.
    assert calcular_makespan([2, 0, 1], EJEMPLO[:, :1]) == 6

    try:
        calcular_makespan([0, 0, 2], EJEMPLO)
    except ValueError:
        pass
    else:
        raise AssertionError('Una secuencia con trabajos repetidos debe rechazarse.')


def probar_secuencias_y_rpd():
    assert secuencia_valida([2, 0, 1], 3)
    assert not secuencia_valida([0, 1], 3)
    assert not secuencia_valida([0, 1, 1], 3)
    assert np.isclose(calcular_rpd(1300, 1250), 4.0)
    assert calcular_rpd(1278, 1278) == 0.0


def probar_heuristica():
    heuristica = calcular_heuristica(EJEMPLO)
    assert heuristica.shape == (4, 3)
    # Ocio de programar el trabajo 1 tras el 3: max(0, p[1,M1] - p[3,M2]) = 3 - 1 = 2.
    assert np.isclose(heuristica[2, 0], 1 / 3)
    assert np.isclose(heuristica[0, 1], 1.0)
    # Desde el inicio el ocio es el tiempo en M1: 3, 1 y 2.
    assert np.allclose(heuristica[3], [1 / 4, 1 / 2, 1 / 3])


def probar_feromonas():
    tau0 = calcular_feromona_inicial(EJEMPLO)
    # SPT ordena por tiempo total (5, 5, 3): secuencia 3-1-2 con C_max = 11.
    assert np.isclose(tau0, 1 / (3 * 11))

    feromonas = inicializar_feromonas(3, tau0)
    assert feromonas.shape == (4, 3)
    assert np.all(feromonas == tau0)

    feromonas[0, 1] = 0.2
    actualizar_feromona_local(feromonas, 0, 1, 0.1, tau0)
    assert np.isclose(feromonas[0, 1], 0.9 * 0.2 + 0.1 * tau0)
    assert feromonas[1, 0] == tau0  # matriz dirigida: no se toca la arista inversa

    antes = feromonas.copy()
    actualizar_feromonas(feromonas, [1, 0, 2], 8, 0.1)
    for anterior, siguiente in [(3, 1), (1, 0), (0, 2)]:
        assert np.isclose(feromonas[anterior, siguiente], 0.9 * antes[anterior, siguiente] + 0.1 / 8)
    assert feromonas[0, 1] == antes[0, 1]  # arista fuera de la secuencia


def probar_construccion():
    tiempos, _ = leer_instancia(DATOS / 'tai20_5.txt')
    tau0 = calcular_feromona_inicial(tiempos)
    feromonas = inicializar_feromonas(20, tau0)
    heuristica = calcular_heuristica(tiempos)
    generador = np.random.default_rng(7)
    for _ in range(10):
        secuencia = construir_secuencia(feromonas, heuristica, tau0, 0.1, 2.0, 0.9, generador)
        assert secuencia_valida(secuencia, 20)


def probar_mejor_solucion():
    assert actualizar_mejor_solucion(None, float('inf'), [1, 0], 9) == ([1, 0], 9)
    assert actualizar_mejor_solucion([1, 0], 9, [0, 1], 12) == ([1, 0], 9)
    assert actualizar_mejor_solucion([1, 0], 9, [0, 1], 7) == ([0, 1], 7)


def probar_algoritmo():
    tiempos, _ = leer_instancia(DATOS / 'tai20_5.txt')
    parametros = ParametrosACS(123, 5, 15, 0.1, 2.0, 0.9)
    secuencia_1, makespan_1, historial = ejecutar_acs(tiempos, parametros)
    secuencia_2, makespan_2, _ = ejecutar_acs(tiempos, parametros)

    # Reproducibilidad: misma semilla, misma secuencia y makespan.
    assert secuencia_1 == secuencia_2
    assert makespan_1 == makespan_2
    assert calcular_makespan(secuencia_1, tiempos) == makespan_1

    # La mejor solución mejora o se mantiene en cada iteración.
    mejores = [registro['mejor_makespan'] for registro in historial]
    assert mejores == sorted(mejores, reverse=True)
    assert all(
        registro['mejor_makespan'] <= registro['makespan_iteracion'] for registro in historial
    )


if __name__ == '__main__':
    probar_lectura_taillard()
    probar_makespan_calculado_a_mano()
    probar_secuencias_y_rpd()
    probar_heuristica()
    probar_feromonas()
    probar_construccion()
    probar_mejor_solucion()
    probar_algoritmo()
    print('Pruebas correctas.')
