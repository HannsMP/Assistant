import numpy as np


class Evento:
    def __init__(self, tipo, datos=None):
        self.tipo = tipo
        self.datos = datos


class Publicador:
    def __init__(self):
        self.suscriptores = np.array([], dtype=object)

    def suscribir(self, suscriptor):
        self.suscriptores = np.append(self.suscriptores, suscriptor)

    def notificar(self, evento):
        # Crear una matriz de eventos para cada suscriptor
        eventos = np.full(len(self.suscriptores), evento)
        # Ejecutar el método actualizar de cada suscriptor
        np.vectorize(Suscriptor.actualizar)(self.suscriptores, eventos)


class Suscriptor:
    def __init__(self, nombre):
        self.nombre = nombre

    def actualizar(self, evento):
        print(f"{self.nombre} recibió el evento '{evento.tipo}' con datos: {evento.datos}")


# --------------------------------------------------
# ----------------------- TEST ---------------------
# --------------------------------------------------

if __name__ == "__main__":
    # Uso del sistema de eventos con listado de suscriptores NumPy
    publicador = Publicador()

    juan = Suscriptor("Juan")
    maria = Suscriptor("Maria")

    publicador.suscribir(juan)
    publicador.suscribir(maria)

    evento_1 = Evento("clic_mouse", {"x": 100, "y": 50})
    evento_2 = Evento("tecla_presionada", {"tecla": "A"})

    publicador.notificar(evento_1)
    publicador.notificar(evento_2)
