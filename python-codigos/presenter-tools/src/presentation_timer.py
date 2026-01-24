import time
import os
import sys
from pynput import keyboard

# --- CONFIGURACIÓN ---
TECLA_SIGUIENTE = keyboard.Key.page_down  # Pitch down -> Siguiente
TECLA_ANTERIOR = keyboard.Key.page_up     # Pitch up -> Anterior
TECLA_TAP = keyboard.Key.tab              # Tap -> INICIAR / TERMINAR sesión

CARPETA_LOGS = "../logs"

# Variables de Estado Global
grabando = False
archivo_actual = None
start_time = None
slide_number = 1
last_slide_time = None

def obtener_nombre_archivo():
    """Busca el siguiente número disponible para el log."""
    if not os.path.exists(CARPETA_LOGS):
        os.makedirs(CARPETA_LOGS)
    
    contador = 1
    while True:
        nombre = f"presentation_{contador:03d}.txt"
        ruta = os.path.join(CARPETA_LOGS, nombre)
        if not os.path.exists(ruta):
            return ruta
        contador += 1

def log_to_file(mensaje):
    """Escribe en el archivo abierto y en la consola."""
    print(mensaje)
    if archivo_actual:
        archivo_actual.write(mensaje + "\n")
        archivo_actual.flush() # Asegura que se guarde en disco al instante

def iniciar_sesion():
    global grabando, archivo_actual, start_time, slide_number, last_slide_time
    
    ruta_archivo = obtener_nombre_archivo()
    archivo_actual = open(ruta_archivo, "w", encoding="utf-8")
    grabando = True
    slide_number = 1
    start_time = time.time()
    last_slide_time = start_time
    
    print("\n" + "="*40)
    log_to_file(f"=== INICIO DE PRESENTACIÓN: {os.path.basename(ruta_archivo)} ===")
    log_to_file(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*40 + "\n")

def terminar_sesion():
    global grabando, archivo_actual
    
    if not grabando:
        return

    duration = time.time() - start_time
    print("\n" + "="*40)
    log_to_file(f"=== FIN DE PRESENTACIÓN ===")
    log_to_file(f"Duración Total: {duration:.2f} segundos")
    log_to_file(f"Total Diapositivas: {slide_number}")
    print("="*40 + "\n")
    
    if archivo_actual:
        archivo_actual.close()
        archivo_actual = None
    
    grabando = False
    print("--> En espera (Presiona TAP para nueva sesión o ESC para salir)")

def check_key(current_key, target_key):
    if isinstance(target_key, str):
        try:
            return current_key.char == target_key
        except AttributeError:
            return False
    return current_key == target_key

def on_press(key):
    global slide_number, last_slide_time
    
    # 1. CONTROL DE SESIÓN (TAP)
    if check_key(key, TECLA_TAP):
        if not grabando:
            iniciar_sesion()
        else:
            terminar_sesion()
        return

    # 2. SALIDA DE EMERGENCIA (ESC)
    if key == keyboard.Key.esc:
        if grabando:
            terminar_sesion()
        print("Saliendo del programa...")
        return False

    # 3. LÓGICA DE DIAPOSITIVAS (Solo si está grabando)
    if grabando:
        if check_key(key, TECLA_SIGUIENTE):
            now = time.time()
            slide_duration = now - last_slide_time
            total_elapsed = now - start_time
            
            log_to_file(f"Slide {slide_number}: {slide_duration:.2f}s (T+{total_elapsed:.2f}s)")
            
            slide_number += 1
            last_slide_time = now
            
        elif check_key(key, TECLA_ANTERIOR):
            # Solo registramos el evento, no cambiamos tiempos para no romper la cronología
            log_to_file(f"--> [Retroceso desde Slide {slide_number}]")
            if slide_number > 1:
                slide_number -= 1

print("=== SISTEMA DE TIMER PARA PRESENTADOR ===")
print(f"1. Presiona TAP ({TECLA_TAP}) para EMPEZAR una nueva grabación.")
print(f"2. Usa el mando para pasar diapositivas.")
print(f"3. Presiona TAP de nuevo para TERMINAR y guardar.")
print(f"4. Presiona ESC para cerrar el programa.")
print(f"Logs se guardarán en: {os.path.abspath(CARPETA_LOGS)}")
print("=========================================")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()