"""Requerimiento 1 - Similitud textual entre abstracts.

Plan de modulos (cada uno expone una funcion f(texto_a, texto_b) -> float en [0, 1]).
Clasicos: 2 de programacion dinamica + 2 de espacio vectorial/conjuntos.
    levenshtein.py      distancia de edicion por programacion dinamica
    needleman_wunsch.py alineamiento global por programacion dinamica
    jaccard.py          coeficiente de Jaccard sobre conjuntos de tokens
    coseno_tfidf.py     pesos TF-IDF y similitud del coseno, desde cero
    embeddings.py       2 modelos de IA (embeddings densos) + coseno/euclidiana

Entrada comun: src.corpus.preprocesamiento.tokens_documento(doc).
"""
