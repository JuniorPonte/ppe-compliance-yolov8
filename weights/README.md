# Weights

Esta carpeta debe contener el modelo final entrenado:

```text
weights/best.pt
```

Debido al tamaño del archivo, el peso entrenado puede almacenarse externamente en Google Drive.

## Instrucciones

Descargar `best.pt` desde el enlace proporcionado por el equipo.

Colocarlo en esta carpeta:

```text
weights/best.pt
```

Ejecutar:

```bash
python run_pipeline.py --mode demo
```

## Modelos utilizados

- `yolov8s.pt`: modelo YOLOv8s preentrenado usado como detector auxiliar de personas.
- `best.pt`: modelo YOLOv8s entrenado para detección de EPP.

## Enlace de descarga

El archivo `best.pt` puede descargarse desde:

[Descargar best.pt](PEGA_AQUI_TU_LINK_DE_GOOGLE_DRIVE)
