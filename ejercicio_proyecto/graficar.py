"""Gráficos de convergencia y de experimentos a partir de archivos CSV."""
import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def leer_csv(ruta):
    with open(ruta, newline='', encoding='utf-8') as archivo:
        return list(csv.DictReader(archivo))


def graficar_convergencia(filas, salida):
    iteraciones = [int(fila['iteracion']) for fila in filas]
    plt.figure(figsize=(7, 4))
    plt.plot(iteraciones, [int(fila['makespan_iteracion']) for fila in filas],
             alpha=0.4, label='Mejor de la iteración')
    plt.plot(iteraciones, [int(fila['mejor_makespan']) for fila in filas], label='Mejor global')
    plt.axhline(int(filas[0]['mejor_conocido']), color='gray', linestyle='--', label='Mejor conocido')
    plt.xlabel('Iteración')
    plt.ylabel('Makespan')
    algoritmo = filas[0].get('algoritmo') or 'ACS'
    plt.title(f"Convergencia de {algoritmo} — {filas[0]['instancia']} (semilla {filas[0]['semilla']})")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(salida)


def graficar_experimentos(filas, salida):
    instancias = list(dict.fromkeys(fila['instancia'] for fila in filas))
    factores = list(dict.fromkeys(fila['factor'] for fila in filas))
    figura, ejes = plt.subplots(2, 3, figsize=(13, 7))

    for eje, factor in zip(ejes.flat, factores):
        for instancia in instancias:
            grupo = [f for f in filas if f['factor'] == factor and f['instancia'] == instancia]
            valores = sorted({float(f['valor']) for f in grupo})
            rpd = [[float(f['rpd']) for f in grupo if float(f['valor']) == v] for v in valores]
            eje.errorbar(valores, [np.mean(grupo) for grupo in rpd],
                         yerr=[np.std(grupo) for grupo in rpd],
                         marker='o', capsize=3, label=instancia)
        eje.set_xlabel(factor)
        eje.set_ylabel('RPD medio (%)')
        eje.grid(alpha=0.3)

    eje = ejes.flat[len(factores)]
    for instancia in instancias:
        grupo = [f for f in filas if f['instancia'] == instancia]
        eje.scatter([float(f['tiempo_segundos']) for f in grupo],
                    [float(f['rpd']) for f in grupo], s=10, alpha=0.6, label=instancia)
    eje.set_xlabel('Tiempo (s)')
    eje.set_ylabel('RPD (%)')
    eje.set_title('Calidad vs. tiempo')
    eje.grid(alpha=0.3)
    eje.legend()

    figura.suptitle('Sensibilidad de ACS a sus parámetros (media ± desviación en 5 semillas)')
    figura.tight_layout()
    figura.savefig(salida)


def main():
    parser = argparse.ArgumentParser(description='Grafica resultados de AG, AM o ACS para PFSP.')
    parser.add_argument('resultados', help='CSV generado por ag.py, am.py, acs.py o experimentos.py.')
    parser.add_argument('salida', nargs='?', help='PDF de salida (por defecto graficos/<nombre>.pdf).')
    argumentos = parser.parse_args()

    try:
        filas = leer_csv(argumentos.resultados)
    except OSError as error:
        parser.error(str(error))
    if not filas:
        parser.error('El archivo de resultados no contiene datos.')

    salida = Path(argumentos.salida or Path(__file__).parent / 'graficos' / f'{Path(argumentos.resultados).stem}.pdf')
    salida.parent.mkdir(parents=True, exist_ok=True)
    if 'iteracion' in filas[0]:
        graficar_convergencia(filas, salida)
    elif 'factor' in filas[0]:
        graficar_experimentos(filas, salida)
    else:
        parser.error('El CSV no contiene iteraciones ni experimentos reconocibles.')
    print('Gráfico guardado en:', salida)


if __name__ == '__main__':
    main()
