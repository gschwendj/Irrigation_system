from time import sleep
import logging
import threading
from gpiozero import DigitalOutputDevice, DigitalInputDevice

from .level_alarm import Level_alarm


class Pump_control:
    def __init__(
        self,
        water_pump: DigitalOutputDevice,
        level_alarm: Level_alarm,
        start_reset_button: DigitalInputDevice,
        pump_volume: int,
    ) -> None:
        self.pump_output = water_pump
        self.level_alarm = level_alarm
        self.start_reset = start_reset_button
        self.pump_volume = pump_volume
        self.start_reset.when_activated = self.__start_reset_pressed

    def __irrigation_Thread_function(self) -> None:
        if self.start():
            logging.debug(
                "pump is pumping for {:.2f} seconds / {} litre".format(
                    self.pump_volume / 0.1125, self.pump_volume
                )
            )
            sleep(self.pump_volume / 0.1125)
            self.stop()

    def __start_reset_pressed(self) -> None:
        if self.level_alarm.status():
            logging.debug("reset button pressed")
            self.level_alarm.reset_empty_tank()
        else:
            logging.debug("start button pressed")
            self.irrigation()

    def status(self) -> bool:
        logging.debug("Pump value is: {}".format(self.pump_output.value))
        return bool(self.pump_output.value)

    def set_pump_volume(self, litre: int) -> None:
        logging.debug(f"set volume to {litre} litre")
        self.pump_volume = litre

    def start(self) -> bool:
        # check that tank is not empty
        if self.level_alarm.status() == False:
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
