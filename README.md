# Detección de Cumplimiento de Normas de Seguridad en Obras de Construcción mediante YOLOv8

Este repositorio contiene el desarrollo de un prototipo de visión computacional para detectar equipos de protección personal (EPP) en imágenes de obras de construcción utilizando YOLOv8.

El proyecto incluye la construcción de un dataset combinado, entrenamiento de un modelo YOLOv8s, validación del modelo, pruebas con imágenes externas reales de obra y un verificador de cumplimiento basado en reglas espaciales.

## 1. Descripción general

La supervisión del uso de equipos de protección personal en obras de construcción es una tarea crítica para reducir riesgos laborales. Sin embargo, la revisión manual puede ser limitada cuando existen múltiples frentes de trabajo, gran cantidad de trabajadores, baja iluminación, oclusión, trabajadores de espalda o imágenes tomadas desde diferentes ángulos.

Este proyecto propone un sistema basado en detección de objetos que permite:

- Detectar personas o trabajadores.
- Detectar cascos de seguridad.
- Detectar ausencia de casco.
- Detectar chalecos.
- Detectar ausencia de chaleco.
- Detectar guantes.
- Detectar gafas.
- Detectar botas.
- Asociar los EPP detectados a cada persona.
- Calcular tasa de cumplimiento de casco.
- Calcular tasa de cumplimiento completo.
- Generar imágenes anotadas.
- Generar un resumen CSV con los resultados por imagen.

## 2. Ejecución de extremo a extremo

El código puede ejecutarse de extremo a extremo con un único comando documentado.

Primero, instalar las dependencias:

```bash
pip install -r requirements.txt
```

Luego, ejecutar el pipeline completo de demostración:

```bash
python run_pipeline.py --mode demo
```

Este comando realiza automáticamente:

1. Carga del detector auxiliar de personas YOLOv8 preentrenado en COCO.
2. Carga del modelo YOLOv8s entrenado para detección de EPP.
3. Lectura de imágenes desde `data/demo_images/`.
4. Detección de personas.
5. Detección de EPP.
6. Asociación espacial entre personas y EPP.
7. Cálculo de cumplimiento de casco.
8. Cálculo de cumplimiento completo.
9. Generación de imágenes anotadas.
10. Generación del archivo `resumen_cumplimiento.csv`.

Los resultados se guardan en:

```text
results/demo_outputs/
```

También se puede ejecutar indicando rutas personalizadas:

```bash
python run_pipeline.py --mode demo --input data/demo_images --output results/demo_outputs --weights weights/best.pt
```

## 3. Objetivo general

Desarrollar y evaluar un prototipo de visión computacional basado en YOLOv8 para detectar trabajadores y equipos de protección personal en imágenes de obra, implementando un verificador de cumplimiento mediante reglas espaciales.

## 4. Objetivos específicos

* Construir un dataset combinado para detección de EPP.
* Convertir anotaciones del dataset SHWD desde Pascal VOC hacia formato YOLO.
* Entrenar un modelo YOLOv8s para detección multiclase.
* Evaluar el modelo con métricas de detección de objetos.
* Analizar curvas de entrenamiento, matriz de confusión y resultados por clase.
* Implementar un detector auxiliar de personas usando YOLOv8 preentrenado en COCO.
* Asociar espacialmente cada EPP detectado con una persona.
* Calcular cumplimiento de casco y cumplimiento completo.
* Probar el sistema con imágenes reales externas de obra.
* Analizar el efecto de la oclusión en el desempeño del sistema.

## 5. Clases del modelo

El modelo final considera ocho clases:

| ID | Clase     | Descripción              |
| -: | --------- | ------------------------ |
|  0 | person    | Persona o trabajador     |
|  1 | helmet    | Casco de seguridad       |
|  2 | no_helmet | Cabeza/persona sin casco |
|  3 | vest      | Chaleco de seguridad     |
|  4 | no_vest   | Ausencia de chaleco      |
|  5 | gloves    | Guantes                  |
|  6 | goggles   | Gafas de seguridad       |
|  7 | boots     | Botas de seguridad       |

## 6. Datasets utilizados

Para construir el dataset combinado se utilizaron las siguientes fuentes:

1. Safety Helmet Detection Dataset.
2. PPE Detection Dataset.
3. Worker Detection Dataset.
4. SafetyHelmetWearing Dataset, SHWD.

Cada dataset fue revisado, remapeado y adaptado al esquema de clases finales.

## 7. Remapeo de clases

| Dataset                 | Clase original | Clase final |
| ----------------------- | -------------- | ----------- |
| Safety Helmet Detection | head           | no_helmet   |
| Safety Helmet Detection | helmet         | helmet      |
| Safety Helmet Detection | person         | person      |
| PPE Detection           | helmet         | helmet      |
| PPE Detection           | no-helmet      | no_helmet   |
| PPE Detection           | vest           | vest        |
| PPE Detection           | no-vest        | no_vest     |
| PPE Detection           | gloves         | gloves      |
| PPE Detection           | goggles        | goggles     |
| PPE Detection           | boots          | boots       |
| Worker Detection        | person         | person      |
| Worker Detection        | worker         | person      |
| SHWD                    | hat            | helmet      |
| SHWD                    | person         | no_helmet   |
| SHWD                    | dog            | ignorada    |

## 8. Dataset combinado final

La distribución final del dataset combinado fue:

| Split | Imágenes | Etiquetas |
| ----- | -------: | --------: |
| train |   22,509 |    22,509 |
| valid |    3,173 |     3,173 |
| test  |    2,822 |     2,822 |

Distribución final de anotaciones:

| Clase     | Anotaciones |
| --------- | ----------: |
| person    |       6,328 |
| helmet    |      67,396 |
| no_helmet |     128,538 |
| vest      |       5,841 |
| no_vest   |       1,175 |
| gloves    |       1,549 |
| goggles   |         588 |
| boots     |       4,601 |

El dataset completo no se incluye en este repositorio debido a su tamaño. Se recomienda almacenarlo en Google Drive o Roboflow.

## 9. Estructura del repositorio

```text
ppe-compliance-yolov8/
│
├── README.md
├── requirements.txt
├── .gitignore
├── run_pipeline.py
│
├── notebooks/
│   ├── 01_modelo_base_casco.ipynb
│   ├── 02_dataset_combinado_ppe_shwd.ipynb
│   └── 03_modelo_final_yolo_ppe.ipynb
│
├── data/
│   ├── README.md
│   └── demo_images/
│       ├── obra_01.jpg
│       ├── obra_02.jpg
│       └── ...
│
├── weights/
│   └── README.md
│
└── results/
    ├── README.md
    └── demo_outputs/
```

## 10. Notebooks del proyecto

### Notebook 1: Modelo base de casco

Archivo:

```text
notebooks/01_modelo_base_casco.ipynb
```

Este notebook entrena una primera línea base con el Safety Helmet Detection Dataset. Permite evaluar la detección inicial de casco, no casco y persona.

### Notebook 2: Dataset combinado PPE + SHWD

Archivo:

```text
notebooks/02_dataset_combinado_ppe_shwd.ipynb
```

Este notebook descarga, revisa, remapea e integra diferentes datasets. También convierte SHWD desde formato Pascal VOC hacia YOLO y genera el dataset combinado final.

### Notebook 3: Modelo final YOLOv8 PPE

Archivo:

```text
notebooks/03_modelo_final_yolo_ppe.ipynb
```

Este notebook entrena el modelo YOLOv8s final, valida sobre test, genera métricas, muestra predicciones, implementa los verificadores V1, V2 y V3, y analiza imágenes externas reales de obra.

## 11. Configuración del entrenamiento

El entrenamiento final fue realizado con la siguiente configuración:

| Parámetro        | Valor        |
| ---------------- | ------------ |
| Modelo base      | YOLOv8s      |
| Pesos iniciales  | yolov8s.pt   |
| Épocas           | 50           |
| Tamaño de imagen | 640          |
| Batch size       | 16           |
| Optimizer        | auto         |
| close_mosaic     | 10           |
| patience         | 15           |
| GPU              | Tesla T4     |
| Plataforma       | Google Colab |

Comando de entrenamiento usado:

```python
!yolo detect train \
    model=yolov8s.pt \
    data={data_yaml_path} \
    epochs=50 \
    imgsz=640 \
    batch=16 \
    close_mosaic=10 \
    patience=15 \
    project={RUNS_DIR} \
    name=yolov8s_ppe_final
```

## 12. Métricas del modelo final

El modelo final fue evaluado sobre el conjunto de prueba.

| Métrica      | Valor |
| ------------ | ----: |
| Precision    | 0.759 |
| Recall       | 0.676 |
| mAP@0.5      | 0.726 |
| mAP@0.5:0.95 | 0.472 |

Métricas por clase:

| Clase     | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |
| --------- | --------: | -----: | ------: | -----------: |
| person    |     0.405 |  0.617 |   0.631 |        0.470 |
| helmet    |     0.921 |  0.833 |   0.925 |        0.631 |
| no_helmet |     0.930 |  0.889 |   0.944 |        0.495 |
| vest      |     0.845 |  0.929 |   0.948 |        0.745 |
| no_vest   |     0.616 |  0.647 |   0.624 |        0.324 |
| gloves    |     0.831 |  0.096 |   0.270 |        0.139 |
| goggles   |     0.640 |  0.421 |   0.484 |        0.221 |
| boots     |     0.883 |  0.981 |   0.981 |        0.754 |

## 13. Detector auxiliar de personas

Durante las pruebas se observó que la clase `person` del modelo PPE final no siempre era detectada de forma estable. Esto se debe a que varios datasets estaban más orientados a cascos, cabezas o EPP que a cuerpos completos.

Por ello, se utilizó un modelo YOLOv8 preentrenado en COCO como detector auxiliar de personas.

Arquitectura final:

1. YOLOv8 COCO detecta personas.
2. YOLOv8 PPE detecta EPP.
3. El verificador asocia EPP con personas.
4. Se calcula cumplimiento de casco y cumplimiento completo.

## 14. Verificador de cumplimiento

El sistema incluye tres versiones del verificador:

### V1: Regla estricta

Una persona cumple si se detecta casco y chaleco asociados.

### V2: Asociación espacial flexible

Se amplía el bounding box de cada persona y se asocian EPP mediante centro de caja e IoU.

### V3: Verificador final

Se separan dos indicadores:

* Tasa de cumplimiento de casco.
* Tasa de cumplimiento completo.

Esta versión fue seleccionada porque el sistema mostró mayor robustez en detección de casco que en verificación completa.

## 15. Resultados en imágenes externas

Se probaron imágenes reales de obra no utilizadas durante el entrenamiento.

| Imagen      | Personas detectadas | Cumplen casco | Cumplen completo | Revisión | Tasa casco | Tasa completo |
| ----------- | ------------------: | ------------: | ---------------: | -------: | ---------: | ------------: |
| obra_09.jpg |                   9 |             9 |                5 |        4 |     1.0000 |        0.5556 |
| obra_08.jpg |                   3 |             3 |                0 |        3 |     1.0000 |        0.0000 |
| obra_07.jpg |                  14 |            13 |                0 |       14 |     0.9286 |        0.0000 |
| obra_06.jpg |                   3 |             3 |                2 |        1 |     1.0000 |        0.6667 |
| obra_05.jpg |                   5 |             5 |                0 |        5 |     1.0000 |        0.0000 |
| obra_04.jpg |                   3 |             3 |                0 |        3 |     1.0000 |        0.0000 |
| obra_02.jpg |                   6 |             6 |                1 |        5 |     1.0000 |        0.1667 |
| obra_01.jpg |                   7 |             5 |                3 |        4 |     0.7143 |        0.4286 |
| obra_03.jpg |                   6 |             3 |                1 |        5 |     0.5000 |        0.1667 |

## 16. Análisis de oclusión

Las imágenes externas fueron clasificadas manualmente en tres niveles de oclusión.

| Nivel de oclusión | Imágenes | Personas detectadas | Tasa casco promedio | Tasa completo promedio |
| ----------------- | -------: | ------------------: | ------------------: | ---------------------: |
| Baja              |        1 |                   9 |              1.0000 |                 0.5556 |
| Media             |        7 |                  41 |              0.9490 |                 0.1803 |
| Alta              |        1 |                   6 |              0.5000 |                 0.1667 |

Conclusión:

* La detección de casco fue más robusta.
* El cumplimiento completo fue más sensible a oclusión.
* La detección de chaleco fue el principal factor limitante.
* El estado `revision` es necesario cuando la evidencia visual no es suficiente.

## 17. Instalación

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 18. Uso básico del modelo

Ejemplo de inferencia simple:

```python
from ultralytics import YOLO

model = YOLO("weights/best.pt")

results = model.predict(
    source="data/demo_images/obra_01.jpg",
    imgsz=640,
    conf=0.25,
    save=True
)
```

## 19. Reproducibilidad

Para reproducir la demostración final:

1. Clonar este repositorio.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Descargar el peso entrenado `best.pt`, si no está incluido.
4. Colocar `best.pt` en la carpeta `weights/`.
5. Colocar imágenes de prueba en `data/demo_images/`.
6. Ejecutar:

```bash
python run_pipeline.py --mode demo
```

7. Revisar resultados en `results/demo_outputs/`.

## 20. Limitaciones

El proyecto presenta las siguientes limitaciones:

* Dataset combinado con desbalance entre clases.
* Diferencias entre fuentes de datos.
* Bajo rendimiento en objetos pequeños como guantes y gafas.
* Dificultad para detectar chalecos parcialmente ocultos.
* Dependencia de reglas espaciales para asociar EPP con personas.
* Evaluación realizada sobre imágenes, no sobre video en tiempo real.
* Necesidad de mayor validación con imágenes locales de obra.

## 21. Trabajo futuro

Como trabajo futuro se propone:

* Incorporar más imágenes reales de obras locales.
* Agregar detección de arnés de seguridad.
* Mejorar detección de chalecos.
* Balancear clases minoritarias.
* Comparar YOLOv8s con YOLOv8m, YOLOv8l, SSD y Faster R-CNN.
* Implementar evaluación en video.
* Integrar pose estimation para asociar casco con cabeza y chaleco con torso.
* Desarrollar una aplicación web o dashboard de monitoreo.

## 22. Consideraciones éticas

Este sistema debe utilizarse como herramienta de apoyo preventivo para la supervisión de seguridad. No debe utilizarse como mecanismo automático de sanción.

Los casos clasificados como `revision` deben ser evaluados por un supervisor humano.

En una implementación real se recomienda:

* Informar a los trabajadores sobre el uso del sistema.
* Proteger la privacidad de las personas.
* Difuminar rostros si es necesario.
* Evitar decisiones automáticas sin revisión humana.
* Auditar falsos positivos y falsos negativos.
* Usar el sistema como apoyo a la mejora de seguridad, no como herramienta punitiva.

## 23. Autores

* Kelvin Alexander Aquino Ynga
* Junior Alexander Ponte Paz
* Carlos Enrique Villanueva Portal

Facultad de Ingeniería Industrial y de Sistemas
Universidad Nacional de Ingeniería
Lima, Perú

## 24. Licencia

Este proyecto fue desarrollado con fines académicos. El uso de datasets externos debe respetar las licencias originales de cada fuente.
