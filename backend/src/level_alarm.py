import logging
from gpiozero import DigitalInputDevice, LED, DigitalOutputDevice


class Level_alarm:
    def __init__(
        self,
        level_sensor: DigitalInputDevice,
        level_indicator_led: LED,
        water_pump: DigitalOutputDevice,
    ) -> None:
        self.pump_output = water_pump
        self.level_sensor = level_sensor
        self.empty_indicator_led = level_indicator_led
        self.level_sensor.when_deactivated = self.__tank_empty

    def __tank_empty(self) -> None:
        logging.info("Tank is Empty")
        self.empty_indicator_led.on()
        self.pump_output.off()

    def reset_empty_tank(self) -> None:
        if self.level_sensor.value == 1:
            logging.info("Tank is Full")
            self.empty_indicator_led.off()

    def status(self) -> bool:
        return bool(self.empty_indicator_led.value)
