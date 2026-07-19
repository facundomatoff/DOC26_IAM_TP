import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import yaml
import shutil

class YOLOAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Annotator Pro - Estructura Permanente")
        self.root.geometry("1100x950")
        self.root.resizable(False, False)

        # Configuración de rutas
        self.base_dir = "dataset"
        self.img_dir = os.path.join(self.base_dir, "images")
        self.lbl_dir = os.path.join(self.base_dir, "labels")
        self.trash_dir = "trash"
        self.yaml_path = "data.yaml"
        self.log_file = "processed.log"
        
        if not os.path.exists(self.trash_dir): os.makedirs(self.trash_dir)
        
        # Inicialización de estado
        self.index = 0
        self.classes = self.load_classes()
        self.colors = ["red", "blue", "green", "yellow", "cyan", "magenta", "orange"]
        
        # --- ORDEN CRÍTICO: UI primero ---
        self.setup_ui()
        
        # --- Lógica de datos después ---
        self.refresh_file_list()
        self.load_data()

    def setup_ui(self):
        """Crea todos los componentes de la interfaz de forma fija."""
        # Barra superior
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=1000, mode='determinate')
        self.progress_bar.pack(pady=10)
        self.status_label = tk.Label(self.root, text="Inicializando...", font=("Arial", 10, "bold"))
        self.status_label.pack()

        # Frame contenedor de Imagen y Texto
        self.top_frame = tk.Frame(self.root, width=1050, height=550)
        self.top_frame.pack(pady=10, expand=True)
        
        self.img_label = tk.Label(self.top_frame, width=500, height=500, bg="gray", text="Sin imagen cargada")
        self.img_label.pack(side=tk.LEFT, padx=20)

        self.text_area = tk.Text(self.top_frame, height=25, width=40)
        self.text_area.pack(side=tk.RIGHT, padx=20)

        self.filename_label = tk.Label(self.root, text="Archivo actual: Ninguno", font=("Courier", 10, "italic"), fg="blue")
        self.filename_label.pack(pady=5)

        # Frame de botones (SIEMPRE VISIBLE)
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.X, pady=20, side=tk.BOTTOM)
        
        # Botones de clases
        for idx, name in self.classes.items():
            btn = tk.Button(self.bottom_frame, text=f"{name} ({idx})", command=lambda i=idx: self.auto_save_and_next(i))
            btn.pack(side=tk.LEFT, padx=5)

        # Botones de control (SIEMPRE VISIBLES)
        tk.Button(self.bottom_frame, text="Mover a Trash", command=self.move_to_trash, bg="orange").pack(side=tk.LEFT, padx=5)
        tk.Button(self.bottom_frame, text="Guardar y seguir", command=self.save_and_next, bg="green", fg="white").pack(side=tk.RIGHT, padx=5)
        tk.Button(self.bottom_frame, text="REINICIAR", command=self.reset_process, bg="red", fg="white").pack(side=tk.RIGHT, padx=5)

    def refresh_file_list(self):
        self.processed_files = self.load_log()
        all_files = sorted([f for f in os.listdir(self.img_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])
        self.total_files = len(all_files)
        self.pending_files = [f for f in all_files if f not in self.processed_files]
        self.index = 0

    def load_data(self):
        """Carga datos o muestra estado en la UI existente."""
        if self.index < len(self.pending_files):
            img_name = self.pending_files[self.index]
            # ... (Lógica de dibujo y carga de texto que ya funciona)
            self.draw_and_show(img_name)
        else:
            # AVISO: En lugar de ocultar todo, solo actualizamos los labels
            self.img_label.config(image='', text="¡Dataset completo!")
            self.status_label.config(text="Progreso: 100%")
            self.filename_label.config(text="No hay imágenes pendientes.")

    def draw_yolo_boxes(self, img, txt_path):
        draw = ImageDraw.Draw(img)
        w, h = img.size
        if os.path.exists(txt_path):
            with open(txt_path, "r") as f:
                for i, line in enumerate(f.readlines()):
                    parts = list(map(float, line.split()))
                    if len(parts) < 5: continue
                    x1 = (parts[1] - parts[3]/2) * w
                    y1 = (parts[2] - parts[4]/2) * h
                    x2 = (parts[1] + parts[3]/2) * w
                    y2 = (parts[2] + parts[4]/2) * h
                    draw.rectangle([x1, y1, x2, y2], outline=self.colors[i % len(self.colors)], width=8)
        return img

    def move_to_trash(self):
        if self.index < len(self.pending_files):
            img_name = self.pending_files[self.index]
            txt_name = os.path.splitext(img_name)[0] + ".txt"
            shutil.move(os.path.join(self.img_dir, img_name), os.path.join(self.trash_dir, img_name))
            if os.path.exists(os.path.join(self.lbl_dir, txt_name)):
                shutil.move(os.path.join(self.lbl_dir, txt_name), os.path.join(self.trash_dir, txt_name))
            self.pending_files.pop(self.index)
            self.load_data()

    def update_progress(self):
        processed = self.total_files - len(self.pending_files)
        pct = (processed / self.total_files * 100) if self.total_files > 0 else 100
        self.progress_bar['value'] = pct
        self.status_label.config(text=f"Procesadas: {processed} / {self.total_files}")

    def save_and_next(self):
        img_name = self.pending_files[self.index]
        txt_path = os.path.join(self.lbl_dir, os.path.splitext(img_name)[0] + ".txt")
        with open(txt_path, "w") as f: f.write(self.text_area.get(1.0, tk.END).strip())
        with open(self.log_file, "a") as f: f.write(img_name + "\n")
        self.pending_files.pop(self.index)
        self.load_data()

    def auto_save_and_next(self, idx):
        lines = self.text_area.get(1.0, tk.END).strip().split('\n')
        new_lines = [" ".join([str(idx)] + line.split()[1:]) for line in lines if line.strip()]
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "\n".join(new_lines))
        self.save_and_next()

    def reset_process(self):
        if messagebox.askyesno("Reiniciar", "¿Limpiar log de proceso?"):
            if os.path.exists(self.log_file): os.remove(self.log_file)
            self.refresh_file_list()
            self.load_data()

    def load_classes(self):
        with open(self.yaml_path, 'r') as f: return yaml.safe_load(f).get('names', {})
    def load_log(self):
        return set(line.strip() for line in open(self.log_file, "r")) if os.path.exists(self.log_file) else set()

if __name__ == "__main__":
    root = tk.Tk()
    app = YOLOAnnotator(root)
    root.mainloop()