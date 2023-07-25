import logging
import time
import threading
from gpiozero import LED, DigitalInputDevice, DigitalOutputDevice
import schedule
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from src.level_alarm import Level_alarm
from src.pump_control import Pump_control

pump_out = DigitalOutputDevice(5)
indicator_led__out = LED(6)
level_alarm_in = DigitalInputDevice(4, bounce_time=0.1)

pump_control = Pump_control(pump_out, level_alarm_in, 10)
level_alarm = Level_alarm(level_alarm_in, indicator_led__out, pump_out)
irrigation_time = "20:00"

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Raspberry Pi Irrigation System"),
        # Display pump status
        html.H2("Pump Status:"),
        html.Div(id="pump-status"),
        # Display water tank status
        html.H2("Water Tank Status:"),
        html.Div(id="water-tank-status"),
        # Button to start the pump immediately
        html.Button("Start Pump", id="start-pump-button", n_clicks=0),
        # Button to start the pump immediately
        html.Button("Refresh", id="refresh", n_clicks=0),
        # Input fields for setting the pump schedule
        html.H2("Set Pump Schedule:"),
        # dcc.Input(
        #     id="schedule-time",
        #     type="text",
        #     placeholder="HH:MM",
        # ),
        dcc.Input(
            id="pump-volume",
            type="number",
            placeholder="Pump Volume (litre)",
            value=10,
        ),
        html.Button("Set volume", id="set-volume-button", n_clicks=0),
    ]
)

# Callback to update status of irrigation system
@app.callback(
    Output("pump-status", "children"),
    Output("water-tank-status", "children"),
    Input("refresh", "n_clicks"),
    Input('start-pump-button', 'n_clicks')
)
def update_status(n_clicks_refresh, n_clicks_pump):
    if n_clicks_pump:
        pump_control.irrigation()
    return (
        f"Pump is {'On' if pump_control.status() else 'Off'}.",
        f"Water tank is {'full' if level_alarm.level_status() else 'empty'}",
    )


# # Callback to update status of irrigation system
# @app.callback(
#     Output("pump-status", "children"),
#     Output("water-tank-status", "children"),
#     Input("refresh", "n_clicks"),
# )
# def update_status():
#     return (
#         f"Pump is {'On' if pump_control.status() else 'Off'}.",
#         f"Water tank is {'empty' if level_alarm.level_status() else 'full'}",
#     )


# # Callback to set the pump schedule
# @app.callback(
#     Output("pump-status", "children"),
#     Output("water-tank-status", "children"),
#     Input("set-schedule-button", "n_clicks"),
#     Input("pump-volume", "value"),
# )
# def set_pump_schedule(n_clicks, time, volume):
#     if n_clicks > 0 and time and volume:
#         pump_control.set_pump_volume(volume)
#     return (
#         f"Pump is {'On' if pump_control.status() else 'Off'}.",
#         f"Water tank is {'empty' if level_alarm.level_status() else 'full'}",
#     )


def schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(3600)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    schedule.every().day.at("20:00").do(pump_control.irrigation)

    schedule_thread = threading.Thread(target=schedule_loop, daemon=True)
    schedule_thread.start()
    app.run(debug=True)
