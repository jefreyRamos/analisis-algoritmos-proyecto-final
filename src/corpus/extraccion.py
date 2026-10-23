"""Extraccion de metadatos y abstracts de los 20 articulos PDF del corpus.

El resultado se guarda en data/abstracts.json para que los demas
requerimientos (ranking, similitud, clustering, busqueda de patrones)
trabajen sobre el mismo texto sin volver a leer los PDF.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from typing import Dict, List, Optional

from pypdf import PdfReader

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR_PDFS = os.path.join(RAIZ, "data", "pdfs")
RUTA_JSON = os.path.join(RAIZ, "data", "abstracts.json")

# Titulo, autores, anio y revista de cada articulo, transcritos y verificados
# a mano contra la primera pagina de cada PDF. La cabecera cambia demasiado
# entre editoriales (Elsevier, Springer, MDPI, Wiley, Emerald) para extraer
# los autores con un patron confiable, y el corpus es estatico.
RUTA_METADATOS = os.path.join(RAIZ, "data", "metadatos.json")

# Inicio del abstract: "ABSTRACT", "Abstract", "Abstract:" o "A B S T R A C T".
PATRON_INICIO = re.compile(r"A\s?B\s?S\s?T\s?R\s?A\s?C\s?T|Abstract", re.UNICODE)

# Fin del abstract: palabras clave, introduccion o pie de copyright.
# Es sensible a mayusculas a proposito: el abstract del articulo 15
# contiene la palabra "keywords" en minuscula dentro del texto.
PATRON_FIN = re.compile(
    r"Keywords|KEYWORDS|Key words|\n\s*1\.?\s*Introduction|\n\s*Introduction\b|\n\s*1\.\s*INTRODUCTION"
)

# Ajustes para articulos cuya maquetacion no sigue el patron general.
#  - 7: el bloque "Keywords" aparece ANTES del abstract (maquetacion Elsevier
#       a dos columnas), asi que el abstract empieza despues de la ultima keyword.
#  - 9: no hay "Keywords" ni "1. Introduction"; el cuerpo empieza directamente.
AJUSTES: Dict[int, Dict[str, str]] = {
    7: {"inicio_despues_de": "Ethical considerations"},
    9: {"fin_antes_de": "Since Alan Turing"},
}


def normalizar(texto: str) -> str:
    """Limpia artefactos de la extraccion de PDF."""
    # Ligaduras tipograficas que pypdf a veces separa con un espacio: "arti ﬁcial".
    texto = re.sub(r"\s?([ﬀ-ﬆ])", r"\1", texto)
    texto = unicodedata.normalize("NFKC", texto)
    # Palabras partidas por guion al final de linea: "practi-\ntioners", "cur -\nrent".
    texto = re.sub(r"(\w) ?-[ \t]*\n\s*(\w)", r"\1\2", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def _texto_primeras_paginas(ruta: str, paginas: int = 2) -> str:
    lector = PdfReader(ruta)
    return "\n".join((p.extract_text() or "") for p in lector.pages[:paginas])


def extraer_abstract(texto: str, numero: int) -> str:
    ajuste = AJUSTES.get(numero, {})

    if "inicio_despues_de" in ajuste:
        marca = ajuste["inicio_despues_de"]
        inicio = texto.index(marca) + len(marca)
    else:
        m = PATRON_INICIO.search(texto)
        if m is None:
            raise ValueError(f"No se encontro el abstract del articulo {numero}")
        inicio = m.end()

    resto = texto[inicio:]
    if "fin_antes_de" in ajuste:
        fin = resto.index(ajuste["fin_antes_de"])
    else:
        m = PATRON_FIN.search(resto)
        if m is None:
            raise ValueError(f"No se encontro el fin del abstract del articulo {numero}")
        fin = m.start()

    abstract = normalizar(resto[:fin])
    return abstract.lstrip(":").strip()


def _titulo_desde_archivo(nombre: str) -> str:
    sin_extension = os.path.splitext(nombre)[0]
    return re.sub(r"\s+", " ", sin_extension.split(".", 1)[1]).strip()


def cargar_metadatos(ruta: str = RUTA_METADATOS) -> Dict[int, dict]:
    with open(ruta, encoding="utf-8") as f:
        return {m["id"]: m for m in json.load(f)}


def construir_corpus(dir_pdfs: str = DIR_PDFS) -> List[dict]:
    archivos = [f for f in os.listdir(dir_pdfs) if f.lower().endswith(".pdf")]
    archivos.sort(key=lambda f: int(f.split(".", 1)[0]))
    metadatos = cargar_metadatos()

    corpus = []
    for nombre in archivos:
        numero = int(nombre.split(".", 1)[0])
        texto = _texto_primeras_paginas(os.path.join(dir_pdfs, nombre))
        meta = metadatos.get(numero, {})
        corpus.append({
            "id": numero,
            "archivo": nombre,
            "titulo": meta.get("titulo", _titulo_desde_archivo(nombre)),
            "autores": meta.get("autores", []),
            "anio": meta.get("anio"),
            "revista": meta.get("revista"),
            "abstract": extraer_abstract(texto, numero),
        })
    return corpus


def cargar_corpus(ruta_json: str = RUTA_JSON, regenerar: bool = False) -> List[dict]:
    """Devuelve el corpus desde la cache JSON; lo genera si no existe."""
    if regenerar or not os.path.exists(ruta_json):
        corpus = construir_corpus()
        with open(ruta_json, "w", encoding="utf-8") as f:
            json.dump(corpus, f, ensure_ascii=False, indent=2)
        return corpus
    with open(ruta_json, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    import logging

    logging.getLogger("pypdf").setLevel(logging.ERROR)
    for doc in cargar_corpus(regenerar=True):
        print(f"[{doc['id']:2d}] {len(doc['abstract'].split()):4d} palabras | {doc['abstract'][:70]}...")
