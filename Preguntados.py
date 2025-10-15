import tkinter as tk
from tkinter import messagebox
import random
import time


def iniciar_juego():
    frame_inicio.pack_forget()
    frame_juego.pack(fill="both", expand=True)
    actualizar_puntaje()
    lbl_turno.config(text=f"Turno de: {jugadores[0]}")

def elegir_categoria(cat):
    global pregunta_actual, opciones_actuales, respuesta_correcta
    pregunta_actual, opciones_actuales, respuesta_correcta = random.choice(preguntas[cat])
    lbl_categoria.config(text=f"Categoría: {cat}")
    lbl_pregunta.config(text=pregunta_actual)
    color_categoria = colores_categoria[cat]
    for i, boton in enumerate(botones_opciones):
        boton.config(text=opciones_actuales[i], state="normal", bg=color_categoria, fg="white")

def verificar_respuesta(opcion):
    global turno
    jugador = jugadores[turno % 2]
    if opcion == respuesta_correcta:
        messagebox.showinfo("✅ Correcto", f"¡Excelente {jugador}!")
        puntaje[jugador] += 1
    else:
        messagebox.showerror("❌ Incorrecto", f"La respuesta correcta era: {respuesta_correcta}")
    actualizar_puntaje()

    
    total_preguntas_jugadas = (turno + 1)
    if total_preguntas_jugadas >= rondas_por_jugador * 2:
        if puntaje[jugadores[0]] > puntaje[jugadores[1]]:
            mostrar_insignia(jugadores[0])
            return
        elif puntaje[jugadores[1]] > puntaje[jugadores[0]]:
            mostrar_insignia(jugadores[1])
            return
        else:
            mostrar_empate()
            return

    turno += 1
    lbl_turno.config(text=f"Turno de: {jugadores[turno % 2]}")
    lbl_pregunta.config(text="Selecciona una categoría para continuar")
    for boton in botones_opciones:
        boton.config(state="disabled", bg="#b0bec5")

def actualizar_puntaje():
    lbl_puntaje.config(text=f"{jugadores[0]}: {puntaje[jugadores[0]]} | {jugadores[1]}: {puntaje[jugadores[1]]}")

def mostrar_insignia(ganador):
    frame_juego.pack_forget()
    frame_insignia.pack(fill="both", expand=True)
    lbl_ganador.config(text=f"🏆 ¡{ganador} ganó la INSIGNIA! 🏅")
    btn_reiniciar.pack(pady=15)
    animar_insignia()

def mostrar_empate():
    frame_juego.pack_forget()
    frame_insignia.pack(fill="both", expand=True)
    lbl_ganador.config(text="🤝 ¡Empate! Ambos jugadores lo hicieron excelente 🎯")
    btn_reiniciar.pack(pady=15)
    animar_insignia()

def animar_insignia():
    for i in range(8):
        canvas_insignia.itemconfig(circulo, fill=f"#{hex(200+i*7)[2:]}f7fa")
        ventana.update()
        time.sleep(0.1)

def reiniciar_juego():
    global puntaje, turno
    puntaje = {jugadores[0]: 0, jugadores[1]: 0}
    turno = 0
    frame_insignia.pack_forget()
    frame_juego.pack(fill="both", expand=True)
    lbl_puntaje.config(text=f"{jugadores[0]}: 0 | {jugadores[1]}: 0")
    lbl_turno.config(text=f"Turno de: {jugadores[0]}")
    lbl_pregunta.config(text="Selecciona una categoría para comenzar")
    lbl_categoria.config(text="")
    for boton in botones_opciones:
        boton.config(text="", state="disabled", bg="#b0bec5")


preguntas = {
    "Inteligencia Artificial": [
        ("¿Qué significa IA?", ["Inteligencia Artificial", "Interfaz Avanzada", "Ingeniería Algorítmica", "Input Automático"], "Inteligencia Artificial"),
        ("¿Qué lenguaje se usa más en IA?", ["Java", "Python", "C++", "PHP"], "Python"),
        ("¿Qué es el aprendizaje automático?", ["Un juego", "Una rama de la IA", "Un lenguaje de programación", "Una red"], "Una rama de la IA"),
        ("¿Qué es una red neuronal?", ["Un conjunto de cables", "Un modelo que imita el cerebro", "Un algoritmo matemático", "Un hardware"], "Un modelo que imita el cerebro"),
        ("¿Qué es el deep learning?", ["Una técnica avanzada de IA", "Una base de datos", "Un lenguaje de bajo nivel", "Un virus"], "Una técnica avanzada de IA"),
        ("¿Qué es el procesamiento del lenguaje natural?", ["IA para entender texto", "IA para imágenes", "Compresión de datos", "Minería de texto"], "IA para entender texto"),
        ("¿Qué es la visión por computadora?", ["IA que interpreta imágenes", "Un sensor óptico", "Un tipo de cámara", "Un lenguaje visual"], "IA que interpreta imágenes"),
        ("¿Qué es el overfitting?", ["Cuando el modelo memoriza los datos", "Cuando falla la red", "Error de cálculo", "Cuando se borra un dataset"], "Cuando el modelo memoriza los datos"),
        ("¿Qué hace TensorFlow?", ["Biblioteca de IA", "Software antivirus", "Sistema operativo", "Framework de red"], "Biblioteca de IA"),
        ("¿Qué es la IA generativa?", ["IA que crea contenido nuevo", "IA que analiza virus", "IA que clasifica datos", "IA para hardware"], "IA que crea contenido nuevo"),
    ],
    "Ciberseguridad": [
        ("¿Qué es el phishing?", ["Robo de información con engaño", "Virus del sistema", "Protección de datos", "Copia de seguridad"], "Robo de información con engaño"),
        ("¿Qué es un firewall?", ["Filtro de red", "Sistema de archivos", "Lenguaje de programación", "Cortafuegos de hardware"], "Filtro de red"),
        ("¿Qué es un virus informático?", ["Software dañino", "Antivirus", "Programa de respaldo", "Archivo comprimido"], "Software dañino"),
        ("¿Qué es un ransomware?", ["Software que pide rescate", "Antivirus", "Navegador web", "Router"], "Software que pide rescate"),
        ("¿Qué es una contraseña segura?", ["Contiene letras, números y símbolos", "Solo números", "Nombre del usuario", "Palabra simple"], "Contiene letras, números y símbolos"),
        ("¿Qué es el hacking ético?", ["Pruebas de seguridad autorizadas", "Ataques maliciosos", "Ingeniería inversa ilegal", "Uso de malware"], "Pruebas de seguridad autorizadas"),
        ("¿Qué es un ataque DDoS?", ["Saturar un servidor", "Eliminar virus", "Instalar software", "Filtrar tráfico"], "Saturar un servidor"),
        ("¿Qué hace un antivirus?", ["Detecta y elimina malware", "Aumenta la velocidad", "Crea redes", "Edita imágenes"], "Detecta y elimina malware"),
        ("¿Qué es una VPN?", ["Red privada virtual", "Protocolo de red local", "Sistema de seguridad física", "Gestor de contraseñas"], "Red privada virtual"),
        ("¿Qué es la autenticación de dos factores?", ["Verificación extra de identidad", "Backup automático", "Inicio sin contraseña", "Escaneo de hardware"], "Verificación extra de identidad"),
    ],
    "Programación": [
        ("¿Qué hace la función print en Python?", ["Muestra texto", "Suma números", "Importa librerías", "Guarda archivos"], "Muestra texto"),
        ("¿Qué es una variable?", ["Espacio para guardar datos", "Un bucle", "Una condición", "Un archivo"], "Espacio para guardar datos"),
        ("¿Qué tipo de lenguaje es Python?", ["Interpretado", "Compilado", "Binario", "Visual"], "Interpretado"),
        ("¿Qué es un bucle for?", ["Estructura repetitiva", "Función matemática", "Lista de datos", "Condición lógica"], "Estructura repetitiva"),
        ("¿Qué hace 'if' en Python?", ["Evalúa una condición", "Crea una lista", "Guarda un valor", "Imprime texto"], "Evalúa una condición"),
        ("¿Qué es una función?", ["Bloque de código reutilizable", "Un error de sintaxis", "Una constante", "Un archivo"], "Bloque de código reutilizable"),
        ("¿Qué es un IDE?", ["Entorno de desarrollo", "Motor de búsqueda", "Servidor web", "Editor de texto plano"], "Entorno de desarrollo"),
        ("¿Qué significa 'def'?", ["Define una función", "Declara una variable", "Cierra un bloque", "Inicia un bucle"], "Define una función"),
        ("¿Qué es un comentario?", ["Texto ignorado por el programa", "Código ejecutable", "Error de sintaxis", "Variable global"], "Texto ignorado por el programa"),
        ("¿Qué es una lista en Python?", ["Colección ordenada de elementos", "Un bucle", "Un módulo", "Un archivo"], "Colección ordenada de elementos"),
    ],
    "Redes": [
        ("¿Qué significa IP?", ["Internet Protocol", "Internal Port", "Integrated Process", "Internet Program"], "Internet Protocol"),
        ("¿Qué hace un router?", ["Conecta redes", "Cifra datos", "Crea usuarios", "Edita contraseñas"], "Conecta redes"),
        ("¿Qué es una LAN?", ["Red local", "Red global", "Router central", "Servidor web"], "Red local"),
        ("¿Qué es una WAN?", ["Red amplia", "Red local", "Red cerrada", "Cable de red"], "Red amplia"),
        ("¿Qué es el DNS?", ["Traduce nombres a IPs", "Conecta dispositivos", "Envía datos", "Guarda contraseñas"], "Traduce nombres a IPs"),
        ("¿Qué es una dirección MAC?", ["Identificador único de hardware", "Contraseña del router", "Dirección IP", "Tipo de red"], "Identificador único de hardware"),
        ("¿Qué es un switch?", ["Conecta varios dispositivos", "Divide señales eléctricas", "Controla la velocidad", "Convierte IPs"], "Conecta varios dispositivos"),
        ("¿Qué hace un servidor?", ["Provee recursos o servicios", "Guarda contraseñas", "Cifra datos", "Genera IPs"], "Provee recursos o servicios"),
        ("¿Qué protocolo usa la web?", ["HTTP", "FTP", "SMTP", "SSH"], "HTTP"),
        ("¿Qué es un puerto de red?", ["Canal de comunicación lógico", "Cable de red", "Antena WiFi", "IP temporal"], "Canal de comunicación lógico"),
    ]
}


jugadores = ["Jugador 1", "Jugador 2"]
puntaje = {jugadores[0]: 0, jugadores[1]: 0}
turno = 0
pregunta_actual = None
respuesta_correcta = None
rondas_por_jugador = 3  


ventana = tk.Tk()
ventana.title("🎯 Preguntados Tecnológicos")
ventana.geometry("800x600")
ventana.config(bg="#e0f7fa")

colores_categoria = {
    "Inteligencia Artificial": "#0288d1",
    "Ciberseguridad": "#c62828",
    "Programación": "#2e7d32",
    "Redes": "#6a1b9a"
}


frame_inicio = tk.Frame(ventana, bg="#00acc1")
frame_inicio.pack(fill="both", expand=True)
tk.Label(frame_inicio, text="🎮 PREGUNTADOS TECNOLÓGICOS 🎮", font=("Arial", 26, "bold"), fg="white", bg="#00acc1").pack(pady=120)
tk.Button(frame_inicio, text="Comenzar Juego", font=("Arial", 16, "bold"), bg="#004d40", fg="white", width=18, height=2, command=iniciar_juego).pack()


frame_juego = tk.Frame(ventana, bg="#e0f7fa")

lbl_turno = tk.Label(frame_juego, text="", font=("Arial", 18, "bold"), bg="#e0f7fa")
lbl_turno.pack(pady=15)

frame_categorias = tk.Frame(frame_juego, bg="#e0f7fa")
frame_categorias.pack(pady=10)

for cat in preguntas.keys():
    tk.Button(frame_categorias, text=cat, width=18, height=2, bg=colores_categoria[cat], fg="white", font=("Arial", 12, "bold"),
              command=lambda c=cat: elegir_categoria(c)).pack(side="left", padx=5)

lbl_categoria = tk.Label(frame_juego, text="", font=("Arial", 14, "italic"), bg="#e0f7fa")
lbl_categoria.pack()

lbl_pregunta = tk.Label(frame_juego, text="Selecciona una categoría para comenzar", font=("Arial", 14), wraplength=650, bg="#e0f7fa")
lbl_pregunta.pack(pady=20)

frame_opciones = tk.Frame(frame_juego, bg="#e0f7fa")
frame_opciones.pack()

botones_opciones = []
for i in range(4):
    b = tk.Button(frame_opciones, text="", width=35, height=2, state="disabled", bg="#b0bec5", fg="black",
                  font=("Arial", 12), command=lambda i=i: verificar_respuesta(botones_opciones[i].cget("text")))
    b.pack(pady=5)
    botones_opciones.append(b)

lbl_puntaje = tk.Label(frame_juego, text=f"{jugadores[0]}: 0 | {jugadores[1]}: 0", font=("Arial", 14, "bold"), bg="#e0f7fa")
lbl_puntaje.pack(pady=10)


frame_insignia = tk.Frame(ventana, bg="#fff3e0")
lbl_ganador = tk.Label(frame_insignia, text="", font=("Arial", 22, "bold"), bg="#fff3e0", fg="#bf360c")
lbl_ganador.pack(pady=30)
canvas_insignia = tk.Canvas(frame_insignia, width=200, height=200, bg="#fff3e0", highlightthickness=0)
canvas_insignia.pack()
circulo = canvas_insignia.create_oval(50, 50, 150, 150, fill="#ffcc80", outline="#fb8c00", width=4)
canvas_insignia.create_text(100, 100, text="🏅", font=("Arial", 40))

btn_reiniciar = tk.Button(frame_insignia, text="🔁 Jugar de nuevo", bg="#2e7d32", fg="white", font=("Arial", 14, "bold"), width=16, command=reiniciar_juego)
btn_salir = tk.Button(frame_insignia, text="Salir", bg="#bf360c", fg="white", font=("Arial", 14, "bold"), width=12, command=ventana.destroy)
btn_salir.pack(pady=15)

ventana.mainloop()
