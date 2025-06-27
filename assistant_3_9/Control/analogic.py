import pigpio

class Gpio:
    def __init__(self, pin, mode, pwm_freq=None):
        self.pin = pin
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("No se puede conectar a pigpio daemon")

        if mode == 'out':
            self.pi.set_mode(self.pin, pigpio.OUTPUT)
        elif mode == 'in':
            self.pi.set_mode(self.pin, pigpio.INPUT)
        elif mode == 'pwm':
            self.pi.set_mode(self.pin, pigpio.OUTPUT)
            if pwm_freq:
                self.pi.set_PWM_frequency(self.pin, pwm_freq)
        else:
            raise ValueError('Modo de pin inválido -> Introduzca "out" para salida, "in" para entrada, "pwm" para PWM')

    def write(self, value):
        if isinstance(value, int) and 0 <= value <= 255:
            self.pi.set_PWM_dutycycle(self.pin, value)
        elif value in [0, 1]:
            self.pi.write(self.pin, value)
        else:
            raise ValueError('Valor inválido -> Introduzca un número entre 0 y 255 para PWM, 0 o 1 para digital')

    def read(self):
        return self.pi.read(self.pin)

    def set_pwm_frequency(self, frequency):
        self.pi.set_PWM_frequency(self.pin, frequency)

    def __del__(self):
        self.pi.stop()