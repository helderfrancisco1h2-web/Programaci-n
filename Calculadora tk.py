import tkinter as tk
from tkinter import messagebox
import math


def presionar(tecla):
    if tecla == "C":
        entrada_var.set("")
    elif tecla == "=":
        try:
            expresion = entrada_var.get()
            expresion = expresion.replace("×", "*").replace("÷", "/").replace("^", "**")
            resultado = eval(expresion)
            entrada_var.set(str(resultado))
        except Exception:
            messagebox.showerror("Error", "Expresión inválida")
            entrada_var.set("")
    elif tecla == "√":
        try:
            valor = float(entrada_var.get())
            entrada_var.set(str(math.sqrt(valor)))
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para raíz cuadrada")
    elif tecla == "sin":
        try:
            valor = float(entrada_var.get())
            entrada_var.set(str(round(math.sin(math.radians(valor)), 6)))
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para seno")
    elif tecla == "cos":
        try:
            valor = float(entrada_var.get())
            entrada_var.set(str(round(math.cos(math.radians(valor)), 6)))
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para coseno")
    elif tecla == "tan":
        try:
            valor = float(entrada_var.get())
            entrada_var.set(str(round(math.tan(math.radians(valor)), 6)))
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para tangente")
    elif tecla == "log":
        try:
            valor = float(entrada_var.get())
            if valor <= 0:
                messagebox.showerror("Error", "El logaritmo solo está definido para números positivos.")
            else:
                entrada_var.set(str(round(math.log10(valor), 6)))
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para logaritmo")
    elif tecla == "π":
        entrada_var.set(entrada_var.get() + str(math.pi))
    else:
        entrada_var.set(entrada_var.get() + tecla)


root = tk.Tk()
root.title("Calculadora Científica 🇦🇷")
root.resizable(False, False)
root.configure(bg="white")


banner_superior = tk.Frame(root, bg="#5DADE2", height=40)
banner_superior.grid(row=0, column=0, columnspan=5, sticky="nsew")
tk.Label(banner_superior, text="Calculadora Científica", bg="#5DADE2", fg="white",
         font=("Arial Black", 13)).pack(pady=5)


entrada_var = tk.StringVar()
pantalla = tk.Entry(root, textvariable=entrada_var, font=("Consolas", 18, "bold"), bd=6,
                    relief="sunken", justify="right", bg="#EAF2F8", fg="#154360", width=22)
pantalla.grid(row=1, column=0, columnspan=5, padx=10, pady=10)


botones = [
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("÷", 2, 3), ("C", 2, 4),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("×", 3, 3), ("√", 3, 4),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("−", 4, 3), ("^", 4, 4),
    ("0", 5, 0), (".", 5, 1), ("π", 5, 2), ("+", 5, 3), ("=", 5, 4),
    ("sin", 6, 0), ("cos", 6, 1), ("tan", 6, 2), ("log", 6, 3)
]

for (texto, fila, columna) in botones:
    if texto in ["+", "−", "×", "÷", "=", "^"]:
        color_fondo = "#2E86C1"
        color_texto = "white"
    elif texto in ["C"]:
        color_fondo = "#E74C3C"
        color_texto = "white"
    elif texto in ["√", "π", "sin", "cos", "tan", "log"]:
        color_fondo = "#AED6F1"
        color_texto = "#154360"
    else:
        color_fondo = "white"
        color_texto = "#154360"

    b = tk.Button(root, text=texto, width=6, height=2, bg=color_fondo, fg=color_texto,
                  font=("Arial", 12, "bold"), relief="ridge", bd=3,
                  command=lambda t=texto: presionar(t))
    b.grid(row=fila, column=columna, padx=4, pady=4)


banner_inferior = tk.Frame(root, bg="#5DADE2", height=30)
banner_inferior.grid(row=7, column=0, columnspan=5, sticky="nsew")
tk.Label(banner_inferior, text="Francisco Helder", bg="#5DADE2", fg="white",
         font=("Arial", 10, "bold")).pack(pady=3)

root.mainloop()
