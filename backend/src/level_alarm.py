from gpiozero import DigitalInputDevice, LED, DigitalOutputDevice
import logging


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
        self.level_sensor.when_activated = self.__tank_not_empty

    def __tank_empty(self) -> None:
        logging.info("Tank is Empty")
        self.empty_indicator_led.on()
        self.pump_output.off()

    def __tank_not_empty(self) -> None:
        logging.info("Tank is not Empty")
        self.empty_indicator_led.off()

    def status(self) -> bool:
        return bool(self.level_sensor.value)
