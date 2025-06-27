from os import system
from time import sleep

class Gpio:
    def __init__(self, num, mode):
        if 0 <= num <= 40:
            self.num = num
        else:
            raise ValueError('Número de pin inválido -> Introduzca un número de 0 a 40')

        if mode in ['out', 'write']:
            self.mode = 'out'
        elif mode in ['in', 'read']:
            self.mode = 'in'
        else:
            raise ValueError('Modo de pin inválido -> Introduzca "out" o "write" para salida, "in" o "read" para entrada')

        self.export_pin()
        self.set_mode(self.mode)

    def export_pin(self):
        system(f'echo {self.num} > /sys/class/gpio/export')
        sleep(0.05)

    def unexport_pin(self):
        system(f'echo {self.num} > /sys/class/gpio/unexport')

    def set_mode(self, mode):
        system(f'echo {mode} > /sys/class/gpio/gpio{self.num}/direction')

    def write(self, A):
        if value in [0, 'LOW']:
            system(f'echo 0 > /sys/class/gpio/gpio{self.num}/value')
        elif value in [1, 'HIGH']:
            system(f'echo 1 > /sys/class/gpio/gpio{self.num}/value')
        else:
            raise ValueError('Invalid value -> Enter 1 or "HIGH" for HIGH, 0 or "LOW" for LOW')

    def read(self):
        with open(f'/sys/class/gpio/gpio{self.num}/value', 'r') as file:
            return file.read().strip()

    def reset(self):
        self.write(0)
        self.set_mode('in')

    def __del__(self):
        self.reset()
        self.unexport_pin()
