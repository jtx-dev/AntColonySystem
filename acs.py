from pathlib import Path

import pandas as pd

from operadores import calcular_distancias, leer_datos


def main():
    entrada = Path(__file__).parent / 'datos' / 'instancia.txt'
    coordenadas, n = leer_datos(entrada)
    matriz_distancias = calcular_distancias(coordenadas, n)

    print(f'Ciudades leídas: {n}')
    print(f'Tamaño de la matriz: {matriz_distancias.shape}')

    cantidad_mostrada = min(10, n)
    ciudades = range(1, cantidad_mostrada + 1)
    vista_previa = pd.DataFrame(
        matriz_distancias[:cantidad_mostrada, :cantidad_mostrada],
        index=ciudades,
        columns=ciudades,
    )
    vista_previa.index.name = 'Ciudad'

    print(f'\nVista previa de las primeras {cantidad_mostrada} ciudades:')
    print(vista_previa.round(2).to_string())


if __name__ == '__main__':
    main()
