'''La idea de este proyecto es crear un programa que evalúe cuan rápido puedes escribir una oración de manera precisa.
Este programa puede requerir crear una interfaz gráfica de usuario (GUI) mediante el módulo tkinter. 
Si eres nuevo en las GUI, este ejemplo es una buena introducción, ya que tan solo necesitas crear una serie de etiquetas simples, 
botones y campos de entrada para crear una ventana. Puedes usar el módulo timeit de Python para manejar el aspecto de temporización
de nuestra prueba de escritura, y el módulo random para seleccionar aleatoriamente una frase de prueba.'''

import tkinter as tk
import random
import time

FRASES = [
    "El rápido zorro marrón salta sobre el perro perezoso",
    "Python es un lenguaje de programación poderoso y divertido",
    "La práctica hace al maestro en la programación",
    "Aprender a programar abre muchas puertas laborales",
    "La curiosidad es la madre de la ciencia y la tecnología",
    "Nunca es tarde para aprender algo nuevo y útil",
    "El éxito es 1% inspiración y 99% transpiración",
    "Programar es resolver problemas de forma creativa",
    "La perseverancia es clave para dominar cualquier habilidad",
    "Hoy es un gran día para escribir código increíble"
]

class TypingTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test de Velocidad de Escritura")
        self.geometry("800x600")
        self.configure(bg="#2c3e50")
        self.resizable(False, False)

        # Variables
        self.frase_actual = ""
        self.tiempo_inicio = None
        self.timer_id = None

        self.cargar_nueva_frase()
        self.crear_widgets()

    def gestionar_tecla(self, event=None):
        texto_actual = self.entry.get().strip()
        
        if texto_actual and self.tiempo_inicio is None:
            # Primera vez que escribe algo, empieza el tiempo
            self.tiempo_inicio = time.time()
            self.label_info.config(
                text="¡Escribiendo... Presiona Enter cuando termines",
                fg="#f1c40f"
            )
            # AQUÍ EMPIEZA EL RELOJ EN PANTALLA
            self.actualizar_reloj()
            
        elif not texto_actual:
            # Borró todo, reiniciamos el cronómetro
            self.tiempo_inicio = None
            self.label_info.config(
                text="Escribe la frase y presiona Enter",
                fg="#95a5a6"
            )
            self.label_tiempo.config(text="00:00.00", fg="#3498db")

    def actualizar_reloj(self):
        """Actualiza el reloj en pantalla mientras el usuario escribe"""
        if self.tiempo_inicio is not None:
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            minutos = int(tiempo_transcurrido // 60)
            segundos = int(tiempo_transcurrido % 60)
            milisegundos = int((tiempo_transcurrido - int(tiempo_transcurrido)) * 100)
            
            texto_reloj = f"{minutos:02d}:{segundos:02d}.{milisegundos:02d}"
            self.label_tiempo.config(text=texto_reloj, fg="#e74c3c")
            
            # Programar la próxima actualización en 50 ms (20 veces por segundo)
            # Guardamos el ID del próximo after para poder cancelarlo después
            self.timer_id = self.after(50, self.actualizar_reloj)
        else:
            self.label_tiempo.config(text="00:00.00", fg="#3498db")
            self.timer_id = None

            

    def crear_widgets(self):
        # Título
        titulo = tk.Label(self, text="Test de Velocidad de Escritura", 
                         font=("Helvetica", 24, "bold"), fg="#ecf0f1", bg="#2c3e50")
        titulo.pack(pady=20)

        # Frase a escribir
        self.label_frase = tk.Label(self, text=self.frase_actual, font=("Arial", 18),
                                   wraplength=700, fg="#e74c3c", bg="#2c3e50", justify="center")
        self.label_frase.pack(pady=30)

        # Campo de entrada
        self.entry = tk.Entry(self, font=("Arial", 18), justify="center", bd=5, relief="flat")
        self.entry.bind("<KeyRelease>", self.gestionar_tecla) # Inicia el cronómetro
        self.entry.pack(pady=20)
        self.entry.focus()

        # Etiqueta de instrucciones
        self.label_info = tk.Label(self, text="Escribe la frase y presiona Enter", 
                                  font=("Arial", 14), fg="#95a5a6", bg="#2c3e50")
        self.label_info.pack(pady=10)

        # Etiqueta para mostrar el tiempo en vivo
        self.label_tiempo = tk.Label(self, text="00:00", font=("Courier", 20, "bold"),
                                    fg="#3498db", bg="#2c3e50")
        self.label_tiempo.pack(pady=10)

        # Área de resultados (inicialmente vacía)
        self.label_resultado = tk.Label(self, text="", font=("Arial", 16, "bold"),
                                       fg="#2ecc71", bg="#2c3e50")
        self.label_resultado.pack(pady=20)

        # Botón reiniciar
        btn_reiniciar = tk.Button(self, text="Jugar de nuevo", font=("Arial", 14),
                                 command=self.reiniciar)
        btn_reiniciar.pack(pady=10)

        # Vincular Enter
        self.entry.bind("<Return>", lambda event: self.verificar())

    def cargar_nueva_frase(self):
        self.frase_actual = random.choice(FRASES)

    def reiniciar(self):
        self.cargar_nueva_frase()
        self.label_frase.config(text=self.frase_actual)
        # Reactivar el campo
        self.entry.config(state="normal")
        # Borrar lo que había escrito
        self.entry.delete(0, tk.END)
        self.entry.focus()
        # Limpiar resultados
        self.label_resultado.config(text="")
        self.label_info.config(text="Escribe la frase y presiona Enter")
        self.label_tiempo.config(text="00:00.00", fg="#3498db")
        # Detener reloj si estaba corriendo
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.tiempo_inicio = None
        

    def empezar_cronometro(self, event=None):
        """Se llama cada vez que el usuario suelta una tecla.
        Si es la primera vez que escribe algo, empieza el tiempo."""
        # Si ya empezamos a contar, no hacemos nada más
        if self.tiempo_inicio is not None:
            return

        # Si el campo tiene al menos 1 carácter → es la primera vez que escribe
        if self.entry.get().strip():
            self.tiempo_inicio = time.time()  # Inicia el cronómetro
            self.label_info.config(
                text="¡Escribiendo... Presiona Enter cuando termines!",
                fg="#f1c40f"  # color amarillo para avisar que ya empezó
            )

    def verificar_si_vacio(self, event=None):
        """Se llama cada vez que suelta una tecla.
        Si el campo queda vacío → reiniciamos el tiempo."""
        if not self.entry.get().strip():
            self.tiempo_inicio = None
            self.label_info.config(
                text="Escribe la frase y presiona Enter",
                fg="#95a5a6"  # vuelve al color gris original
            )

    def verificar(self, event=None):
        if self.tiempo_inicio is None:
            # Si presionó Enter sin haber escrito nada
            self.label_resultado.config(text="¡Escribe algo primero!", fg="#e74c3c")
            return

        tiempo_final = time.time()
        tiempo_total = tiempo_final - self.tiempo_inicio

        escrito = self.entry.get()
        original = self.frase_actual

        # ---------- CÁLCULO DE PRECISIÓN ----------
        correctos = 0
        for a, b in zip(escrito, original):
            if a == b:
                correctos += 1
        # Si escribió de más o de menos, ajustamos
        longitud_min = min(len(escrito), len(original))
        precision = (correctos / longitud_min) * 100 if longitud_min > 0 else 0

        # ---------- CÁLCULO DE WPM ----------
        palabras_escritas = len(escrito.split())
        minutos = tiempo_total / 60
        wpm = int(palabras_escritas / minutos) if minutos > 0 else 0

        # ---------- FORMATEO DEL RESULTADO ----------
        minutos_str = int(tiempo_total // 60)
        segundos_str = int(tiempo_total % 60)

        # Cambiamos el mensaje de "Escribiendo..."
        self.label_info.config(text="¡Terminado!", fg="#2ecc71")
        
        self.label_resultado.config(
            text=f"Tiempo: {minutos_str:02d}:{segundos_str:02d}\n"
                 f"Palabras por minuto: {wpm}\n"
                 f"Precisión: {precision:.1f}%\n\n"
                 f"¿Quieres volver a intentar con una frase nueva?",
            fg="#2ecc71", font=("Arial", 16, "bold")
        )

        # Detener el reloj en vivo
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        
        # Mostrar el tiempo final bonito
        minutos_str = int(tiempo_total // 60)
        segundos_str = int(tiempo_total % 60)
        self.label_tiempo.config(text=f"{minutos_str:02d}:{segundos_str:02d}", fg="#2ecc71")

        # Desactivar el entry para que no siga escribiendo
        self.entry.config(state="disabled")

if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop() 