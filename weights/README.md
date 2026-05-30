# Pesos del modelo

Esta carpeta debe contener el modelo final entrenado:

```text
weights/best.pt
```

Debido al tamaño del archivo, el peso entrenado puede almacenarse externamente en Google Drive.

## Instrucciones

Descargar `best.pt` desde el enlace proporcionado.

Colocarlo en esta carpeta:

```text
weights/best.pt
```

Ejecutar:

```bash
python run_pipeline.py --mode demo
```

## Pesos utilizados

- `yolov8s.pt`: modelo YOLOv8s preentrenado usado para detectar personas.
- `best.pt`: modelo YOLOv8s entrenado para detección de EPP.
