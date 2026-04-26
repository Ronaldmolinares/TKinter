import tkinter as tk
from tkinter import messagebox

import joblib  # type: ignore


class IrisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App Clasificadora Iris")
        self.root.geometry("450x600")

        # Cargar el modelo
        try:
            self.modelo = joblib.load("modelo.pkl")
        except:
            messagebox.showerror("Error", "No se encontró el archivo modelo.pkl")

        # --- Interfaz (Boceto 1) ---
        tk.Label(
            root, text="Clasificador de Especies Iris", font=("Arial", 16, "bold")
        ).pack(pady=20)

        self.frame_inputs = tk.Frame(root)
        self.frame_inputs.pack(pady=10)

        # Campos de entrada
        labels = [
            "Largo Sépalo (cm):",
            "Ancho Sépalo (cm):",
            "Largo Pétalo (cm):",
            "Ancho Pétalo (cm):",
        ]
        self.entries = []
        for i, text in enumerate(labels):
            tk.Label(self.frame_inputs, text=text).grid(
                row=i, column=0, sticky="e", padx=5, pady=5
            )
            entry = tk.Entry(self.frame_inputs)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(entry)

        self.btn_predecir = tk.Button(
            root,
            text="Predecir Especie",
            command=self.predecir,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.btn_predecir.pack(pady=20)

        # --- Area de Resultados (Boceto 2) ---
        self.lbl_resultado = tk.Label(
            root, text="", font=("Arial", 14, "bold"), fg="blue"
        )
        self.lbl_resultado.pack(pady=10)

        self.btn_limpiar = tk.Button(
            root, text="Limpiar Formulario", command=self.limpiar
        )
        self.btn_limpiar.pack(pady=5)

        self.status = tk.Label(
            root, text="Estado: Modelo cargado", bd=1, relief="sunken", anchor="w"
        )
        self.status.pack(side="bottom", fill="x")

    def predecir(self):
        try:
            # Obtener datos
            datos = [float(e.get()) for e in self.entries]

            # Predicción (El modelo espera una lista de listas)
            prediccion = self.modelo.predict([datos])[0]

            # Mapeo de nombres (Ajustar según tu entrenamiento)
            nombres = {0: "Iris-setosa", 1: "Iris-versicolor", 2: "Iris-virginica"}
            resultado = nombres.get(prediccion, "Desconocido")

            self.lbl_resultado.config(text=f"Especie Predicha: {resultado}")
            self.status.config(text="Estado: Predicción realizada con éxito")

        except ValueError:
            messagebox.showwarning(
                "Error de datos", "Por favor ingresa solo valores numéricos."
            )

    def limpiar(self):
        for e in self.entries:
            e.delete(0, tk.END)
        self.lbl_resultado.config(text="")
        self.status.config(text="Estado: Formulario limpio")


if __name__ == "__main__":
    root = tk.Tk()
    app = IrisApp(root)
    root.mainloop()
