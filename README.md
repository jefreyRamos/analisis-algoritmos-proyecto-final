# Proyecto Final — Análisis de Algoritmos (2026-2)

Análisis computacional de los abstracts de 20 artículos sobre IA en educación.

## Estructura

```
data/pdfs/            20 artículos del corpus (PDF)
data/metadatos.json   título, autores, año y revista (verificados a mano contra cada PDF)
data/abstracts.json   corpus extraído: metadatos + abstract (cache compartida por todos los requerimientos)
src/corpus/           extracción de PDF y preprocesamiento de texto (tokens_documento, frecuencias)
src/ordenamiento/     Counting Sort, Radix Sort y Bucket Sort (implementados desde cero)
src/ranking.py        Seguimiento: ranking de términos + mediciones
src/similitud/        Req. 1 (por implementar; plan en __init__.py)
src/clustering/       Req. 2 (por implementar; plan en __init__.py)
src/busqueda/         Req. 3 (por implementar; plan en __init__.py)
tests/                pruebas unitarias (ordenamiento y corpus)
resultados/           CSV y gráficos generados
docs/                 documento del seguimiento (.docx) y su generador
```

## Uso

```bash
pip install -r requirements.txt
python -m src.corpus.extraccion        # regenera data/abstracts.json
python -m src.ranking                  # ranking, tiempos y gráficos en resultados/
python -m unittest discover -s tests   # pruebas
python -m docs.generar_documento       # docs/Taller_Ranking_Terminos.docx
```

## Estado

- [x] Seguimiento: ranking de términos (Counting / Radix / Bucket Sort)
- [x] Corpus con título, autores, año y revista para los requerimientos de cruce de información
- [ ] Req. 1: similitud textual (4 clásicos + 2 con IA)
- [ ] Req. 2: clustering jerárquico + dendrogramas
- [ ] Req. 3: búsqueda de patrones (KMP, Boyer-Moore, Rabin-Karp)
- [ ] Req. 4: despliegue + documentación técnica
