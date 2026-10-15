"""Gráficos a partir de los CSV de AG, AM y ACS."""
import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


ALGORITMOS = ('AG', 'AM', 'ACS')
COLORES = {'AG': '#2563eb', 'AM': '#f59e0b', 'ACS': '#059669'}


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
    plt.title(f"Convergencia de {algoritmo} - {filas[0]['instancia']} (semilla {filas[0]['semilla']})")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(salida)
    plt.close()


def graficar_comparacion(carpeta, salida):
    """Genera una curva promedio por instancia desde una carpeta de ejecuciones."""
    grupos = {}
    for archivo in sorted(carpeta.glob('*.csv')):
        filas = leer_csv(archivo)
        if not filas or 'iteracion' not in filas[0]:
            raise ValueError(f'CSV de ejecución inválido: {archivo.name}')
        instancia = Path(filas[0]['instancia']).stem
        algoritmo = filas[0]['algoritmo']
        grupos.setdefault((instancia, algoritmo), []).append(filas)

    if not grupos:
        raise ValueError('La carpeta no contiene CSV de ejecuciones.')

    salida.mkdir(parents=True, exist_ok=True)
    generados = []
    for instancia in sorted({clave[0] for clave in grupos}):
        faltantes = [algoritmo for algoritmo in ALGORITMOS if (instancia, algoritmo) not in grupos]
        if faltantes:
            raise ValueError(f'Faltan ejecuciones de {", ".join(faltantes)} para {instancia}.')

        cantidades = {len(grupos[(instancia, algoritmo)]) for algoritmo in ALGORITMOS}
        if len(cantidades) != 1:
            raise ValueError(f'Los algoritmos no tienen igual cantidad de semillas para {instancia}.')

        plt.figure(figsize=(7, 4))
        referencia = None
        for algoritmo in ALGORITMOS:
            ejecuciones = grupos[(instancia, algoritmo)]
            iteraciones = [int(fila['iteracion']) for fila in ejecuciones[0]]
            if any([int(fila['iteracion']) for fila in filas] != iteraciones for filas in ejecuciones):
                raise ValueError(f'Las ejecuciones de {algoritmo} no comparten iteraciones en {instancia}.')
            curvas = [[int(fila['mejor_makespan']) for fila in filas] for filas in ejecuciones]
            plt.plot(iteraciones, np.mean(curvas, axis=0), label=algoritmo,
                     color=COLORES[algoritmo])
            referencia = int(ejecuciones[0][0]['mejor_conocido'])

        semillas = cantidades.pop()
        plt.axhline(referencia, color='#4b5563', linestyle='--',
                    label=f'Mejor conocido ({referencia})')
        plt.xlabel('Iteración')
        plt.ylabel('Mejor makespan acumulado')
        plt.title(f'Convergencia comparativa - {instancia}')
        plt.legend(ncol=4, fontsize=8)
        plt.grid(alpha=0.3)
        plt.figtext(0.5, 0.01, f'Curvas promedio de {semillas} semillas',
                    ha='center', fontsize=7, color='#4b5563')
        plt.tight_layout(rect=(0, 0.04, 1, 1))
        destino = salida / f'convergencia_{instancia}.pdf'
        plt.savefig(destino)
        plt.close()
        generados.append(destino)
    return generados


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
    plt.close(figura)


parser = argparse.ArgumentParser(description='Grafica resultados de AG, AM o ACS para PFSP.')
parser.add_argument(
    'resultados',
    help='CSV de una ejecución o carpeta con los CSV de la comparación.',
)
parser.add_argument(
    'salida',
    nargs='?',
    help='PDF de salida, o carpeta de salida si resultados es una carpeta.',
)
argumentos = parser.parse_args()

entrada = Path(argumentos.resultados)
if entrada.is_dir():
    salida = Path(argumentos.salida or Path(__file__).parent / 'graficos')
    try:
        generados = graficar_comparacion(entrada, salida)
    except (OSError, ValueError, KeyError) as error:
        parser.error(str(error))
    for generado in generados:
        print('Gráfico guardado en:', generado)
    return

try:
    filas = leer_csv(entrada)
except (OSError, ValueError, KeyError) as error:
    parser.error(str(error))
if not filas:
    parser.error('El archivo de resultados no contiene datos.')

salida = Path(argumentos.salida or Path(__file__).parent / 'graficos' / f'{entrada.stem}.pdf')
salida.parent.mkdir(parents=True, exist_ok=True)
if 'iteracion' in filas[0]:
    graficar_convergencia(filas, salida)
elif 'factor' in filas[0]:
    graficar_experimentos(filas, salida)
else:
    parser.error('El CSV no contiene iteraciones ni experimentos reconocibles.')
print('Gráfico guardado en:', salida)
