# Data

Esta carpeta contiene imágenes de demostración para ejecutar el pipeline final.

## Imágenes de demostración

Las imágenes para probar el pipeline deben ubicarse en:

```text
data/demo_images/
```

Para ejecutar la demo:

```bash
python run_pipeline.py --mode demo
```

## Dataset completo

El dataset combinado completo no se incluye en este repositorio debido a su tamaño.

El dataset final fue construido a partir de:

- [Dataset safety helmet detection Computer Vision Model](https://universe.roboflow.com/marina-wgvsb/safety-helmet-detection-apiwd/dataset/1)
- [PPE detection Computer Vision Model](https://universe.roboflow.com/testcasque/ppe-detection-qlq3d)
- [Worker detection Computer Vision Model](https://universe.roboflow.com/inzynierka-fcqsu/worker-detection-wh7fp/browse?queryText=class%3Aworker&pageSize=50&startingIndex=0&browseQuery=true)
- [SafetyHelmetWearing Dataset, SHWD](https://github.com/njvisionpower/Safety-Helmet-Wearing-Dataset)

Estructura esperada del dataset completo:

```text
ppe_combined_dataset/
    train/
        images/
        labels/
    valid/
        images/
        labels/
    test/
        images/
        labels/
    data.yaml
```
