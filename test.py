from gpiozero import LED, DigitalInputDevice, DigitalOutputDevice
from pause import seconds
from src.level_alarm import Level_alarm
from src.pump_control import Pump_control

if __name__ == "__main__":
    pump_out = DigitalOutputDevice(5)
    indicator_led__out = LED(3)
    level_alarm_in = DigitalInputDevice(4)

    pump_control = Pump_control(pump_out, level_alarm_in)
    leve_alarm = Level_alarm(level_alarm_in, indicator_led__out, pump_out)

    while True:
        seconds(20)
        pump_control.irrigation(10)
