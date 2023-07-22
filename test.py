import logging
import time
from gpiozero import LED, DigitalInputDevice, DigitalOutputDevice
import schedule

from src.level_alarm import Level_alarm
from src.pump_control import Pump_control

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    pump_out = DigitalOutputDevice(5)
    indicator_led__out = LED(6)
    level_alarm_in = DigitalInputDevice(4, bounce_time=0.1)

    pump_control = Pump_control(pump_out, level_alarm_in)
    leve_alarm = Level_alarm(level_alarm_in, indicator_led__out, pump_out)

    schedule.every().day.at("20:00").do(pump_control.irrigation, litre=10)

    while True:
        schedule.run_pending()
        time.sleep(1)
