from gpiozero import DigitalOutputDevice, DigitalInputDevice
from time import sleep


class Pump_control:
    def __init__(
        self,
        water_pump: DigitalOutputDevice,
        level_sensor: DigitalInputDevice,
    ) -> None:
        self.pump_output = water_pump
        self.level_sensor = level_sensor

    def status(self) -> bool:
        return self.pump_output.value

    def start(self) -> bool:
        # check that tank is not empty
        if self.level_sensor.value == True:
            self.pump_output.on()
        return self.pump_output.value

    def stop(self) -> None:
        self.pump_output.off()

    def irrigation(self, litre: int) -> None:
        self.start()
        sleep(60)  # here we need a translation from litters to time
        self.stop()
