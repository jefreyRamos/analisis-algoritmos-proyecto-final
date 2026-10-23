"""Taller - Ranking de terminos mediante algoritmos de ordenamiento no comparativos.

Ejecucion (desde la raiz del proyecto):
    python -m src.ranking

Genera en resultados/:
    frecuencias.csv     lista completa (termino, frecuencia) en orden de entrada
    top15.csv           los 15 terminos mas frecuentes segun cada algoritmo
    tiempos.csv         tiempos de ejecucion (ms) sobre el corpus completo
    escalabilidad.csv   tiempos al replicar la lista de entrada 1x..32x
    top15.png, tiempos.png, escalabilidad.png
"""
from __future__ import annotations

import csv
import logging
import os
import platform
import statistics
import sys
import time
from typing import Callable, Dict, List, Tuple

from .corpus.extraccion import RAIZ, cargar_corpus
from .corpus.preprocesamiento import frecuencias_corpus
from .ordenamiento import ALGORITMOS

Par = Tuple[str, int]

DIR_RESULTADOS = os.path.join(RAIZ, "resultados")
TOP = 15
REPETICIONES = 200
FACTORES_ESCALA = [1, 2, 4, 8, 16, 32]
REPETICIONES_ESCALA = 20

# Paleta categorica validada (slots 1-3), un color fijo por algoritmo.
COLORES = {"Counting Sort": "#2a78d6", "Radix Sort": "#eb6834", "Bucket Sort": "#1baf7a"}
TINTA = "#2b2b29"
TINTA_SECUNDARIA = "#6b6a63"
REJILLA = "#e4e3dd"


def medir_ms(algoritmo: Callable[[List[Par]], List[Par]], pares: List[Par], repeticiones: int) -> List[float]:
    """Tiempo de pared de cada ejecucion en milisegundos (perf_counter_ns)."""
    algoritmo(pares)  # calentamiento: excluye el costo de la primera llamada
    tiempos = []
    for _ in range(repeticiones):
        t0 = time.perf_counter_ns()
        algoritmo(pares)
        tiempos.append((time.perf_counter_ns() - t0) / 1e6)
    return tiempos


def replicar(pares: List[Par], factor: int) -> List[Par]:
    """Entrada sintetica de tamano factor*n con la misma distribucion de frecuencias."""
    return [(f"{t}#{r}", f) for r in range(factor) for t, f in pares]


def _escribir_csv(nombre: str, encabezado: List[str], filas: List[list]) -> None:
    with open(os.path.join(DIR_RESULTADOS, nombre), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(encabezado)
        w.writerows(filas)


def _estilo_ejes(ax) -> None:
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(REJILLA)
    ax.tick_params(colors=TINTA_SECUNDARIA, labelsize=9)
    ax.set_axisbelow(True)


def graficar(top: List[Par], tiempos: Dict[str, List[float]], escala: Dict[str, List[float]], tamanos: List[int]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": TINTA, "axes.labelcolor": TINTA_SECUNDARIA})

    # Top 15: barras horizontales (magnitud de una sola serie).
    fig, ax = plt.subplots(figsize=(8, 5.2), dpi=150)
    terminos = [t for t, _ in top][::-1]
    valores = [f for _, f in top][::-1]
    barras = ax.barh(terminos, valores, color=COLORES["Counting Sort"], height=0.7)
    for b, v in zip(barras, valores):
        ax.text(b.get_width() + 1, b.get_y() + b.get_height() / 2, str(v), va="center", fontsize=8.5, color=TINTA)
    ax.grid(axis="x", color=REJILLA, linewidth=0.8)
    ax.set_xlabel("Frecuencia en los 20 abstracts")
    ax.set_title("Top 15 términos más frecuentes del corpus", loc="left", fontsize=12, color=TINTA)
    _estilo_ejes(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_RESULTADOS, "top15.png"))
    plt.close(fig)

    # Tiempos: mediana por algoritmo con rango intercuartilico.
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150)
    nombres = list(tiempos)
    medianas = [statistics.median(tiempos[a]) for a in nombres]
    q = {a: statistics.quantiles(tiempos[a], n=4) for a in nombres}
    errores = [[medianas[i] - q[a][0] for i, a in enumerate(nombres)], [q[a][2] - medianas[i] for i, a in enumerate(nombres)]]
    barras = ax.bar(nombres, medianas, color=[COLORES[a] for a in nombres], width=0.55,
                    yerr=errores, ecolor=TINTA_SECUNDARIA, capsize=4, error_kw={"linewidth": 1})
    for b, v in zip(barras, medianas):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() / 2, f"{v:.3f} ms",
                ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    ax.grid(axis="y", color=REJILLA, linewidth=0.8)
    ax.set_ylabel("Tiempo (ms), mediana")
    ax.set_title(f"Tiempo de ordenamiento sobre el corpus completo ({REPETICIONES} ejecuciones)",
                 loc="left", fontsize=11, color=TINTA)
    _estilo_ejes(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_RESULTADOS, "tiempos.png"))
    plt.close(fig)

    # Escalabilidad: tiempo vs n, con marcadores y etiqueta directa al final.
    fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=150)
    marcadores = {"Counting Sort": "o", "Radix Sort": "s", "Bucket Sort": "^"}
    for a, serie in escala.items():
        ax.plot(tamanos, serie, color=COLORES[a], linewidth=2, marker=marcadores[a], markersize=6, label=a)
        ax.annotate(a, (tamanos[-1], serie[-1]), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=TINTA)
    ax.grid(color=REJILLA, linewidth=0.8)
    ax.set_xlabel("n (número de términos en la entrada)")
    ax.set_ylabel("Tiempo (ms), mediana")
    ax.set_title("Crecimiento del tiempo con el tamaño de la entrada", loc="left", fontsize=11, color=TINTA)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_xlim(0, tamanos[-1] * 1.18)
    _estilo_ejes(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_RESULTADOS, "escalabilidad.png"))
    plt.close(fig)


def main() -> None:
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    os.makedirs(DIR_RESULTADOS, exist_ok=True)

    corpus = cargar_corpus()
    pares = frecuencias_corpus(corpus)
    n = len(pares)
    k = max(f for _, f in pares)
    total = sum(f for _, f in pares)
    print(f"Corpus: {len(corpus)} abstracts | {total} tokens utiles | n = {n} terminos distintos | k = {k}")

    _escribir_csv("frecuencias.csv", ["termino", "frecuencia"], [list(p) for p in pares])

    # Ordenamiento y validacion cruzada de los tres resultados.
    ordenados = {nombre: alg(pares) for nombre, alg in ALGORITMOS.items()}
    referencia = sorted(pares, key=lambda p: -p[1])  # solo para verificar (sorted es estable)
    for nombre, res in ordenados.items():
        estado = "OK" if res == referencia else "DIFERENTE"
        print(f"  {nombre:<14} validacion contra referencia: {estado}")

    filas_top = []
    for i in range(TOP):
        fila = [i + 1]
        for nombre in ALGORITMOS:
            fila += list(ordenados[nombre][i])
        filas_top.append(fila)
    encabezado = ["posicion"]
    for nombre in ALGORITMOS:
        encabezado += [f"{nombre} - termino", f"{nombre} - frecuencia"]
    _escribir_csv("top15.csv", encabezado, filas_top)

    print(f"\nTop {TOP} (identico en los tres algoritmos):")
    for i, (t, f) in enumerate(ordenados["Counting Sort"][:TOP], 1):
        print(f"  {i:2d}. {t:<16} {f}")

    # Medicion empirica sobre el corpus completo.
    tiempos = {nombre: medir_ms(alg, pares, REPETICIONES) for nombre, alg in ALGORITMOS.items()}
    filas_t = []
    print(f"\nTiempos sobre el corpus completo ({REPETICIONES} repeticiones, ms):")
    for nombre, ts in tiempos.items():
        fila = [nombre, n, k, REPETICIONES, min(ts), statistics.median(ts), statistics.mean(ts), statistics.stdev(ts), max(ts)]
        filas_t.append([fila[0], *fila[1:4], *(f"{x:.4f}" for x in fila[4:])])
        print(f"  {nombre:<14} min {fila[4]:.4f} | mediana {fila[5]:.4f} | media {fila[6]:.4f} | desv {fila[7]:.4f}")
    _escribir_csv("tiempos.csv", ["algoritmo", "n", "k", "repeticiones", "min_ms", "mediana_ms", "media_ms", "desv_ms", "max_ms"], filas_t)

    # Escalabilidad: misma distribucion (mismo k), n creciente.
    tamanos = []
    escala: Dict[str, List[float]] = {nombre: [] for nombre in ALGORITMOS}
    filas_e = []
    for factor in FACTORES_ESCALA:
        entrada = replicar(pares, factor)
        tamanos.append(len(entrada))
        fila = [factor, len(entrada)]
        for nombre, alg in ALGORITMOS.items():
            med = statistics.median(medir_ms(alg, entrada, REPETICIONES_ESCALA))
            escala[nombre].append(med)
            fila.append(f"{med:.4f}")
        filas_e.append(fila)
    _escribir_csv("escalabilidad.csv", ["factor", "n"] + [f"{a} (ms)" for a in ALGORITMOS], filas_e)
    print("\nEscalabilidad (mediana ms):")
    for fila in filas_e:
        print("  n = {:>6} | ".format(fila[1]) + " | ".join(f"{a}: {v}" for a, v in zip(ALGORITMOS, fila[2:])))

    graficar(ordenados["Counting Sort"][:TOP], tiempos, escala, tamanos)
    print(f"\nEntorno: Python {platform.python_version()} | {platform.processor() or platform.machine()} | {platform.system()} {platform.release()}")
    print(f"Resultados guardados en {DIR_RESULTADOS}")


if __name__ == "__main__":
    sys.exit(main())
