# PPE Compliance YOLOv8

Proyecto para deteccion de cumplimiento de equipos de proteccion personal (PPE) en imagenes de obra usando YOLOv8.

## Ejecución de extremo a extremo

El código puede ejecutarse de extremo a extremo con un único comando documentado.

Primero instalar dependencias:

```bash
pip install -r requirements.txt
```

Luego ejecutar el pipeline completo de demostración:

```bash
python run_pipeline.py --mode demo
```

Este comando realiza automáticamente:

- Carga del detector auxiliar de personas YOLOv8 preentrenado en COCO.
- Carga del modelo YOLOv8s entrenado para EPP.
- Lectura de imágenes desde `data/demo_images/`.
- Detección de personas.
- Detección de EPP.
- Asociación espacial entre personas y EPP.
- Cálculo de cumplimiento de casco.
- Cálculo de cumplimiento completo.
- Generación de imágenes anotadas.
- Generación del archivo `resumen_cumplimiento.csv`.

Los resultados se guardan en:

```text
results/demo_outputs/
```

## Comando alternativo

También se puede especificar una carpeta de imágenes personalizada:

```bash
python run_pipeline.py --mode demo --input data/demo_images --output results/demo_outputs --weights weights/best.pt
```

## Estructura

```text
ppe-compliance-yolov8/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- run_pipeline.py
|-- notebooks/
|-- data/
|   `-- demo_images/
|-- weights/
`-- results/
    |-- demo_outputs/
    `-- metrics/
```

## Instalacion

Se recomienda crear un entorno virtual antes de instalar dependencias.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

En Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

Coloca el modelo entrenado en `weights/best.pt` y las imagenes de prueba en `data/demo_images/`.

Comandos principales del proyecto:

```bash
pip install -r requirements.txt
python run_pipeline.py --mode demo
```

El comando de ejecucion realiza el flujo completo:

1. Carga YOLOv8 preentrenado para detectar personas.
2. Carga el modelo PPE entrenado desde `weights/best.pt`.
3. Lee imagenes desde `data/demo_images/`.
4. Detecta personas.
5. Detecta EPP.
6. Asocia EPP con personas.
7. Calcula cumplimiento.
8. Guarda imagenes anotadas en `results/demo_outputs/`.
9. Guarda el resumen CSV en `results/demo_outputs/resumen_cumplimiento.csv`.

Tambien puedes indicar rutas personalizadas:

```bash
python run_pipeline.py --mode demo --weights weights/best.pt --input data/demo_images --output results/demo_outputs
```

## Notebooks

Los notebooks del proyecto deben colocarse en `notebooks/`:

- `01_modelo_base_casco.ipynb`
- `02_dataset_combinado_ppe_shwd.ipynb`
- `03_modelo_final_yolo_ppe.ipynb`

## Datos y pesos

Los datasets completos y pesos pesados no deben subirse directamente al repositorio si exceden el limite recomendado por GitHub. En ese caso, colocar enlaces de descarga en:

- `data/README.md`
- `weights/README.md`

## Resultados

Los resultados exportados, metricas y predicciones de demostracion se almacenan en `results/`.

## Verificación final antes de subir

Antes de subir, prueba localmente o en Colab:

```bash
pip install -r requirements.txt
python run_pipeline.py --mode demo
```

Debe generarte:

```text
results/demo_outputs/resumen_cumplimiento.csv
```

y varias imágenes:

```text
resultado_obra_01.jpg
resultado_obra_02.jpg
...
```
