import logging
import socket
import json
from gpiozero import LED, DigitalInputDevice, DigitalOutputDevice

from src.level_alarm import Level_alarm
from src.pump_control import Pump_control


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    host = "0.0.0.0"
    port = 5000

    pump_out = DigitalOutputDevice(5)
    indicator_led_out = LED(6)
    level_alarm_in = DigitalInputDevice(4, bounce_time=1)
    start_reset_button = DigitalInputDevice(22, bounce_time=0.1)

    level_alarm = Level_alarm(level_alarm_in, indicator_led_out, pump_out)
    pump_control = Pump_control(pump_out, level_alarm, start_reset_button, 10)

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                data = json.loads(conn.recv(1024))

                try:
                    match data["command"]:
                        case "status":
                            answer = json.dumps(
                                {
                                    "http_code": 200,
                                    "pump_status": pump_control.status(),
                                    "water_level_status": level_alarm.status(),
                                    "pump_volume": pump_control.pump_volume,
                                }
                            )
                            conn.sendall(answer.encode())
                        case "start_irrigation":
                            pump_control.irrigation()
                            answer = json.dumps({"http_code": 200})
                            conn.sendall(answer.encode())
                        case "set_pump_volume":
                            pump_control.set_pump_volume(data["volume"])
                            answer = json.dumps({"http_code": 200})
                            conn.sendall(answer.encode())
                        case "reset_level_alarm":
                            level_alarm.reset_empty_tank()
                            answer = json.dumps({"http_code": 200})
                            conn.sendall(answer.encode())

                except KeyError as e:
                    logging.error("command has wrong format")
                    answer = json.dumps({"http_code": 400, "msg": str(e)})
                    conn.sendall(answer.encode())
