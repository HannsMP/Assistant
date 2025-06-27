import os
from time import sleep
from gpio import Gpio

class FanController:
    def __init__(self, control_pin, status_pin, threshold_temp):
        self.control_pin = Gpio(control_pin, 'out')
        self.status_pin = Gpio(status_pin, 'in')
        self.threshold_temp = threshold_temp

    def get_cpu_temp(self):
        temp_str = os.popen('vcgencmd measure_temp').readline()
        temp = float(temp_str.replace("temp=", "").replace("'C\n", ""))
        return temp

    def control_fan(self):
        while True:
            current_temp = self.get_cpu_temp()
            if current_temp >= self.threshold_temp:
                self.control_pin.write('HIGH')
            else:
                self.control_pin.write('LOW')
            sleep(5)

    def read_fan_status(self):
        return self.status_pin.read()

def main():
    fan_controller = FanController(
        control_pin=13, 
        status_pin=19,
        threshold_temp=60
    )
    try:
        fan_controller.control_fan()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
