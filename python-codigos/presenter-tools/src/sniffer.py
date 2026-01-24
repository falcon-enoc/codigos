from pynput import keyboard

def on_press(key):
    try:
        # Intenta leer si es una tecla de caracter (letras, numeros)
        print(f"--> Tecla detectada: {key.char}")
    except AttributeError:
        # Si falla, es una tecla especial (Flechas, PageDown, etc.)
        print(f"--> Tecla Especial detectada: {key}")

    if key == keyboard.Key.esc:
        print("Saliendo...")
        return False

print("=== DIAGNÓSTICO DE PUNTERO ===")
print("1. Asegúrate de que esta ventana esté activa (haz clic aquí).")
print("2. Presiona el botón de tu puntero.")
print("3. Anota el nombre EXACTO que sale abajo.")
print("4. Presiona 'ESC' en tu teclado para salir.")
print("================================")

# Escuchar el teclado
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
