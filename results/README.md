# Results

Esta carpeta almacena los resultados generados por el pipeline.

Al ejecutar:

```bash
python run_pipeline.py --mode demo
```

se generan:

```text
results/demo_outputs/
    resultado_obra_01.jpg
    resultado_obra_02.jpg
    ...
    resumen_cumplimiento.csv
```

El archivo `resumen_cumplimiento.csv` contiene:

- imagen
- personas detectadas
- personas que cumplen casco
- personas que cumplen cumplimiento completo
- casos no cumple
- casos en revisión
- tasa de casco
- tasa de cumplimiento completo
