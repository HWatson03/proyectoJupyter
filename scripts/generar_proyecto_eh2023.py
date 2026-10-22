"""Construye y ejecuta el notebook reproducible de la EH 2023 Vivienda."""

from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "analisis_encuesta_hogares_2023_vivienda.ipynb"


def md(source: str):
    return nbf.v4.new_markdown_cell(source.strip())


def code(source: str):
    return nbf.v4.new_code_cell(source.strip())


cells = [
    md(r"""
# Universidad Amazónica de Pando
## Carrera de Ingeniería de Sistemas
### Ingeniería de Software I

**Análisis de las características habitacionales de los hogares bolivianos según la Encuesta de Hogares 2023**

**Docente:** Ph. D. Juan Carlos Huanca Guanca  
**Autor:** Cristopher Coaquira  
**R.U.:** ____________________  
**Grupo:** ____________________  
**Lugar:** Cobija, Bolivia  
**Gestión:** 2026

---

## Perfil del estudio

La disponibilidad de vivienda adecuada, servicios básicos y espacio suficiente constituye una dimensión central de las condiciones de vida. Este análisis describe características físicas y de acceso a servicios de los hogares observados por la Encuesta de Hogares 2023 del Instituto Nacional de Estadística (INE). El archivo de trabajo contiene una observación por vivienda/hogar y cubre los nueve departamentos y las áreas urbana y rural.

**Objetivo.** Describir las características habitacionales observadas y presentar estimaciones ponderadas de materiales de paredes y fuente de agua, distinguiendo claramente las estadísticas de muestra de las estimaciones de población.

**Preguntas analíticas preliminares.** ¿Qué materiales predominan en las paredes? ¿Cuáles son las fuentes de agua reportadas? ¿Cómo se distribuyen el número de personas y de habitaciones? ¿Cómo difieren las características entre áreas urbana y rural? ¿Qué asociación descriptiva existe entre tamaño del hogar y habitaciones ocupadas?

**Selección.** La base oficial resulta pertinente porque mide directamente vivienda, tenencia, materiales, agua, saneamiento, energía, residuos, cocina, habitaciones e internet; además supera ampliamente el mínimo de 600 observaciones. El catálogo ANDA clasifica el archivo como de uso público. Se preserva el original y el cuaderno no exporta registros individuales.

**Fuente y metadatos:** [INE, Encuesta de Hogares 2023 (ANDA)](https://anda.ine.gob.bo/index.php/catalog/108), [diccionario de EH2023_Vivienda](https://anda.ine.gob.bo/index.php/catalog/108/data-dictionary/F2?file_name=EH2023_Vivienda), [materiales relacionados y diseño muestral](https://fm.ine.gob.bo/index.php/catalog/108/related-materials). La documentación publicada señala 12.815 casos y 36 variables. La copia local se verifica por separado y contiene una variable adicional, `Factor_Rev2025`.

**Diseño muestral.** El catálogo identifica `factor` como el factor de expansión y describe selección de UPM con probabilidad proporcional al tamaño y selección sistemática de viviendas. El archivo local añade `Factor_Rev2025`; el INE informa que sus series actualizadas usan factores ajustados a las Proyecciones de Población, revisión 2025. Por ello, los estimadores puntuales de población de este cuaderno usan `Factor_Rev2025`, mientras `factor` se conserva en el diccionario como el ponderador original. No se calculan errores estándar ni intervalos de confianza del diseño complejo; las conclusiones inferenciales quedan limitadas.

**Alcance.** Las estadísticas sin ponderar describen la muestra observada. Las tablas ponderadas son estimaciones puntuales con el factor indicado y no sustituyen un análisis de varianza que incorpore conglomerados y estratos.

**Limitaciones previstas.** El diseño es muestral; los módulos tienen saltos que producen faltantes estructurales; las variables de diseño se encuentran anonimizadas; el cuaderno no estima incertidumbre del diseño; y la copia local contiene una columna que no aparece en el listado de 36 variables del catálogo.

### Preparación del archivo

En una instalación local se utiliza por defecto la ruta original entregada. En Jupyter/Colab, se puede definir `EH2023_SAV_PATH` o editar la ruta en la siguiente celda. Instale las dependencias declaradas en `pyproject.toml` antes de ejecutar.
"""),
    md("## 1. Explicación — configuración y lectura\nSe leerá el SAV sin aplicar formatos de valor para conservar códigos numéricos y etiquetas en metadatos separados. No se modifica ni se sobrescribe el archivo fuente."),
    code(r'''
from pathlib import Path
import os
import json
import math
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyreadstat
from IPython.display import display, Markdown

pd.set_option("display.max_rows", 50)
pd.set_option("display.max_columns", 12)
pd.set_option("display.width", 160)
pd.set_option("display.max_colwidth", 100)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

ROOT = Path.cwd()
RUTA_SAV = Path(os.environ.get(
    "EH2023_SAV_PATH",
    "/home/usic03/Descargas/BD_EH2023/EH2023_Vivienda.sav"
))
if not RUTA_SAV.exists() and (ROOT / "data" / "EH2023_Vivienda.sav").exists():
    RUTA_SAV = ROOT / "data" / "EH2023_Vivienda.sav"
if not RUTA_SAV.exists():
    raise FileNotFoundError(
        "No se encontró el SAV. Defina EH2023_SAV_PATH con la ruta local "
        "o coloque EH2023_Vivienda.sav en data/."
    )

CARPETA_EXPORTACIONES = ROOT / "exportaciones_eh2023"
CARPETA_EXPORTACIONES.mkdir(parents=True, exist_ok=True)
'''),
    md("## 2. Resultado — dimensiones y metadatos\nLa siguiente lectura conserva los valores originales de las variables y devuelve los metadatos SPSS. El resultado reporta dimensiones locales comprobadas."),
    code(r'''
CODIGO_EXTRACTO_LITERAL = """datos, metadatos = pyreadstat.read_sav(str(RUTA_SAV), apply_value_formats=False)
assert datos.shape[0] > 600
print(f\"Dimensiones verificadas: {datos.shape[0]:,} registros × {datos.shape[1]} variables\")"""
exec(CODIGO_EXTRACTO_LITERAL)

etiquetas_variables = metadatos.column_names_to_labels or {}
etiquetas_valores = metadatos.variable_value_labels or {}
print(f"Codificación de texto: {metadatos.file_encoding}")
print(f"Etiquetas descriptivas disponibles: {len(etiquetas_variables)}")
print(f"Variables con etiquetas categóricas: {len(etiquetas_valores)}")
print(f"Campos de faltantes especiales declarados por SPSS: {len(metadatos.missing_ranges or {}) + len(metadatos.missing_user_values or {})}")
display(pd.DataFrame({
    "variable": datos.columns,
    "tipo_python": [str(datos[c].dtype) for c in datos.columns],
    "etiqueta_original_INE": [etiquetas_variables.get(c, "") for c in datos.columns],
}))
'''),
    md("## 3. Explicación — unidad de análisis y diccionario\nLa unidad es el registro de vivienda/hogar de la sección 6. Los códigos categóricos se interpretan con las etiquetas SPSS; no se usan como cantidades. Los ejemplos de identificadores y respuestas abiertas se enmascaran para no divulgar registros."),
    code(r'''
variables_cuantitativas = {"totper", "s06a_08a", "s06a_08b", "s06a_16", "s06a_17"}
variables_conteo = {"totper", "s06a_08a", "s06a_16", "s06a_17"}
variables_id = {"folio", "upm", "estrato"}
variables_peso = {"factor", "Factor_Rev2025"}
variables_texto = {c for c in datos.select_dtypes(include=["object", "str"]).columns}
texto_abierto = variables_texto - variables_id

def tipo_analitico(variable):
    if variable in variables_id:
        return "Identificador/diseño nominal"
    if variable in variables_peso:
        return "Cuantitativa continua (factor de expansión)"
    if variable in variables_cuantitativas:
        return "Cuantitativa discreta (conteo)" if variable in variables_conteo else "Cuantitativa discreta"
    if variable in texto_abierto:
        return "Categórica nominal (texto abierto)"
    return "Categórica nominal (código numérico)"

def ejemplo_seguro(variable):
    serie = datos[variable]
    no_nulos = serie.dropna()
    if variable in variables_id:
        return "Valor observado; identificador suprimido"
    if variable in texto_abierto:
        no_vacios = no_nulos.astype("string").str.strip().ne("")
        return "Respuesta textual observada; contenido suprimido" if no_vacios.any() else "Cadena vacía observada"
    if no_nulos.empty:
        return "Sin valor observado"
    valor = no_nulos.iloc[0]
    mapa = etiquetas_valores.get(variable, {})
    claves = [valor, str(valor)]
    if isinstance(valor, (int, float, np.number)):
        claves.extend([str(float(valor)), f"{float(valor):g}"])
    etiqueta = next((mapa[clave] for clave in claves if clave in mapa), None)
    if etiqueta:
        return f"{valor:g} = {etiqueta}" if isinstance(valor, (int, float, np.number)) else f"{valor} = {etiqueta}"
    return str(valor)

filas_diccionario = []
for variable in datos.columns:
    serie = datos[variable]
    categorias = etiquetas_valores.get(variable, {})
    categorias_texto = "; ".join(f"{k}: {v}" for k, v in categorias.items())
    rol = (
        "Identificador único de hogar" if variable == "folio" else
        "Variable de conglomerado/UPM" if variable == "upm" else
        "Variable de estratificación" if variable == "estrato" else
        "Factor de expansión original" if variable == "factor" else
        "Factor revisado con EPP 2025; ponderador utilizado" if variable == "Factor_Rev2025" else
        "Desagregación geográfica" if variable in {"depto", "area"} else
        "Variable cuantitativa principal" if variable in {"totper", "s06a_16", "s06a_17"} else
        "Respuesta abierta complementaria" if variable in texto_abierto else
        "Variable de caracterización habitacional"
    )
    filas_diccionario.append({
        "nombre_original": variable,
        "etiqueta_original_INE": etiquetas_variables.get(variable, ""),
        "etiquetas_de_valores_INE": categorias_texto,
        "ejemplo_real_seguro": ejemplo_seguro(variable),
        "tipo_tecnico": str(serie.dtype),
        "tipo_analitico": tipo_analitico(variable),
        "rol": rol,
        "nulos_SAV": int(serie.isna().sum()),
    })
diccionario = pd.DataFrame(filas_diccionario)
diccionario.to_csv(CARPETA_EXPORTACIONES / "diccionario_variables.csv", index=False, encoding="utf-8-sig")
display(diccionario)
print(f"Unidad de observación: vivienda/hogar; {len(datos):,} registros.")
'''),
    md("## 4. Explicación — auditoría de calidad\nSe contabilizan los nulos del archivo, las cadenas vacías por separado, los valores distintos y la unicidad. Se contrasta `folio` como clave candidata y se buscan duplicados exactos. Los nulos en preguntas condicionadas se interpretan como posibles saltos de cuestionario."),
    code(r'''
auditoria = pd.DataFrame({
    "nombre_original": datos.columns,
    "tipo_reconocido": [str(datos[c].dtype) for c in datos.columns],
    "nulos": [int(datos[c].isna().sum()) for c in datos.columns],
    "porcentaje_nulos": [datos[c].isna().mean() * 100 for c in datos.columns],
    "valores_unicos": [int(datos[c].nunique(dropna=True)) for c in datos.columns],
    "porcentaje_unicidad": [datos[c].nunique(dropna=True) / len(datos) * 100 for c in datos.columns],
    "cadenas_vacias": [int(datos[c].astype("string").str.strip().eq("").sum()) if c in variables_texto else 0 for c in datos.columns],
})
auditoria.to_csv(CARPETA_EXPORTACIONES / "auditoria_calidad.csv", index=False, encoding="utf-8-sig")
duplicados = int(datos.duplicated().sum())
folio_unicos = int(datos["folio"].nunique(dropna=True))
assert folio_unicos == len(datos), "folio no resultó único; no afirmar clave única"
assert duplicados == 0, "se detectaron duplicados exactos"

campos_faltantes = auditoria.loc[auditoria["nulos"] > 0].sort_values("nulos", ascending=False)
hallazgos_calidad = [
    f"No hay filas duplicadas exactas ({duplicados:,}) y folio identifica los {folio_unicos:,} registros sin repetición.",
    f"El máximo de nulos está en s06a_21: {int(auditoria.set_index('nombre_original').loc['s06a_21','nulos']):,} ({auditoria.set_index('nombre_original').loc['s06a_21','porcentaje_nulos']:.2f} %); es una pregunta de conexión fija y presenta salto de cuestionario.",
    f"La variable de agua semanal s06a_08a tiene {int(auditoria.set_index('nombre_original').loc['s06a_08a','nulos']):,} nulos ({auditoria.set_index('nombre_original').loc['s06a_08a','porcentaje_nulos']:.2f} %); se reportan como faltantes del archivo y no se imputan.",
]
print("Duplicados exactos:", duplicados)
print("folio único:", folio_unicos == len(datos), f"({folio_unicos:,} valores distintos)")
display(auditoria)
display(Markdown("### Tres hallazgos de calidad\n" + "\n".join(f"{i}. {h}" for i, h in enumerate(hallazgos_calidad, 1))))
'''),
    md("## 5. Explicación — pesos y estadística descriptiva\nLas tres variables de conteo elegidas son personas por hogar, habitaciones ocupadas y habitaciones destinadas exclusivamente a dormir. Se presentan estadísticos no ponderados de la muestra y la media ponderada como estimación puntual adicional. Para las variables categóricas se publican frecuencia de muestra y estimación ponderada usando `Factor_Rev2025`; las frecuencias muestrales no se interpretan como representativas por sí solas."),
    code(r'''
PESO = "Factor_Rev2025"
VARIABLES_NUMERICAS = ["totper", "s06a_16", "s06a_17"]
VARIABLES_CATEGORICAS = ["s06a_03", "s06a_07"]
assert PESO in datos.columns and datos[PESO].notna().all() and (datos[PESO] > 0).all()

filas_estadistica = []
for variable in VARIABLES_NUMERICAS:
    valores = datos[variable].dropna()
    pesos_validos = datos.loc[valores.index, PESO]
    filas_estadistica.append({
        "variable": variable,
        "etiqueta": etiquetas_variables.get(variable, ""),
        "n_observaciones_validas": int(valores.count()),
        "media_muestral": valores.mean(),
        "mediana_muestral": valores.median(),
        "desviacion_estandar_muestral": valores.std(ddof=1),
        "minimo": valores.min(),
        "Q1": valores.quantile(0.25),
        "Q3": valores.quantile(0.75),
        "maximo": valores.max(),
        "media_ponderada_Factor_Rev2025": np.average(valores, weights=pesos_validos),
    })
estadistica = pd.DataFrame(filas_estadistica)
estadistica.to_csv(CARPETA_EXPORTACIONES / "estadistica_descriptiva.csv", index=False, encoding="utf-8-sig")
display(estadistica.round(3))

def tabla_frecuencias(variable):
    serie = datos[variable]
    valido = serie.notna()
    conteos = serie[valido].value_counts(dropna=False)
    mapa = etiquetas_valores.get(variable, {})
    categorias = list(mapa.keys()) if mapa else list(conteos.index)
    filas = []
    total_muestra = int(valido.sum())
    total_ponderado = float(datos.loc[valido, PESO].sum())
    for categoria in categorias:
        # Las claves SPSS suelen ser texto aunque los códigos en pandas sean float.
        try:
            valor_categoria = float(categoria)
        except (TypeError, ValueError):
            valor_categoria = categoria
        mascara = valido & serie.eq(valor_categoria)
        n = int(mascara.sum())
        expandido = float(datos.loc[mascara, PESO].sum())
        etiqueta = mapa.get(categoria, mapa.get(str(categoria), str(categoria)))
        filas.append({
            "variable": variable,
            "codigo": categoria,
            "categoria_INE": etiqueta,
            "frecuencia_muestra": n,
            "porcentaje_muestra": n / total_muestra * 100 if total_muestra else np.nan,
            "estimacion_hogares_ponderada": expandido,
            "porcentaje_ponderado": expandido / total_ponderado * 100 if total_ponderado else np.nan,
        })
    tabla = pd.DataFrame(filas).sort_values("frecuencia_muestra", ascending=False, ignore_index=True)
    moda = tabla.iloc[0]
    return tabla, moda

frecuencias = {}
modas = {}
for indice, variable in enumerate(VARIABLES_CATEGORICAS, start=1):
    frecuencias[variable], modas[variable] = tabla_frecuencias(variable)
    frecuencias[variable].to_csv(CARPETA_EXPORTACIONES / f"frecuencias_categoria_{indice}.csv", index=False, encoding="utf-8-sig")
    print(f"Frecuencias de {variable}; moda muestral: {modas[variable]['categoria_INE']} ({int(modas[variable]['frecuencia_muestra']):,}; {modas[variable]['porcentaje_muestra']:.2f} %).")
    print(f"Estimación ponderada de la categoría modal: {modas[variable]['porcentaje_ponderado']:.2f} %; factor: {PESO}.")
    display(frecuencias[variable].round(3))
'''),
    md("## 6. Resultado — interpretación de estadísticos\nLas interpretaciones siguientes se calculan directamente de las tablas descriptivas y frecuencias. Los estadísticos de conteo describen la muestra; las proporciones ponderadas estiman la distribución de hogares bajo el ponderador documentado."),
    code(r'''
def fila_est(variable):
    return estadistica.set_index("variable").loc[variable]

interpretaciones_descriptivas = [
    f"En la muestra, el tamaño del hogar (`totper`) tiene n={int(fila_est('totper')['n_observaciones_validas']):,}, media {fila_est('totper')['media_muestral']:.2f} personas, mediana {fila_est('totper')['mediana_muestral']:.0f}, Q1={fila_est('totper')['Q1']:.0f}, Q3={fila_est('totper')['Q3']:.0f} y rango {fila_est('totper')['minimo']:.0f}–{fila_est('totper')['maximo']:.0f}.",
    f"Las habitaciones ocupadas (`s06a_16`) registran media {fila_est('s06a_16')['media_muestral']:.2f}, mediana {fila_est('s06a_16')['mediana_muestral']:.0f} y rango {fila_est('s06a_16')['minimo']:.0f}–{fila_est('s06a_16')['maximo']:.0f}; el 50 % central está entre Q1={fila_est('s06a_16')['Q1']:.0f} y Q3={fila_est('s06a_16')['Q3']:.0f}.",
    f"Las habitaciones exclusivas para dormir (`s06a_17`) tienen media muestral {fila_est('s06a_17')['media_muestral']:.2f} y mediana {fila_est('s06a_17')['mediana_muestral']:.0f}; su rango observado es {fila_est('s06a_17')['minimo']:.0f}–{fila_est('s06a_17')['maximo']:.0f}.",
    f"La moda muestral de material de paredes es “{modas['s06a_03']['categoria_INE']}”, con {int(modas['s06a_03']['frecuencia_muestra']):,} hogares ({modas['s06a_03']['porcentaje_muestra']:.2f} %); su porcentaje ponderado es {modas['s06a_03']['porcentaje_ponderado']:.2f} %.",
    f"La moda muestral de fuente de agua es “{modas['s06a_07']['categoria_INE']}”, con {int(modas['s06a_07']['frecuencia_muestra']):,} hogares ({modas['s06a_07']['porcentaje_muestra']:.2f} %); su porcentaje ponderado es {modas['s06a_07']['porcentaje_ponderado']:.2f} %.",
]
for i, texto in enumerate(interpretaciones_descriptivas, 1):
    print(f"{i}. {texto}")
'''),
    md("## 7. Distribuciones\nSe describen dos distribuciones cuantitativas y dos categóricas. Los rangos y cuartiles se refieren a observaciones válidas de la muestra; las proporciones categóricas ponderadas se identifican como estimaciones."),
    code(r'''
interpretaciones_distribuciones = [
    f"Distribución de personas por hogar: {int(fila_est('totper')['n_observaciones_validas']):,} valores válidos, rango {fila_est('totper')['minimo']:.0f}–{fila_est('totper')['maximo']:.0f}, mediana {fila_est('totper')['mediana_muestral']:.0f}, Q1 {fila_est('totper')['Q1']:.0f} y Q3 {fila_est('totper')['Q3']:.0f}.",
    f"Distribución de habitaciones ocupadas: {int(fila_est('s06a_16')['n_observaciones_validas']):,} valores válidos, rango {fila_est('s06a_16')['minimo']:.0f}–{fila_est('s06a_16')['maximo']:.0f}, mediana {fila_est('s06a_16')['mediana_muestral']:.0f}, Q1 {fila_est('s06a_16')['Q1']:.0f} y Q3 {fila_est('s06a_16')['Q3']:.0f}.",
    f"Material de paredes: la categoría más frecuente es “{modas['s06a_03']['categoria_INE']}” ({int(modas['s06a_03']['frecuencia_muestra']):,}; {modas['s06a_03']['porcentaje_muestra']:.2f} % de la muestra) y representa {modas['s06a_03']['porcentaje_ponderado']:.2f} % en la estimación ponderada.",
    f"Fuente de agua: la categoría más frecuente es “{modas['s06a_07']['categoria_INE']}” ({int(modas['s06a_07']['frecuencia_muestra']):,}; {modas['s06a_07']['porcentaje_muestra']:.2f} % de la muestra) y representa {modas['s06a_07']['porcentaje_ponderado']:.2f} % en la estimación ponderada.",
]
for i, texto in enumerate(interpretaciones_distribuciones, 1):
    print(f"{i}. {texto}")
'''),
    md("## 8. Visualizaciones\nSe generan exactamente cinco figuras. Los histogramas y el boxplot muestran la muestra no ponderada; las barras categóricas muestran porcentajes estimados con `Factor_Rev2025`. Cada archivo incluye título, ejes, escala y fuente."),
    code(r'''
figuras_interpretadas = []

def guardar_figura(figura, nombre):
    figura.tight_layout()
    figura.savefig(CARPETA_EXPORTACIONES / nombre, dpi=180, bbox_inches="tight")
    plt.show()
    plt.close(figura)

def texto_fuente(ax, ponderada=False):
    fuente = "Fuente: INE, Encuesta de Hogares 2023; elaboración propia."
    fuente += f"\nPonderador: {PESO}." if ponderada else " Estadística de muestra no ponderada."
    ax.text(0.01, -0.22, fuente, transform=ax.transAxes, fontsize=7, va="top")

# Figura 1: histograma de personas por hogar.
serie = datos["totper"].dropna()
fig, ax = plt.subplots(figsize=(8, 4.5))
bordes = np.arange(int(serie.min()) - 0.5, int(serie.max()) + 1.5, 1)
ax.hist(serie, bins=bordes, color="#2878B5", edgecolor="white")
ax.set(title="Personas por hogar en la muestra EH 2023", xlabel="Personas por hogar (personas)", ylabel="Hogares observados (n)")
ax.set_xticks(sorted(serie.unique()))
texto_fuente(ax)
guardar_figura(fig, "grafico_01_histograma_personas_hogar.png")
figuras_interpretadas.append(f"La figura 1 resume {len(serie):,} hogares: media {serie.mean():.2f} personas, mediana {serie.median():.0f} y Q1–Q3 de {serie.quantile(.25):.0f}–{serie.quantile(.75):.0f} personas.")

# Figura 2: histograma de habitaciones ocupadas.
serie = datos["s06a_16"].dropna()
fig, ax = plt.subplots(figsize=(8, 4.5))
bordes = np.arange(int(serie.min()) - 0.5, int(serie.max()) + 1.5, 1)
ax.hist(serie, bins=bordes, color="#46A77A", edgecolor="white")
ax.set(title="Habitaciones ocupadas por el hogar en la muestra EH 2023", xlabel="Habitaciones ocupadas (habitaciones)", ylabel="Hogares observados (n)")
ax.set_xticks(sorted(serie.unique()))
texto_fuente(ax)
guardar_figura(fig, "grafico_02_histograma_habitaciones.png")
figuras_interpretadas.append(f"La figura 2 incluye {len(serie):,} hogares; media {serie.mean():.2f}, mediana {serie.median():.0f}, Q1={serie.quantile(.25):.0f} y Q3={serie.quantile(.75):.0f} habitaciones.")

# Figura 3: porcentaje ponderado por material de paredes.
tabla = frecuencias["s06a_03"].sort_values("porcentaje_ponderado", ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(tabla["categoria_INE"], tabla["porcentaje_ponderado"], color="#D9822B")
ax.invert_yaxis()
ax.set(title="Material predominante en paredes — estimación ponderada", xlabel="Hogares estimados (%)", ylabel="Material de paredes")
texto_fuente(ax, ponderada=True)
guardar_figura(fig, "grafico_03_barras_material_paredes.png")
top = tabla.iloc[0]
segundo = tabla.iloc[1]
figuras_interpretadas.append(f"La figura 3 estima que “{top['categoria_INE']}” representa {top['porcentaje_ponderado']:.2f} % y “{segundo['categoria_INE']}” {segundo['porcentaje_ponderado']:.2f} % de los hogares ponderados; las bases muestrales son n={int(top['frecuencia_muestra']):,} y n={int(segundo['frecuencia_muestra']):,}.")

# Figura 4: porcentaje ponderado por fuente de agua.
tabla = frecuencias["s06a_07"].sort_values("porcentaje_ponderado", ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(tabla["categoria_INE"], tabla["porcentaje_ponderado"], color="#37A6B8")
ax.invert_yaxis()
ax.set(title="Procedencia principal del agua — estimación ponderada", xlabel="Hogares estimados (%)", ylabel="Fuente principal de agua")
texto_fuente(ax, ponderada=True)
top = tabla.iloc[0]
segundo = tabla.iloc[1]
figuras_interpretadas.append(f"La figura 4 estima {top['porcentaje_ponderado']:.2f} % para “{top['categoria_INE']}” y {segundo['porcentaje_ponderado']:.2f} % para “{segundo['categoria_INE']}”; sus frecuencias de muestra son {int(top['frecuencia_muestra']):,} y {int(segundo['frecuencia_muestra']):,} hogares.")
guardar_figura(fig, "grafico_04_barras_fuente_agua.png")

# Figura 5: boxplot de personas por hogar.
serie = datos["totper"].dropna()
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.boxplot(serie, orientation="horizontal", patch_artist=True, boxprops={"facecolor": "#9B78B5"}, medianprops={"color": "black", "linewidth": 2})
ax.set(title="Dispersión del tamaño del hogar en la muestra EH 2023", xlabel="Personas por hogar (personas)", yticks=[], ylabel="")
ax.set_xlim(left=0)
texto_fuente(ax)
guardar_figura(fig, "grafico_05_boxplot_personas_hogar.png")
q1, mediana, q3 = serie.quantile([.25, .5, .75])
figuras_interpretadas.append(f"La figura 5 muestra mediana de {mediana:.0f} personas e intervalo intercuartílico de {q1:.0f}–{q3:.0f}; el rango observado va de {serie.min():.0f} a {serie.max():.0f} personas.")

assert len(list(CARPETA_EXPORTACIONES.glob("grafico_*.png"))) == 5
for i, interpretacion in enumerate(figuras_interpretadas, 1):
    print(f"Interpretación de figura {i}: {interpretacion}")
'''),
    md("## 9. Preguntas analíticas\nEl plan combina dos preguntas descriptivas, dos comparativas y una relacional. Las comparaciones y asociaciones son descriptivas y no permiten atribuir causalidad. El análisis relacional se propone como correlación de Spearman, sin inferencia causal."),
    code(r'''
plan_preguntas = pd.DataFrame([
    {"tipo": "Descriptiva", "pregunta": "¿Qué materiales predominan en las paredes de las viviendas?", "variables": "s06a_03; Factor_Rev2025", "tecnica": "Frecuencias, porcentajes y estimación ponderada"},
    {"tipo": "Descriptiva", "pregunta": "¿Cuál es la distribución de las fuentes principales de agua?", "variables": "s06a_07; Factor_Rev2025", "tecnica": "Frecuencias, porcentajes y estimación ponderada"},
    {"tipo": "Comparativa", "pregunta": "¿Cómo varía el material de paredes entre áreas urbana y rural?", "variables": "s06a_03; area; Factor_Rev2025", "tecnica": "Tabla cruzada de porcentajes ponderados por área"},
    {"tipo": "Comparativa", "pregunta": "¿Cómo difiere el número de habitaciones ocupadas entre áreas urbana y rural?", "variables": "s06a_16; area; Factor_Rev2025", "tecnica": "Medias y distribuciones ponderadas por área; contraste descriptivo"},
    {"tipo": "Relacional", "pregunta": "¿Qué asociación descriptiva existe entre personas por hogar y habitaciones ocupadas?", "variables": "totper; s06a_16", "tecnica": "Correlación de Spearman y diagrama/tabulación exploratoria; sin causalidad"},
])
plan_preguntas.to_csv(CARPETA_EXPORTACIONES / "plan_preguntas.csv", index=False, encoding="utf-8-sig")
display(plan_preguntas)
'''),
    md("## 10. Hallazgos, limitaciones y conclusiones\nLos hallazgos se derivan de las tablas de salida. Las estimaciones ponderadas son puntuales; no se presentan como resultados con intervalos de confianza."),
    code(r'''
hallazgos = [
    interpretaciones_descriptivas[0],
    interpretaciones_descriptivas[1],
    interpretaciones_descriptivas[3],
    interpretaciones_descriptivas[4],
    f"El peso revisado suma {datos[PESO].sum():,.2f} hogares estimados en el conjunto de registros; el peso original factor suma {datos['factor'].sum():,.2f}. Ambos están completos, pero las estimaciones principales usan {PESO} por corresponder a la revisión 2025 informada por el INE.",
]
limitaciones = [
    "La Encuesta de Hogares es una muestra; las cifras muestrales sin ponderar no representan por sí solas a todos los hogares bolivianos.",
    "Se calculan estimaciones puntuales con Factor_Rev2025, pero no errores estándar, intervalos de confianza ni pruebas que incorporen completamente estratos y UPM.",
    "Las preguntas condicionadas generan faltantes estructurales; no se imputan ni se convierten en categorías sustantivas.",
    "La copia local contiene 37 columnas, mientras el diccionario público de ANDA lista 36; la columna adicional Factor_Rev2025 se identifica como revisión de ponderador.",
    "Los identificadores de UPM y estrato están anonimizados; los archivos agregados omiten identificadores y texto libre para proteger registros individuales.",
]
conclusiones = [
    f"La descripción de {len(datos):,} viviendas/hogares permite caracterizar materiales, agua y espacio doméstico en el conjunto de hogares observados.",
    f"Las tablas ponderadas con {PESO} ofrecen estimaciones puntuales coherentes con el factor revisado que acompaña a la base y con la nota de actualización del INE.",
    "Los resultados son descriptivos; para publicar inferencias con precisión muestral se requiere implementar el diseño complejo y documentar sus estimadores de varianza.",
]

for i, texto in enumerate(hallazgos, 1):
    print(f"Hallazgo {i}: {texto}")
print("Limitaciones:")
for i, texto in enumerate(limitaciones, 1):
    print(f"{i}. {texto}")
print("Conclusiones:")
for i, texto in enumerate(conclusiones, 1):
    print(f"{i}. {texto}")

resumen_resultados = pd.DataFrame({"tipo": ["Hallazgo"] * len(hallazgos) + ["Limitación"] * len(limitaciones) + ["Conclusión"] * len(conclusiones), "texto": hallazgos + limitaciones + conclusiones})
resumen_resultados.to_csv(CARPETA_EXPORTACIONES / "resumen_resultados.csv", index=False, encoding="utf-8-sig")
(CARPETA_EXPORTACIONES / "resumen_resultados.md").write_text(
    "# Resumen de resultados verificables\n\n" +
    "## Hallazgos\n" + "\n".join(f"{i}. {x}" for i, x in enumerate(hallazgos, 1)) +
    "\n\n## Limitaciones\n" + "\n".join(f"{i}. {x}" for i, x in enumerate(limitaciones, 1)) +
    "\n\n## Conclusiones\n" + "\n".join(f"{i}. {x}" for i, x in enumerate(conclusiones, 1)) + "\n",
    encoding="utf-8",
)
'''),
    md("## 11. Informe académico Word\nEl informe se arma con las tablas CSV y PNG generadas en las celdas anteriores. El fragmento de código se toma de `CODIGO_EXTRACTO_LITERAL`, que se ejecutó en la celda de lectura de este notebook."),
    code(r'''
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

RUTA_DOCX = ROOT / "Informe_Encuesta_Hogares_2023_Vivienda.docx"
doc = Document()
seccion = doc.sections[0]
seccion.top_margin = Inches(0.72)
seccion.bottom_margin = Inches(0.72)
seccion.left_margin = Inches(0.72)
seccion.right_margin = Inches(0.72)

for estilo in doc.styles:
    if estilo.type == 1:
        estilo.font.name = "Times New Roman"
        estilo.font.color.rgb = RGBColor(0, 0, 0)
        estilo._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        if estilo.name == "Normal":
            estilo.font.size = Pt(10)

def sombrear(celda, color="D9E2F3"):
    tc_pr = celda._tc.get_or_add_tcPr()
    sombreado = OxmlElement("w:shd")
    sombreado.set(qn("w:fill"), color)
    tc_pr.append(sombreado)

def repetir_encabezado(fila):
    tr_pr = fila._tr.get_or_add_trPr()
    encabezado = OxmlElement("w:tblHeader")
    encabezado.set(qn("w:val"), "true")
    tr_pr.append(encabezado)

def agregar_tabla(frame, columnas=None, max_filas=None, font_size=7):
    vista = frame if columnas is None else frame[columnas]
    if max_filas is not None:
        vista = vista.head(max_filas)
    tabla = doc.add_table(rows=1, cols=len(vista.columns))
    tabla.style = "Table Grid"
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    repetir_encabezado(tabla.rows[0])
    encabezado_trpr = tabla.rows[0]._tr.get_or_add_trPr()
    encabezado_trpr.append(OxmlElement("w:cantSplit"))
    for j, nombre in enumerate(vista.columns):
        celda = tabla.rows[0].cells[j]
        celda.text = str(nombre)
        sombrear(celda)
    for _, registro in vista.iterrows():
        fila = tabla.add_row()
        fila._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        celdas = fila.cells
        for j, valor in enumerate(registro.tolist()):
            celdas[j].text = "" if pd.isna(valor) else str(valor)
            celdas[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for fila in tabla.rows:
        for celda in fila.cells:
            for parrafo in celda.paragraphs:
                parrafo.paragraph_format.space_after = Pt(0)
                for run in parrafo.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(font_size)
                    run.font.color.rgb = RGBColor(0, 0, 0)
    return tabla

def agregar_lista(items):
    for item in items:
        doc.add_paragraph(str(item), style="List Bullet")

def agregar_imagen(nombre, pie):
    ruta = CARPETA_EXPORTACIONES / nombre
    doc.add_picture(str(ruta), width=Inches(6.3))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    parrafo = doc.add_paragraph(pie)
    parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Portada.
for linea in ["UNIVERSIDAD AMAZÓNICA DE PANDO", "CARRERA DE INGENIERÍA DE SISTEMAS", "INGENIERÍA DE SOFTWARE I"]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(linea)
    r.bold = True
    r.font.size = Pt(14 if "UNIVERSIDAD" in linea else 12)
doc.add_paragraph("\n\n")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("ANÁLISIS DE LAS CARACTERÍSTICAS HABITACIONALES DE LOS HOGARES BOLIVIANOS SEGÚN LA ENCUESTA DE HOGARES 2023")
r.bold = True
r.font.size = Pt(16)
doc.add_paragraph("\n\n")
for linea in ["Docente: Ph. D. Juan Carlos Huanca Guanca", "Autor: Cristopher Coaquira", "R.U.: ____________________", "Grupo: ____________________", "Cobija, Bolivia", "2026"]:
    p = doc.add_paragraph(linea)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_page_break()

doc.add_heading("Índice", level=1)
for titulo in [
    "Resumen",
    "1. Perfil y selección del dataset",
    "2. Caracterización general",
    "3. Diccionario de variables",
    "4. Diagnóstico de calidad",
    "5. Estadísticas descriptivas",
    "6. Análisis de distribuciones",
    "7. Visualizaciones",
    "8. Preguntas analíticas",
    "9. Hallazgos",
    "10. Limitaciones",
    "11. Conclusiones",
    "12. Reproducibilidad",
    "Referencias",
    "Anexos",
]:
    doc.add_paragraph(titulo, style="List Bullet")
doc.add_page_break()

doc.add_heading("Resumen", level=1)
doc.add_paragraph(
    f"El estudio caracteriza las condiciones habitacionales de {len(datos):,} viviendas/hogares incluidos en el archivo EH2023_Vivienda del Instituto Nacional de Estadística. La inspección local encontró {datos.shape[1]} variables, tipos mixtos, etiquetas categóricas SPSS, ausencia de duplicados exactos y una clave folio única. Se describen tres variables cuantitativas y dos categóricas. Los resultados de muestra se distinguen de las estimaciones puntuales ponderadas mediante {PESO}; no se calculan errores estándar del diseño complejo. No se publican registros individuales ni respuestas abiertas."
)
doc.add_paragraph("Palabras clave: vivienda, hogar, Encuesta de Hogares 2023, Bolivia, análisis exploratorio.")

doc.add_heading("1. Perfil y selección del dataset", level=1)
doc.add_paragraph("La vivienda adecuada y el acceso a servicios básicos son dimensiones relevantes del bienestar. La Encuesta de Hogares 2023 recoge características físicas y de servicios de las viviendas particulares en los nueve departamentos. La selección se justifica por su correspondencia temática, fuente oficial, disponibilidad de etiquetas y tamaño superior al requisito académico de 600 registros.")
doc.add_paragraph("Identificación: INE, Encuesta de Hogares 2023 (EH 2023), archivo EH2023_Vivienda, sección 6, parte A, preguntas 1 a 21. El catálogo ANDA declara uso público y registra 12.815 casos y 36 variables. La inspección del archivo local verificó 12.815 registros y 37 columnas; la variable adicional es Factor_Rev2025.")
doc.add_paragraph("Objetivo: describir las características habitacionales observadas y presentar estimaciones ponderadas para materiales de paredes y procedencia de agua.")

doc.add_heading("2. Caracterización general", level=1)
doc.add_paragraph(f"Dimensiones locales: {len(datos):,} registros × {datos.shape[1]} variables. Unidad de observación: vivienda/hogar. Cobertura: nueve departamentos, con áreas urbana y rural. El archivo contiene identificador anonimizado, variables geográficas, variables de vivienda, UPM, estrato y factores de expansión.")
doc.add_paragraph("Las variables codificadas numéricamente con etiquetas SPSS se trataron como categóricas cuando el código representa una opción de respuesta. Los conteos de personas y habitaciones se analizaron como cuantitativos. Los pesos se usaron únicamente para estimaciones ponderadas.")

seccion_diccionario = doc.add_section(WD_SECTION_START.NEW_PAGE)
seccion_diccionario.orientation = WD_ORIENT.LANDSCAPE
seccion_diccionario.page_width = Inches(11)
seccion_diccionario.page_height = Inches(8.5)
seccion_diccionario.top_margin = Inches(0.55)
seccion_diccionario.bottom_margin = Inches(0.55)
seccion_diccionario.left_margin = Inches(0.55)
seccion_diccionario.right_margin = Inches(0.55)
doc.add_heading("3. Diccionario de variables", level=1)
doc.add_paragraph("Se reproducen las etiquetas originales disponibles en el SAV. Las categorías se muestran con sus códigos y etiquetas. Los ejemplos de identificadores y texto abierto se enmascaran para evitar divulgación de registros.")
dic_doc = diccionario.copy()
dic_doc["etiquetas_de_valores_INE"] = dic_doc["etiquetas_de_valores_INE"].replace("", "—")
agregar_tabla(dic_doc, font_size=6)

seccion_retrato = doc.add_section(WD_SECTION_START.NEW_PAGE)
seccion_retrato.orientation = WD_ORIENT.PORTRAIT
seccion_retrato.page_width = Inches(8.5)
seccion_retrato.page_height = Inches(11)
seccion_retrato.top_margin = Inches(0.72)
seccion_retrato.bottom_margin = Inches(0.72)
seccion_retrato.left_margin = Inches(0.72)
seccion_retrato.right_margin = Inches(0.72)

doc.add_heading("4. Diagnóstico de calidad", level=1)
doc.add_paragraph(f"Se observaron {duplicados:,} filas duplicadas exactas. La variable folio presenta {folio_unicos:,} valores distintos para {len(datos):,} registros y funciona como clave única observada. Los metadatos SPSS no declararon rangos ni valores faltantes de usuario; los nulos detectados corresponden a valores faltantes del archivo, varios compatibles con saltos de preguntas condicionadas.")
agregar_tabla(auditoria.round(3), columnas=["nombre_original", "tipo_reconocido", "nulos", "porcentaje_nulos", "valores_unicos", "porcentaje_unicidad", "cadenas_vacias"], font_size=6)
doc.add_heading("Hallazgos de calidad", level=2)
agregar_lista(hallazgos_calidad)

doc.add_page_break()
doc.add_heading("5. Estadísticas descriptivas", level=1)
doc.add_paragraph("Las estadísticas de conteo son descriptivas de la muestra y no ponderadas. La media ponderada se incluye como estimación puntual de población. Las frecuencias categóricas presentan n y porcentaje muestral junto a la estimación ponderada con Factor_Rev2025.")
agregar_tabla(estadistica.round(3), font_size=7)
doc.add_heading("Material de paredes", level=2)
agregar_tabla(frecuencias["s06a_03"].round(3), font_size=7)
doc.add_heading("Procedencia principal del agua", level=2)
agregar_tabla(frecuencias["s06a_07"].round(3), font_size=7)

doc.add_heading("6. Análisis de distribuciones", level=1)
agregar_lista(interpretaciones_distribuciones)
doc.add_heading("Interpretaciones descriptivas", level=2)
agregar_lista(interpretaciones_descriptivas)

doc.add_heading("7. Visualizaciones", level=1)
pies = [
    "Figura 1. Histograma de personas por hogar (muestra no ponderada).",
    "Figura 2. Histograma de habitaciones ocupadas por hogar (muestra no ponderada).",
    "Figura 3. Material predominante de paredes (estimación ponderada con Factor_Rev2025).",
    "Figura 4. Procedencia principal del agua (estimación ponderada con Factor_Rev2025).",
    "Figura 5. Diagrama de caja de personas por hogar (muestra no ponderada).",
]
archivos_figura = ["grafico_01_histograma_personas_hogar.png", "grafico_02_histograma_habitaciones.png", "grafico_03_barras_material_paredes.png", "grafico_04_barras_fuente_agua.png", "grafico_05_boxplot_personas_hogar.png"]
for nombre, pie, interpretacion in zip(archivos_figura, pies, figuras_interpretadas):
    agregar_imagen(nombre, pie)
    doc.add_paragraph(interpretacion)

doc.add_heading("8. Preguntas analíticas", level=1)
doc.add_paragraph("Las preguntas comparativas y relacionales se plantean con fines exploratorios. Las asociaciones observadas no se interpretan como causales.")
agregar_tabla(plan_preguntas, font_size=8)

doc.add_heading("9. Hallazgos", level=1)
agregar_lista(hallazgos)
doc.add_heading("10. Limitaciones", level=1)
agregar_lista(limitaciones)
doc.add_heading("11. Conclusiones", level=1)
agregar_lista(conclusiones)

doc.add_heading("12. Reproducibilidad", level=1)
doc.add_paragraph("El análisis se ejecuta de principio a fin en el notebook analisis_encuesta_hogares_2023_vivienda.ipynb. La ruta del SAV puede definirse mediante EH2023_SAV_PATH. El entorno utiliza Python, pandas, NumPy, matplotlib, pyreadstat, Jupyter y python-docx. Las exportaciones contienen tablas agregadas y cinco imágenes; no incluyen filas individuales.")
doc.add_paragraph("Extracto literal del código ejecutado en el notebook:")
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.25)
r = p.add_run(CODIGO_EXTRACTO_LITERAL)
r.font.name = "Times New Roman"
r.font.size = Pt(9)
doc.add_paragraph("El extracto anterior se incorpora directamente desde la celda de lectura del notebook.")

doc.add_heading("Referencias", level=1)
referencias = [
    "Instituto Nacional de Estadística. (2024). Encuesta de Hogares 2023 (EH 2023): documentación y archivos de datos. Catálogo del Archivo Nacional de Datos (ANDA). https://anda.ine.gob.bo/index.php/catalog/108",
    "Instituto Nacional de Estadística. (2024). Diccionario de datos: EH2023_Vivienda, Encuesta de Hogares 2023. https://anda.ine.gob.bo/index.php/catalog/108/data-dictionary/F2?file_name=EH2023_Vivienda",
    "Instituto Nacional de Estadística. (2023). Diseño muestral de la Encuesta de Hogares 2023. Materiales relacionados, catálogo ANDA. https://fm.ine.gob.bo/index.php/catalog/108/related-materials",
    "Instituto Nacional de Estadística. (s. f.). Encuestas de hogares: vivienda y servicios básicos. https://www.ine.gob.bo/index.php/estadisticas-sociales/vivienda-y-servicios-basicos/encuestas-de-hogares-vivienda/",
]
for referencia in referencias:
    p = doc.add_paragraph(referencia)
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.first_line_indent = Inches(-0.3)

doc.add_heading("Anexos", level=1)
doc.add_paragraph("Anexo A. El diccionario completo se encuentra en el cuerpo del informe y en exportaciones_eh2023/diccionario_variables.csv. Anexo B. La auditoría se exporta en exportaciones_eh2023/auditoria_calidad.csv. Anexo C. Las tablas y figuras se generan desde el mismo notebook. Anexo D. El SAV original se conserva fuera del control de versiones y su ruta se configura localmente.")
doc.save(RUTA_DOCX)
print(f"Informe Word generado: {RUTA_DOCX}")
'''),
    md("## 12. Resultado — archivos exportados\nSe presentan las rutas creadas y la comprobación final de tablas, cinco figuras y dimensiones. No se exporta una tabla de muestra ni ningún identificador individual."),
    code(r'''
archivos_csv = sorted(CARPETA_EXPORTACIONES.glob("*.csv"))
archivos_png = sorted(CARPETA_EXPORTACIONES.glob("grafico_*.png"))
print(f"Registros: {len(datos):,}; variables: {datos.shape[1]}")
print("CSV agregados:")
for ruta in archivos_csv:
    print(f"- {ruta.relative_to(ROOT)} ({ruta.stat().st_size:,} bytes)")
print("Figuras PNG:")
for ruta in archivos_png:
    print(f"- {ruta.relative_to(ROOT)} ({ruta.stat().st_size:,} bytes)")
print(f"Informe: {RUTA_DOCX.relative_to(ROOT)}")
assert len(archivos_png) == 5
assert len(datos) > 600
assert not any("muestra" in p.name.lower() or "registro" in p.name.lower() for p in archivos_csv)
'''),
]

notebook = nbf.v4.new_notebook(cells=cells)
notebook.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12"},
}
NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
nbf.write(notebook, NOTEBOOK_PATH)
executed = NotebookClient(
    notebook,
    timeout=600,
    kernel_name="python3",
    resources={"metadata": {"path": str(ROOT)}},
    allow_errors=False,
).execute()
nbf.write(executed, NOTEBOOK_PATH)
print(f"Notebook ejecutado y guardado: {NOTEBOOK_PATH}")
