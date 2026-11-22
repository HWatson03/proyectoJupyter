# Resumen integrado de resultados verificables

## Hallazgos
1. En la muestra, el tamaño del hogar (`totper`) tiene n=12,815, media 3.17 personas, mediana 3, Q1=2, Q3=4 y rango 1–14.
2. Las habitaciones ocupadas (`s06a_16`) registran media 2.71, mediana 3 y rango 1–9; el 50 % central está entre Q1=2 y Q3=3.
3. La moda muestral de material de paredes es “1. LADRILLO/ BLOQUES DE CEMENTO/ HORMIGÓN”, con 9,702 hogares (75.71 %); su porcentaje ponderado es 75.57 %.
4. La moda muestral de fuente de agua es “1. Cañería de red dentro de la vivienda?”, con 6,817 hogares (53.20 %); su porcentaje ponderado es 47.66 %.
5. El peso revisado suma 3,799,194.10 hogares estimados en el conjunto de registros; el peso original factor suma 3,898,750.27. Ambos están completos, pero las estimaciones principales usan Factor_Rev2025 por corresponder a la revisión 2025 informada por el INE.
6. La correlación de Spearman entre personas por hogar y habitaciones ocupadas es rho=0.408 (n=12,815; asociación descriptiva).
7. El porcentaje ponderado de hogares sin electricidad para alumbrado es 3.60 %; la proporción muestral es 4.09 %.
8. La regresión logística logra F1=0.469, recall=0.933, precisión=0.313 y ROC-AUC=0.966 en la prueba; detecta 98 de 105 casos positivos.
9. La línea base alcanza accuracy=0.959, pero recall=0 para hogares sin electricidad, por lo que la exactitud sola no representa un buen desempeño en la clase minoritaria.

## Limitaciones
1. La Encuesta de Hogares es una muestra; las cifras muestrales sin ponderar no representan por sí solas a todos los hogares bolivianos.
2. Se calculan estimaciones puntuales con Factor_Rev2025, pero no errores estándar, intervalos de confianza ni pruebas que incorporen completamente estratos y UPM.
3. Las preguntas condicionadas generan faltantes estructurales; no se imputan ni se convierten en categorías sustantivas.
4. La copia local contiene 37 columnas, mientras el diccionario público de ANDA lista 36; la columna adicional Factor_Rev2025 se identifica como revisión de ponderador.
5. Los identificadores de UPM y estrato están anonimizados; los archivos agregados omiten identificadores y texto libre para proteger registros individuales.
6. La clase positiva (hogares sin electricidad) es minoritaria; la partición aleatoria de una sola muestra puede producir métricas variables.
7. El modelado no aplica pesos de expansión ni la estructura de estratos y UPM; sus métricas no son estimaciones poblacionales.
8. La selección por F1 se efectúa sobre una única partición de prueba, sin validación cruzada ni ajuste de hiperparámetros.

## Conclusiones
1. La descripción de 12,815 viviendas/hogares permite caracterizar materiales, agua y espacio doméstico en el conjunto de hogares observados.
2. Las tablas ponderadas con Factor_Rev2025 ofrecen estimaciones puntuales coherentes con el factor revisado que acompaña a la base y con la nota de actualización del INE.
3. Los resultados son descriptivos; para publicar inferencias con precisión muestral se requiere implementar el diseño complejo y documentar sus estimadores de varianza.
