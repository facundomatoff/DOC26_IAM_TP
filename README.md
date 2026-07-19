# 🧊 Detección de Bebidas en Heladeras Exhibidoras — YOLOv8n

Doctorado 2026 - Introducción al Aprendizaje de Máquinas - Trabajo Final

> Sistema de visión por computadora para auditoría automática de productos en heladeras comerciales mediante detección de objetos en tiempo real.

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Clases Detectadas](#clases-detectadas)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Requisitos](#requisitos)
- [Uso Rápido](#uso-rápido)
- [Resultados](#resultados)
- [Informe Técnico](#informe-técnico)
- [Referencias](#referencias)

---

## Descripción del Proyecto

Un cliente propietario de heladeras exhibidoras comerciales requería verificar automáticamente que los productos almacenados correspondieran a su propio catálogo, descartando la presencia de productos de la competencia. Se instalaron cámaras inteligentes en las heladeras que capturan un video corto cada vez que se abre la puerta. Esos videos son procesados frame a frame para detectar qué bebidas son extraídas.

El sistema fue desarrollado sobre **YOLOv8 Nano** (`yolov8n`), reentrenado con un dataset propio construido desde cero mediante videos de prueba en condiciones controladas. El modelo resultante es lo suficientemente liviano para ejecutarse directamente en el hardware embebido de las cámaras inteligentes.

---

## Clases Detectadas

| ID | Clase | Descripción |
|---|---|---|
| 0 | `pepsi_bottle` | Botella con líquido oscuro (incluye Coca-Cola, visualmente indistinguible) |
| 1 | `water_bottle` | Botella de agua mineral |
| 2 | `generic_bottle` | Otras botellas sin marca identificable |
| 3 | `aluminum_can` | Latas de aluminio |
| 4 | `unknown` | Objetos ambiguos: reflejos, fondo, objetos del usuario |

---

## Estructura del Repositorio

```
DOC26_IAM_TP/
├── dataset/
│   ├── images/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── labels/
│       ├── train/
│       ├── val/
│       └── test/
├── runs/
│   └── detect/
│       ├── train/          ← Pesos y métricas del entrenamiento
│       └── val/            ← Resultados de validación
├── data.yaml               ← Configuración de clases y rutas
├── DOC26_IAM_TP.ipynb      ← Notebook principal (entrenamiento + informe)
├── DOC26_IAM_TP.ipynb      ← Notebook principal (entrenamiento + informe)
└── README.md
```

---

## Requisitos

```
Python >= 3.12
torch >= 2.11.0 (con soporte CUDA para GPU)
ultralytics >= 8.4.95
```

Instalación rápida:

```bash
pip install ultralytics
```

---

## Uso Rápido

### Entrenamiento

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # Pesos preentrenados en COCO

model.train(
    data='data.yaml',
    epochs=50,
    imgsz=320
)
```

### Validación y Testing con nuevo Pesos

```python
model = YOLO('runs/detect/train/weights/best.pt')
metrics = model.val(data='data.yaml')
```

### Inferencia sobre una imagen

```python
results = model.predict(source='ruta/a/imagen.jpg', conf=0.25)
results[0].show()
```

---

## Resultados

### Métricas de Validación (conjunto de test — 303 imágenes)

| Clase | Precisión | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| **Global** | **0.843** | **0.840** | **0.908** | **0.780** |
| `pepsi_bottle` | 0.905 | 0.908 | 0.933 | 0.804 |
| `water_bottle` | 0.899 | 0.912 | 0.928 | 0.777 |
| `generic_bottle` | 0.811 | 0.716 | 0.886 | 0.786 |
| `aluminum_can` | 0.767 | 0.833 | 0.915 | 0.804 |
| `unknown` | 0.833 | 0.831 | 0.878 | 0.728 |

**Velocidad de inferencia:** ~3.4 ms/imagen en GPU Tesla T4 (~294 FPS)

### Curvas de Entrenamiento

Las pérdidas de entrenamiento y validación convergen de forma paralela durante las 50 épocas, sin señales de sobreajuste.

![Curvas de entrenamiento](runs/detect/train/results.png)

### Matriz de Confusión

![Matriz de Confusión Normalizada](runs/detect/val/confusion_matrix_normalized.png)

---

## Informe Técnico

El informe técnico completo se encuentra dentro del notebook principal `DOC26_IAM_TP.ipynb`, e incluye:

1. **Introducción** — Descripción del problema y desafíos del escenario
2. **Algoritmo** — Arquitectura YOLOv8n, hiperparámetros, justificación de la selección
3. **Solución implementada** — Pipeline completo y decisiones técnicas tomadas
4. **Resultados** — Análisis de curvas de entrenamiento, métricas de validación y matriz de confusión
5. **Conclusiones** — Evaluación del rendimiento y recomendaciones
6. **Referencias** — Papers que validan el uso de YOLO para este tipo de escenario

---

## Referencias

1. Redmon, J. et al. (2016). *You only look once: Unified, real-time object detection.* CVPR. https://doi.org/10.1109/CVPR.2016.91
2. Jocher, G., Chaurasia, A., & Qiu, J. (2023). *Ultralytics YOLO* (v8.0.0). https://github.com/ultralytics/ultralytics
3. Lin, T. Y. et al. (2014). *Microsoft COCO: Common objects in context.* ECCV. https://doi.org/10.1007/978-3-319-10602-1_48
4. Terven, J. et al. (2023). *A Comprehensive Review of YOLO Architectures.* Machine Learning and Knowledge Extraction, 5(4). https://doi.org/10.3390/make5040083
5. Li, X. et al. (2020). *Generalized Focal Loss.* NeurIPS. https://arxiv.org/abs/2006.04388
6. Hussain, M. (2023). *YOLO-v1 to YOLO-v8, the Rise of YOLO.* Machines, 11(7). https://doi.org/10.3390/machines11070677
7. Jiang, P. et al. (2022). *A Review of YOLO Algorithm Developments.* Procedia Computer Science, 199. https://doi.org/10.1016/j.procs.2022.01.135

---

*Proyecto desarrollado en Google Colab · GPU Tesla T4 · Ultralytics 8.4.95 · PyTorch 2.11.0*
