#
# Este script genera tres archivos .txt que contienen las rutas completas de las imágenes, mezcladas aleatoriamente.
#
# Ventajas de usar archivos .txt de listas (como train.txt, val.txt, test.txt):
# * No destructivo: No necesitas mover o copiar físicamente los archivos (evitas duplicar datos en disco).
# * Flexibilidad: Puedes cambiar la configuración de entrenamiento (ej: probar con más imágenes de validación) simplemente editando la lista, 
# sin tocar los archivos originales.
# * Aleatoriedad: La mezcla se hace en la generación de estas listas, lo cual es mucho más limpio.
#

import os
import random

def generate_split_lists(img_dir, output_dir="dataset_split"):
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    images = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    random.seed(42) # Semilla fija para reproducibilidad
    random.shuffle(images)
    
    n = len(images)
    train_end = int(n * 0.7)
    val_end = train_end + int(n * 0.2)
    
    # Listas
    splits = {
        "train.txt": images[:train_end],
        "val.txt": images[train_end:val_end],
        "test.txt": images[val_end:]
    }
    
    for filename, file_list in splits.items():
        with open(os.path.join(output_dir, filename), "w") as f:
            for img_name in file_list:
                # Escribimos las rutas relativas al repositorio, no las absolutas de tu PC.
                f.write("dataset/images/" + img_name + "\n")
    
    print(f"Listas generadas en {output_dir}: {len(splits['train.txt'])} train, {len(splits['val.txt'])} val, {len(splits['test.txt'])} test.")

if __name__ == "__main__":
    generate_split_lists("dataset/images")