from time import sleep
import asyncio
import threading


class Async:
    def __init__(self):
        self.value = 0

    def log(self):
        async def printer():
            while True:
                print(f"\rItaracion: {self.value}", end="", flush=True)
                sleep(0.01)

        def run():
            asyncio.run(printer())

        return threading.Thread(target=run)

    def change(self):
        i = 0
        while True:
            self.value = i = i + 1
            sleep(0.1)

            if(i == 100):
                break


a = Async()

line = a.log()
line.start()
a.change()
line.join()