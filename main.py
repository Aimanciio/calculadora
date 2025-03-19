import tkinter as tk
from tkinter import messagebox
import pickle
from dataclasses import dataclass
import math

@dataclass
class CalculatorState:
    expression: str = ""

# Colores de los botones
BUTTON_COLORS = {
    'CE': 'orange',
    'C': 'orange',
    '=': 'orange',
    'MEM': 'dark blue'
}

# Configuración de la fuente
RETRO_FONT = ("Courier", 18, "bold")

def evaluate_expression(expression):
    try:
        expression = expression.replace('×', '*').replace('÷', '/')
        expression = expression.replace('^', '**')

        if 'sin(' in expression:
            expression = expression.replace('sin(', 'math.sin(')
        if 'cos(' in expression:
            expression = expression.replace('cos(', 'math.cos(')
        if 'tan(' in expression:
            expression = expression.replace('tan(', 'math.tan(')
        if 'log(' in expression:
            expression = expression.replace('log(', 'math.log10(')
        if 'ln(' in expression:
            expression = expression.replace('ln(', 'math.log(')
        if '√(' in expression:
            expression = expression.replace('√(', 'math.sqrt(')
        if '!' in expression:
            expression = expression.replace('!', 'math.factorial(')
        if 'frac(' in expression:
            expression = expression.replace('frac(', '(')

        result = eval(expression)
        return str(result)
    except Exception:
        return "Error"

def click(button_text):
    if button_text == "=":
        state.expression = evaluate_expression(state.expression)
        if state.expression == "Error":
            display_var.set("Error")
            root.after(1000, reset_calculator)
            return
    elif button_text == "C":
        state.expression = state.expression[:-1]
    elif button_text == "CE":
        state.expression = ""
    elif button_text == "MEM":
        pass
    else:
        if len(state.expression) < 20:
            state.expression += button_text

    update_display()

def update_display():
    display_var.set(state.expression)

def reset_calculator():
    state.expression = ""
    update_display()

def save_state():
    with open("calculator.sav", "wb") as file:
        pickle.dump(state, file)
    messagebox.showinfo("Guardado", "Estado guardado exitosamente.")

def load_state():
    try:
        with open("calculator.sav", "rb") as file:
            global state
            state = pickle.load(file)
        update_display()
        messagebox.showinfo("Cargado", "Estado cargado exitosamente.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró ningún archivo de estado.")

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora Científica")

# Crear un widget de entrada con fondo verde y texto negro
display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, width=20, font=RETRO_FONT, borderwidth=2, relief="solid", bg="green", fg="black", justify="right")
display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, ipady=20)

# Definir los botones en un diccionario para evitar repetición
buttons_layout = [
    ['sin', 'cos', 'tan', '(', ')', '1/x'],
    ['MEM', 'DEL', 'R', 'π', 'log', 'ln'],
    ['7', '8', '9', 'CE', 'C', '='],
    ['4', '5', '6', '×', 'EXP', '^'],
    ['1', '2', '3', '+', '÷', 'frac'],
    ['0', '.', '√', '-', '!']
]

# Crear y colocar los botones usando el diccionario
for row_idx, row in enumerate(buttons_layout, start=1):
    for col_idx, button_text in enumerate(row):
        bg_color = BUTTON_COLORS.get(button_text, 'grey')
        fg_color = 'white' if bg_color in ['orange', 'dark blue'] else 'black'
        tk.Button(root, text=button_text, width=5, height=2, font=RETRO_FONT, bg=bg_color, fg=fg_color,
                  command=lambda text=button_text: click(text)).grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)

# Configurar el tamaño de las filas y columnas
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Estado inicial de la calculadora
state = CalculatorState()

# Ejecutar la aplicación
root.mainloop()
