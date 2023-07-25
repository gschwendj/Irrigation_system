import logging
import threading
import socket
import json
from time import sleep


from gpiozero import LED, DigitalInputDevice, DigitalOutputDevice
import schedule


from src.level_alarm import Level_alarm
from src.pump_control import Pump_control


def schedule_loop():
    while True:
        schedule.run_pending()
        sleep(3600)


if __name__ == "__main__":
    udp_ip = "127.0.0.1"
    udp_port = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    pump_out = DigitalOutputDevice(5)
    indicator_led__out = LED(6)
    level_alarm_in = DigitalInputDevice(4, bounce_time=0.1)

    pump_control = Pump_control(pump_out, level_alarm_in, 10)
    level_alarm = Level_alarm(level_alarm_in, indicator_led__out, pump_out)

    logging.basicConfig(level=logging.DEBUG)

    schedule.every().day.at("20:00").do(pump_control.irrigation)

    schedule_thread = threading.Thread(target=schedule_loop, daemon=True)
    schedule_thread.start()

    while True:
        bit_string, addr = sock.recvfrom(1024)
        data = json.loads(bit_string)
        try:
            match data["command"]:
                case "status":
                    answer = json.dumps(
                        {
                            "http_code": 200,
                            "pump_status": pump_control.status(),
                            "water_level_status": level_alarm.status(),
                        }
                    )
                    sock.sendto(answer.encode(), addr)
                case "start_irrigation":
                    answer = json.dumps({"http_code": 200})
                    sock.sendto(answer.encode, addr)
                    pump_control.irrigation(data["pump_volume"])
                case "set_pump_volume":
                    pump_control.set_pump_volume(data["pump_volume"])
                    answer = json.dumps({{"http_code": 200}})

        except KeyError as e:
            logging.error("command has wrong format")
            answer = json.dumps({"http_code": 400, "msg": e})
