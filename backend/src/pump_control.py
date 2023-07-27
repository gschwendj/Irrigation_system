from collections.abc import Callable, Iterable, Mapping
from time import sleep
import logging
import threading
from gpiozero import DigitalOutputDevice, DigitalInputDevice


class Pump_control:
    def __init__(
        self,
        water_pump: DigitalOutputDevice,
        level_sensor: DigitalInputDevice,
        pump_volume: int,
    ) -> None:
        self.pump_output = water_pump
        self.level_sensor = level_sensor
        self.pump_volume = pump_volume

    def __irrigation_Thread_function(self):
        if self.start():
            logging.debug(
                "pump is pumping for {:.2f} seconds / {} litre".format(
                    self.pump_volume / 0.1125, self.pump_volume
                )
            )
            sleep(self.pump_volume / 0.1125)
            self.stop()

    def status(self) -> bool:
        logging.debug("Pump value is: {}".format(self.pump_output.value))
        return bool(self.pump_output.value)

    def set_pump_volume(self, litre: int):
        self.pump_volume = litre

    def start(self) -> bool:
        # check that tank is not empty
        if self.level_sensor.value == True:
            self.pump_output.on()
        logging.debug("Pump value is: {}".format(self.pump_output.value))
        return bool(self.pump_output.value)

    def stop(self) -> None:
        self.pump_output.off()
        logging.debug("Pump value is: {}".format(self.pump_output.value))

    def irrigation(self) -> bool:
        if self.status() == False:  # if pump is already running we dont run it again
            threading.Thread(
                target=self.__irrigation_Thread_function, daemon=True
            ).start()
            return True
        return False
