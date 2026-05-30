# Weights

Esta carpeta debe contener los pesos necesarios para ejecutar la demo.

## Archivos requeridos

```text
weights/best.pt
```

Este archivo corresponde al mejor modelo YOLOv8s entrenado para detectar EPP.

Debido al tamaño del archivo, el peso entrenado puede almacenarse externamente en Google Drive.

## Archivo opcional

```text
weights/yolov8s.pt
```

Este archivo corresponde al modelo YOLOv8s preentrenado en COCO, usado como detector auxiliar de personas.

Si no se incluye, Ultralytics lo descargará automáticamente al ejecutar el pipeline, porque el script usa:

```python
person_model = YOLO("yolov8s.pt")
```

## Instrucciones

1. Descargar `best.pt` desde el enlace proporcionado por el equipo.
2. Colocarlo en esta carpeta:

```text
weights/best.pt
```

3. Ejecutar:

```bash
python run_pipeline.py --mode demo
```

## Modelos utilizados

- `yolov8s.pt`: modelo YOLOv8s preentrenado usado como detector auxiliar de personas.
- `best.pt`: modelo YOLOv8s entrenado para detección de EPP.

## Enlace de descarga

El archivo `best.pt` puede descargarse desde:

[Descargar best.pt](https://drive.google.com/file/d/1WFgaC-6aEQhsuGMsYLinGGm-Kr9DfbS8/view?usp=sharing)
