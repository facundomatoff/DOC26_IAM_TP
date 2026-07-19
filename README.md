# Detección de Bebidas en Heladeras Exhibidoras — YOLOv8n

> Trabajo Final — Introducción al Aprendizaje de Máquinas · Doctorado en Informática 2026

Este repositorio contiene el trabajo final de la materia **Introducción al Aprendizaje de Máquinas**, correspondiente al **Doctorado en Informática 2026**. El trabajo consiste en el desarrollo de un sistema de visión por computadora para la auditoría automática de productos en heladeras comerciales, implementado mediante detección de objetos en tiempo real con YOLOv8n.

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Clases Detectadas](#clases-detectadas)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Requisitos](#requisitos)
- [Informe Técnico](#informe-técnico)

---

## Descripción del Proyecto

El proyecto consiste en el **reentrenamiento del modelo YOLOv8n** para la detección específica de bebidas en heladeras exhibidoras comerciales. El escenario de aplicación involucra cámaras inteligentes instaladas en heladeras que capturan videos cada vez que se abre la puerta, con el objetivo de verificar que los productos almacenados correspondan al catálogo autorizado del cliente y no a productos de la competencia.

El trabajo abarcó dos etapas principales. La primera consistió en el **desarrollo de un conjunto de scripts Python para ejecución local**, destinados a la construcción del dataset: extracción de frames desde videos, pre-filtrado automático con YOLOv8 preentrenado, organización del dataset y una aplicación de escritorio para el re-etiquetado manual asistido de imágenes. La segunda etapa se llevó a cabo en un **notebook de Google Colab**, que contiene tanto el código necesario para el reentrenamiento y la validación del modelo, como el informe técnico completo del proyecto, incluyendo la descripción del escenario, el pipeline de generación del dataset, los problemas encontrados, los desafíos afrontados y sus soluciones, los resultados obtenidos y las conclusiones finales.

[<img width="117" height="20" alt="image" src="https://github.com/user-attachments/assets/36fbc2ee-110c-447d-8063-1a18627c52e1" />](https://colab.research.google.com/github/facundomatoff/DOC26_IAM_TP/blob/main/Doc26_IAM_Trabajo_Final.ipynb)

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
│
├── dataset/
│   ├── images/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── labels/
│       ├── train/
│       ├── val/
│       └── test/
│
├── dataset_split/
│   ├── test.txt                ← Distribución de imágenes y etiquetas para las pruebas
│   ├── train.txt               ← Distribución de imágenes y etiquetas para el entrenamiento
│   └── val.txt                 ← Distribución de imágenes y etiquetas para la validación
│
├── data.yaml                   ← Configuración de clases y rutas
│
├── DOC26_IAM_TP.ipynb          ← Notebook principal (informe + entrenamiento)
│
├── scripts/                    ← Scripts Python para ejecución local
│   ├── extract_frames.py       ← Extracción de frames desde videos/GIFs
│   ├── identity_bottles.py     ← Pre-filtrado con YOLOv8 preentrenado
│   ├── isolate_empty_labels.py ← Limpieza de etiquetas vacías
│   ├── train_dataset_generator.py ← Organización del dataset para YOLO
│   ├── analyze_dataset.py      ← Reporte de distribución del dataset
│   ├── generate_split_lists.py ← Generación de listas train/val/test
│   └── desktop.py              ← App de re-etiquetado manual asistido
│
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

## Informe Técnico

El informe técnico completo, los resultados del entrenamiento, las métricas de validación y las conclusiones del proyecto se encuentran documentados íntegramente dentro del notebook principal **`DOC26_IAM_TP.ipynb`**. Allí se detallan:

1. **Introducción** — Descripción del problema y desafíos del escenario
2. **Algoritmo** — Arquitectura YOLOv8n, hiperparámetros y justificación de la selección del modelo
3. **Pipeline de construcción del dataset** — Scripts utilizados en cada etapa, decisiones tomadas y problemas encontrados
4. **Reentrenamiento y validación** — Código de entrenamiento, curvas de aprendizaje y análisis de resultados
5. **Conclusiones** — Evaluación del rendimiento, limitaciones y recomendaciones
6. **Referencias** — Papers que validan el uso de YOLO para este tipo de escenario

[<img width="117" height="20" alt="image" src="https://github.com/user-attachments/assets/36fbc2ee-110c-447d-8063-1a18627c52e1" />](https://colab.research.google.com/github/facundomatoff/DOC26_IAM_TP/blob/main/Doc26_IAM_Trabajo_Final.ipynb)

---

*Trabajo Final — Introducción al Aprendizaje de Máquinas · Doctorado en Informática 2026*  
*Desarrollado en Google Colab · GPU Tesla T4 · Ultralytics 8.4.95 · PyTorch 2.11.0*
