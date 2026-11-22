# Proyecto Final — Análisis de la Encuesta de Hogares 2023

Proyecto académico de análisis descriptivo y modelado predictivo de las características habitacionales de los hogares bolivianos, para Ingeniería de Software I de la Universidad Amazónica de Pando.

## Estructura del proyecto

- `informe/Informe_Final.pdf`: informe final (lo agregará el equipo).
- `notebooks/Proyecto_Final.ipynb`: notebook ejecutable del análisis.
- `datos/`: ubicación opcional para el archivo original; no se versionan microdatos.
- `modelos/`: preprocesador y modelos entrenados para clasificar hogares sin electricidad.
- `resultados/tablas_y_figuras/`: diccionario, auditoría, tablas descriptivas, comparación de modelos y gráficos.
- `presentacion/Defensa_Proyecto.pptx`: presentación de defensa (la agregará el equipo).
- `guion/Guion_Video_Exposicion.md`: guion de 15–17 minutos; el equipo grabará el video.
- `requirements.txt`: dependencias de Python.
- `pyproject.toml` y `uv.lock`: definición del entorno con `uv`.

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

Con `pip`:

```bash
pip install -r requirements.txt
jupyter lab
```

También se puede abrir el notebook en Jupyter Notebook o Colab con las dependencias instaladas.

## Ubicar el archivo SPSS

El notebook busca el archivo en este orden:

1. La ruta configurada en la variable de entorno `EH2023_SAV_PATH`.
2. `/home/usic03/Descargas/BD_EH2023/EH2023_Vivienda.sav`.
3. `data/EH2023_Vivienda.sav` dentro del proyecto.
4. `datos/EH2023_Vivienda.sav` dentro del proyecto.

En otra computadora o en Colab, se recomienda establecer `EH2023_SAV_PATH` antes de ejecutar el notebook, o editar la ruta predeterminada en la primera sección de configuración. El SAV está excluido de Git por `.gitignore`; no debe añadirse a commits ni publicarse.

## Ejecutar el análisis

Abre `notebooks/Proyecto_Final.ipynb` y ejecuta todas las celdas en orden. El notebook detecta la raíz del proyecto si Jupyter lo inicia desde `notebooks/`. Lee el SAV sin reemplazar sus códigos por etiquetas, realiza análisis descriptivo, comparaciones exploratorias y entrena una línea base, regresión logística y árbol de decisión para detectar hogares sin electricidad. Genera métricas y gráficos agregados en `resultados/tablas_y_figuras/` y guarda los pipelines y el preprocesador en `modelos/`. No crea archivos con registros individuales ni genera el informe o la presentación.

El informe académico desarrolla los capítulos I–VI, referencias y anexos en el documento disponible en Drive y en `informe/Informe_Final.docx`. La carpeta `guion/` contiene el texto de exposición; el equipo debe grabar y entregar el video y preparar sus diapositivas.

Las estadísticas sin ponderar describen la muestra observada. Las tablas que usan `Factor_Rev2025` se presentan como estimaciones puntuales ponderadas. El ejercicio predictivo usa una partición aleatoria estratificada y métricas sin ponderar; no estima errores estándar ni incorpora plenamente estratos y UPM, por lo que no representa una evaluación de desempeño a escala poblacional.

## Fuente y referencias

- Instituto Nacional de Estadística de Bolivia, [Encuesta de Hogares 2023, catálogo ANDA](https://anda.ine.gob.bo/index.php/catalog/108).
- INE, [diccionario de datos del módulo EH2023_Vivienda](https://anda.ine.gob.bo/index.php/catalog/108/data-dictionary/F2?file_name=EH2023_Vivienda).
- INE, [materiales relacionados y documentación del diseño muestral](https://fm.ine.gob.bo/index.php/catalog/108/related-materials).

## Control de versiones

El trabajo se desarrolla en la rama `proyecto-encuesta-hogares-2023`. No se deben incluir microdatos originales ni archivos con observaciones individuales en commits.
