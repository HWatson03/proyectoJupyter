# Guion para el video de exposición

**Proyecto:** Caracterización y predicción del acceso a electricidad en los hogares bolivianos según la Encuesta de Hogares 2023  
**Duración sugerida:** 15–17 minutos  
**Formato:** exposición grupal con diapositivas y demostración real del notebook  
**Video:** lo grabará y entregará el equipo. Este archivo contiene únicamente el guion.

## Antes de grabar

- Reemplacen `[Integrante 1]`, `[Integrante 2]` y los demás campos por nombres y roles reales.
- Ajusten el reparto para que todas las personas participen de manera equilibrada.
- Abran `notebooks/Proyecto_Final.ipynb` desde la raíz del proyecto y preparen `modelos/` y `resultados/tablas_y_figuras/`.
- Usen las métricas de `resultados/tablas_y_figuras/comparacion_modelos.csv` y las figuras 6 y 7. No lean cifras de memoria si difieren de la ejecución final.
- En la demostración no muestren identificadores, respuestas abiertas ni credenciales.

## 1. Presentación del proyecto — 2 minutos

**[Integrante 1]**  
“Buenos días/tardes. Somos [nombres del equipo], estudiantes de Ingeniería de Sistemas de la Universidad Amazónica de Pando. Presentamos el proyecto *Caracterización y predicción del acceso a electricidad en los hogares bolivianos según la Encuesta de Hogares 2023*.”

“El proyecto estudia condiciones de vivienda y servicios básicos. Nos enfocamos en una pregunta concreta: ¿qué desempeño alcanzan una línea base, una regresión logística y un árbol de decisión al identificar hogares que reportaron no usar electricidad para alumbrar su vivienda?”

“Nuestro objetivo fue describir la muestra, explorar diferencias entre áreas urbana y rural y evaluar modelos de clasificación con métricas apropiadas para una clase minoritaria. Es un análisis observacional y predictivo; no buscamos demostrar causas.”

## 2. Datos y metodología — 3 minutos

**[Integrante 2]**  
“Usamos el archivo EH2023_Vivienda, publicado por el Instituto Nacional de Estadística de Bolivia en el catálogo ANDA. La copia local contiene 12.815 registros y 37 columnas. El catálogo público documenta 36 variables; en nuestra copia aparece además el ponderador revisado Factor_Rev2025.”

“La unidad de análisis es el registro de vivienda/hogar. El archivo incluye características de vivienda, materiales, agua, saneamiento, energía, habitaciones, área urbana o rural y departamento. No publicamos registros individuales; el archivo original permanece local y fuera del control de versiones.”

“Para clasificación usamos `s06a_12`: el código 1 significa que el hogar usa electricidad para alumbrar y el código 2 que no la usa. Definimos esta segunda categoría como clase positiva. En toda la muestra, 524 de 12.815 registros, el 4,09 por ciento, pertenecen a esa clase.”

“Separamos entrenamiento y prueba en proporción 80/20, con partición estratificada y semilla 42. Las imputaciones, la codificación one-hot y el escalado se ajustaron dentro de pipelines solo con entrenamiento, para evitar que la prueba influyera en el aprendizaje. Excluimos identificadores, variables de diseño, pesos de expansión y texto abierto.”

## 3. Exploración y desarrollo técnico — 4 minutos

**[Integrante 3]**  
“En el diagnóstico encontramos 12.815 registros, no observamos filas duplicadas exactas y el folio fue único en esta copia. También documentamos faltantes en preguntas condicionadas. Por ejemplo, la pregunta sobre el medio de conexión fija tiene 6.896 valores faltantes; no los interpretamos automáticamente como respuestas sustantivas.”

“En los descriptivos, el tamaño medio del hogar fue 3,17 personas, con mediana de 3. Las viviendas registraron una media de 2,71 habitaciones ocupadas. Para paredes, ladrillo, bloques de cemento u hormigón fue la categoría más frecuente; para el agua, la cañería de red dentro de la vivienda fue la categoría más frecuente. Las tablas ponderadas con Factor_Rev2025 se presentan como estimaciones puntuales.”

“En la comparación por área, la proporción ponderada de paredes de ladrillo o bloques fue de 89,79 por ciento en el área urbana y 44,34 por ciento en el área rural. La media ponderada de habitaciones ocupadas fue 2,75 en el área urbana y 2,36 en la rural. La correlación de Spearman entre personas por hogar y habitaciones fue 0,408; la interpretamos como asociación descriptiva, no como causalidad.”

“Para la fase predictiva comparamos una línea base que predice la clase mayoritaria, una regresión logística con balance de clases y un árbol de decisión limitado en profundidad y tamaño de hoja. Guardamos los pipelines completos y el preprocesador en la carpeta `modelos`.”

## 4. Evaluación y demostración técnica — 4–6 minutos

**[Integrante 4 o quien demuestre]**  
“En pantalla mostramos el notebook principal y cómo se generan las tablas, los gráficos y los modelos. La prueba contiene 2.563 casos, incluidos 105 hogares sin electricidad.”

“La línea base obtuvo accuracy de 0,959, pero no detectó ninguno de los 105 hogares sin electricidad: su recall y F1 para la clase positiva son cero. Esto muestra por qué una exactitud alta puede ser engañosa cuando hay desbalance.”

“La regresión logística fue seleccionada por F1. Alcanzó recall de 0,933, precisión de 0,313, F1 de 0,469 y ROC-AUC de 0,966. Identificó 98 de los 105 casos positivos, pero generó 215 falsos positivos. El árbol alcanzó recall de 0,886, precisión de 0,285 y F1 de 0,432.”

“Mostramos la matriz de confusión y la curva ROC. La precisión moderada significa que muchas alertas del modelo corresponden a hogares que sí reportaron electricidad. Por eso el modelo sirve como ejercicio analítico y no como mecanismo de decisión automática.”

**Demostración en pantalla:**

1. Mostrar la celda donde se define `s06a_12` y se separan entrenamiento y prueba.
2. Mostrar el pipeline de imputación, codificación y escalado.
3. Mostrar la tabla `comparacion_modelos.csv` y la figura `grafico_06_matrices_confusion.png`.
4. Mostrar `modelos/` y la comprobación que carga el modelo y reproduce las predicciones.
5. Si no se ejecutará el notebook en vivo, mostrar los archivos y resultados generados por la ejecución reproducible, identificándolos como salidas del proyecto.

## 5. Cierre: hallazgos, límites y recomendaciones — 2–3 minutos

**[Integrante 1 o cierre grupal]**  
“Concluimos que la regresión logística detectó la mayoría de los casos sin electricidad en la partición de prueba, aunque con bastantes falsos positivos. La línea base obtuvo buena accuracy por predecir la clase mayoritaria, pero no resolvió el objetivo de identificar la clase minoritaria.”

“Los resultados tienen límites: el modelo se evaluó con una sola partición, sin validación cruzada y sin incorporar ponderadores, estratos ni UPM. Por tanto, sus métricas no son estimaciones de desempeño para todos los hogares de Bolivia y no demuestran relaciones causales.”

“Recomendamos revisar precision y recall en conjunto, probar estabilidad con validación cruzada y, para inferencias poblacionales, diseñar una evaluación que respete el muestreo complejo. Agradecemos su atención y quedamos atentos a sus preguntas.”

## Lista de comprobación de grabación

- Duración final entre 12 y 18 minutos.
- Todos los integrantes aparecen o intervienen de forma identificable y equilibrada.
- Se muestra el notebook real o la recuperación verificable de modelos y resultados.
- Las métricas mencionadas coinciden con el notebook y el informe.
- Audio claro, pantalla horizontal, figuras legibles y permisos correctos si se entrega un enlace.
- No se incluyen credenciales, datos personales o filas individuales.
