import os
from datetime import datetime
from time import sleep

class Logger:
    def __init__(self, dirPrint="log/log.txt", dirErr="log/error.txt"):
        self.dirPrint = dirPrint
        self.dirErr = dirErr

        # Crear directorios si no existen
        os.makedirs(os.path.dirname(dirPrint), exist_ok=True)
        os.makedirs(os.path.dirname(dirErr), exist_ok=True)

        # Leer el contenido existente de los archivos si existen, o inicializarlos vacíos
        self.log_content = self._read_file(self.dirPrint)
        self.err_content = self._read_file(self.dirErr)

        self.status = "Iniciando"
        self.sound = "--------------------"
        self.step = 0

    def _read_file(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                return file.read()
        else:
            return ""

    def _write_to_file(self, filepath, content):
        with open(filepath, 'w') as file:
            file.write(content)

    def _get_timestamp(self):
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def err(self, error_message):
        timestamp = self._get_timestamp()
        new_entry = f"[{timestamp}]: {error_message}\n{self.err_content}"
        self.err_content = new_entry
        self._write_to_file(self.dirErr, new_entry)

    def log(self, log_message):
        timestamp = self._get_timestamp()
        new_entry = f"[{timestamp}]: {log_message}\n{self.log_content}"
        self.log_content = new_entry
        self._write_to_file(self.dirPrint, new_entry)

    async def printer(self):
        while True:
            p = "." * (self.step // 3)
            print(f"\r[{self.sound}]: {self.status}{p}", end="", flush=True)
            self.step += 1
            if self.step > 10:
                self.step = 0
            sleep(0.1)


if __name__ == "__main__":
    # Uso de la clase Logger
    log = Logger()

    # Simular el registro de mensajes de log y error
    log.log("Este es un mensaje de log.")
    log.err("Este es un mensaje de error.")

    # Imprimir el estado actual
    log.status = "Estado actual del sistema"
    log.printer()
