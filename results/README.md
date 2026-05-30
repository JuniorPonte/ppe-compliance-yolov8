# Results

Esta carpeta almacena los resultados generados por el pipeline.

Al ejecutar:

```bash
python run_pipeline.py --mode demo
```

se genera la carpeta:

```text
results/demo_outputs/
```

Dentro de esa carpeta se guardan:

```text
resultado_obra_01.jpg
resultado_obra_02.jpg
...
resumen_cumplimiento.csv
```

El archivo `resumen_cumplimiento.csv` contiene:

- imagen
- personas_detectadas
- cumplen_casco
- cumplen_completo
- no_cumplen
- revision
- tasa_casco
- tasa_cumplimiento_completo
- output
