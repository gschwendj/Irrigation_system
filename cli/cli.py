from sys import exit
import logging
import socket
import argparse
import json


def main():
    host = "localhost"
    port = 5000
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        prog="IrrigationCtrl", description="CLI for the Irrigation System."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-s", "--start", action="store_true", help="starts the irrigation process"
    )
    group.add_argument(
        "-i",
        "--status",
        action="store_true",
        help="returns the status of the irrigation system",
    )
    group.add_argument(
        "-v",
        "--volume",
        action="store",
        type=int,
        help="set the volume in litre that gets pumped during the irrigation process",
        metavar="V",
    )

    args = parser.parse_args()
    if args.volume != None:
        send_cmd = json.dumps({"command": "set pump volume", "volume": args.volume})
        print(f"Set pump volume to {args.volume} litres")
    elif args.start:
        send_cmd = json.dumps({"command": "start"})
        print("start irrigation process")
    elif args.status:
        send_cmd = json.dumps({"command": "status"})
        print("get status of irrigation system")
    else:
        exit(0)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(send_cmd.encode())
        recv_reply = s.recv(1024)
        logging.debug(recv_reply)


if __name__ == "__main__":
    main()
