from gpiozero import DigitalOutputDevice, DigitalInputDevice
from time import sleep
import logging


class Pump_control:
    def __init__(
        self,
        water_pump: DigitalOutputDevice,
        level_sensor: DigitalInputDevice,
    ) -> None:
        self.pump_output = water_pump
        self.level_sensor = level_sensor

    def status(self) -> bool:
        logging.debug("Pump value is: {}".format(self.pump_output.value))
        return bool(self.pump_output.value)

    def start(self) -> bool:
        # check that tank is not empty
        if self.level_sensor.value == True:
            self.pump_output.on()
        logging.debug("Pump value is: {}".format(self.pump_output.value))
        return bool(self.pump_output.value)

    def stop(self) -> None:
        self.pump_output.off()
        logging.debug("Pump value is: {}".format(self.pump_output.value))

    def irrigation(self, litre: int) -> None:
        if self.start():
            logging.debug(
                "pump is pumping for {:.2f} seconds / {} litre".format(
                    litre / 0.1125, litre
                )
            )
            sleep(litre / 0.1125)
            self.stop()
