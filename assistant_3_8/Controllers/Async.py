import asyncio
import threading
from typing import Callable, Any


class Asyncrono:
    def run(self, func: Callable[[], Any]) -> None:
        """
        Ejecuta una función asincrónica usando asyncio.run.

        :param func: Una función asincrónica que no toma argumentos y puede devolver cualquier valor.
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("La función debe ser una función asincrónica (coroutine).")
        try:
            asyncio.run(func())
        except Exception as e:
            raise ValueError(f"Error al ejecutar la función: {e}")

    def line(self, func: Callable[..., Any], *params: Any) -> threading.Thread:
        """
        Ejecuta una función asincrónica en un nuevo hilo.

        :param func: Una función asincrónica que no toma argumentos y puede devolver cualquier valor.
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("La función debe ser una función asincrónica (coroutine).")

        def run():
            try:
                asyncio.run(func(*params))
            except Exception as e:
                raise ValueError(f"Error al ejecutar la función en el hilo: {e}")

        return threading.Thread(target=run)


if __name__ == "__main__":
    # Ejemplo de uso
    import time


    class Logger:
        def __init__(self):
            self.value = 0
            self.state = True

        async def printer(self):
            while self.state:
                print(f"\rIteración: {self.value}", end="", flush=True)
                await asyncio.sleep(0.01)

        def change(self):
            i = 0
            while self.state:
                self.value = i = i + 1
                time.sleep(0.1)
                if i == 100:
                    self.state = False
                    break


    logger = Logger()
    Async = Asyncrono()
    line = Async.line(logger.printer)
    line.start()
    logger.change()
    line.join()  # Asegura que el hilo termine antes de finalizar el programa
