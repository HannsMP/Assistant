import time
import random

# Genera una cadena de nivel de sonido de forma aleatoria
def generate_random_sound_level():
    symbols = ["-", "|"]
    return ''.join(random.choice(symbols) for _ in range(10))

# Simulación de detección de sonido
for _ in range(100):  # Simula 10 estados de sonido
    sound_level = generate_random_sound_level()
    print(f'\r{sound_level}', end='', flush=True)
    #time.sleep(0.1)
print()  # Para asegurarse de que la consola avance a la siguiente línea después de terminar
