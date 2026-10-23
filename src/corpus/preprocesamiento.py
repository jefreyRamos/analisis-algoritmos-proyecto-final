"""Preprocesamiento de los abstracts: tokenizacion, stopwords y frecuencias."""
from __future__ import annotations

import re
from typing import Dict, Iterable, List, Tuple

# Stopwords del ingles (los abstracts del corpus estan en ingles) mas
# palabras de relleno propias de los abstracts academicos que no aportan
# informacion sobre el dominio ("study", "paper", "results"... se conservan
# a proposito porque si describen el tipo de investigacion).
STOPWORDS = frozenset("""
a about above after again against all also although am an and any are as at
be because been before being below between both but by can could did do does
doing down during each either et etc few for from further had has have having
he her here hers herself him himself his how however i if in into is it its
itself just may me might more most must my myself no nor not now of off on
once only or other our ours ourselves out over own per same shall she should
since so some such than that the their theirs them themselves then there
these they this those through thus to too under until up upon us very via was
we were what when where whereas whether which while who whom whose why will
with within without would yet you your yours yourself yourselves
""".split())

PATRON_TOKEN = re.compile(r"[a-z]+")


def tokenizar(texto: str) -> List[str]:
    """Minusculas y secuencias de letras; descarta numeros y signos."""
    return PATRON_TOKEN.findall(texto.lower())


def limpiar(tokens: Iterable[str], longitud_minima: int = 2) -> List[str]:
    # longitud_minima = 2 conserva "ai", el termino central del dominio.
    return [t for t in tokens if len(t) >= longitud_minima and t not in STOPWORDS]


def contar_frecuencias(tokens: Iterable[str]) -> Dict[str, int]:
    """Tabla hash termino -> frecuencia. O(n) esperado.

    El diccionario conserva el orden de primera aparicion, que es el orden
    de entrada que reciben los algoritmos de ordenamiento.
    """
    frecuencias: Dict[str, int] = {}
    for t in tokens:
        frecuencias[t] = frecuencias.get(t, 0) + 1
    return frecuencias


def tokens_documento(doc: dict) -> List[str]:
    """Tokens utiles del abstract de un documento, en orden de aparicion.

    Es la representacion comun para similitud (Req. 1) y clustering (Req. 2).
    """
    return limpiar(tokenizar(doc["abstract"]))


def frecuencias_corpus(corpus: List[dict]) -> List[Tuple[str, int]]:
    """Lista (termino, frecuencia) sobre los abstracts de todo el corpus."""
    tokens: List[str] = []
    for doc in corpus:
        tokens.extend(tokens_documento(doc))
    return list(contar_frecuencias(tokens).items())
