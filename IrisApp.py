import tkinter as tk
from tkinter import messagebox
import os

import joblib  # type: ignore


class IrisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App Clasificadora Iris")
        self.root.geometry("450x600")

        # Cargar el modelo
        try:
            modelo_path = os.path.join(os.path.dirname(__file__), "modelo.pkl")
            self.modelo = joblib.load(modelo_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se encontró el archivo modelo.pkl\n{str(e)}")

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
        # Crear un command de validación
        vcmd = (root.register(self.validar_entrada), "%P")
        
        for i, text in enumerate(labels):
            tk.Label(self.frame_inputs, text=text).grid(
                row=i, column=0, sticky="e", padx=5, pady=5
            )
            entry = tk.Entry(
                self.frame_inputs,
                validate="key",
                validatecommand=vcmd,
                bg="white"
            )
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(entry)

        # --- Reglas de Validación ---
        self.frame_reglas = tk.Frame(root, bg="#f0f0f0", relief="solid", bd=1)
        self.frame_reglas.pack(pady=10, padx=10, fill="x")

        tk.Label(
            self.frame_reglas,
            text="Reglas de validación:",
            font=("Arial", 9, "bold"),
            bg="#f0f0f0"
        ).pack(anchor="w", padx=5, pady=(5, 2))

        reglas_texto = (
            "• Valores entre 0.1 y 10 cm\n"
            "• No se permiten letras ni caracteres especiales\n"
            "• Mínimo 0.1 cm, no se permite 0"
        )

        tk.Label(
            self.frame_reglas,
            text=reglas_texto,
            font=("Arial", 8),
            bg="#f0f0f0",
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 5))

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

    def validar_entrada(self, valor):
        """
        Valida la entrada en tiempo real:
        - Solo permite números y un punto decimal
        - No permite valores mayores a 10
        - No permite letras ni caracteres especiales
        """
        # Si el campo está vacío, es válido
        if valor == "":
            return True
        
        # Solo permitir números y un punto decimal
        if not all(c.isdigit() or c == "." for c in valor):
            return False
        
        # Validar que solo haya un punto decimal
        if valor.count(".") > 1:
            return False
        
        # Intentar convertir a float para validar máximo
        try:
            numero = float(valor)
            # Validar que no exceda 10
            if numero > 10:
                return False
        except ValueError:
            # Permite valores incompletos como "0." para escribir "0.1"
            return True
        
        return True

    def predecir(self):
        try:
            # Validar que ningún campo esté vacío
            datos = []
            for i, e in enumerate(self.entries):
                valor = e.get()
                if valor == "":
                    messagebox.showwarning(
                        "Campos incompletos", 
                        "Por favor completa todos los campos."
                    )
                    return
                numero = float(valor)
                # Validar que sea mayor o igual a 0.1
                if numero < 0.1:
                    messagebox.showerror(
                        "Valor inválido",
                        "El valor mínimo permitido es 0.1 cm."
                    )
                    return
                datos.append(numero)

            # Validar que no todos los datos sean iguales a cero 
            if all(d == 0 for d in datos):
                messagebox.showerror(
                    "Datos inválidos",
                    "Todos los valores no pueden ser 0."
                )
                return

            # Predicción
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
