import sys
import time

# Imprimir tres líneas vacías para dejar espacio
sys.stdout.write("\n" * 3)
sys.stdout.flush()

# Ejemplo de lista de mensajes y niveles de audio
mensajes = ["Escuchando", "Procesando", "Respondiendo"]
niveles_audio = [0.5, 0.7, 0.9]
respuestas = ["Mensaje de respuesta 1", "Mensaje de respuesta 2", "Mensaje de respuesta 3"]
"""
for i in range(len(mensajes)):
    # Mover el cursor hacia arriba en la terminal
    sys.stdout.write("\033[A")
    sys.stdout.write("\033[A")
    sys.stdout.write("\033[A")

    # Imprimir estado
    sys.stdout.write(f"\rEstado: {mensajes[i]}")
    sys.stdout.flush()

    #sys.stdout.write("\033[B")
    # Imprimir nivel de audio
    sys.stdout.write(f"Nivel de audio: {niveles_audio[i]}")
    sys.stdout.flush()

    #sys.stdout.write("\033[B")
    # Imprimir mensaje de respuesta
    sys.stdout.write(f"Respuesta: {respuestas[i]}")
    sys.stdout.flush()

    time.sleep(1)  # Simulación de procesamiento
"""

print(8000//9)