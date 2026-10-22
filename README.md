# Análisis de la Encuesta de Hogares 2023 — Vivienda

Proyecto académico de análisis exploratorio de las características habitacionales de los hogares bolivianos, para Ingeniería de Software I de la Universidad Amazónica de Pando.

## Contenido

- `analisis_encuesta_hogares_2023_vivienda.ipynb`: notebook ejecutable con inspección del archivo SPSS, auditoría de calidad, análisis descriptivo, cinco visualizaciones y exportaciones agregadas.
- `exportaciones_eh2023/`: diccionario de variables, auditoría, tablas descriptivas y de frecuencias, plan de preguntas, resumen de resultados y cinco gráficos PNG.
- `Informe Encuesta Hogares 2023 Vivienda.docx`: documentación académica existente. El notebook no crea ni modifica documentos Word.
- `pyproject.toml` y `uv.lock`: dependencias para reproducir el análisis.

El proyecto no contiene microdatos versionados. El archivo original `EH2023_Vivienda.sav` debe obtenerse desde la fuente oficial del [INE de Bolivia, catálogo ANDA](https://anda.ine.gob.bo/index.php/catalog/108), y guardarse localmente.

## Requisitos

- Python 3.12 o posterior.
- `uv` para instalar el entorno declarado, o instalación equivalente de las dependencias de `pyproject.toml`.
- Jupyter Notebook, JupyterLab o Google Colab.
- El archivo original `EH2023_Vivienda.sav`.

## Preparar el entorno

Con `uv`:

```bash
uv sync
uv run jupyter lab
```

También se puede abrir el notebook en Jupyter Notebook o Colab con las dependencias instaladas.

## Ubicar el archivo SPSS

El notebook busca el archivo en este orden:

1. La ruta configurada en la variable de entorno `EH2023_SAV_PATH`.
2. `/home/usic03/Descargas/BD_EH2023/EH2023_Vivienda.sav`.
3. `data/EH2023_Vivienda.sav` dentro del proyecto.

En otra computadora o en Colab, se recomienda establecer `EH2023_SAV_PATH` antes de ejecutar el notebook, o editar la ruta predeterminada en la primera sección de configuración. El SAV está excluido de Git por `.gitignore`; no debe añadirse a commits ni publicarse.

## Ejecutar el análisis

Abre `analisis_encuesta_hogares_2023_vivienda.ipynb` y ejecuta todas las celdas en orden. El notebook lee el SAV sin reemplazar sus códigos por etiquetas, documenta los metadatos SPSS y genera los CSV agregados y cinco gráficos PNG en `exportaciones_eh2023/`. No crea un CSV con registros individuales y no genera documentos Word.

Las estadísticas sin ponderar describen la muestra observada. Las tablas que usan `Factor_Rev2025` se presentan como estimaciones puntuales ponderadas. El notebook no estima errores estándar ni intervalos de confianza que incorporen plenamente el diseño muestral.

## Fuente y referencias

- Instituto Nacional de Estadística de Bolivia, [Encuesta de Hogares 2023, catálogo ANDA](https://anda.ine.gob.bo/index.php/catalog/108).
- INE, [diccionario de datos del módulo EH2023_Vivienda](https://anda.ine.gob.bo/index.php/catalog/108/data-dictionary/F2?file_name=EH2023_Vivienda).
- INE, [materiales relacionados y documentación del diseño muestral](https://fm.ine.gob.bo/index.php/catalog/108/related-materials).

## Control de versiones

El trabajo se desarrolla en la rama `proyecto-encuesta-hogares-2023`. No se deben incluir microdatos originales ni archivos con observaciones individuales en commits.
