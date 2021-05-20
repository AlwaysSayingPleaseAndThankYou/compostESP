import ds18x20
import machine
import micropython as mp
import onewire
from boot import AP
import utime
# the wlan variable should carry over from boot.py

TEMP_READ_PIN = 12
PUMP_PIN = 0

mp.const(TEMP_READ_PIN)
mp.const(PUMP_PIN)

dat = machine.Pin(TEMP_READ_PIN, machine.Pin.IN)
pump_pin = machine.pin(PUMP_PIN, machine.Pin.OUT)

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for temp devices on the bus
roms = ds.scan()
print('found devices:', roms)

def pump(time=10000, state="off"):
    if state == "on" and pump_pin.value()==0:
        pump_pin.value(1)



def checktemp():
    # read each temp 5 times, once per  .5s. return average of these temps.

    tap_temp = []
    tub_temp = []
    temps = [tap_temp, tub_temp]

    ds.convert_temp()

    for i, rom in enumerate(roms):
        for j in range(5):
            temps[i].append(ds.read_temp(rom))
        temps[i] = sum(temps[i])/len(temps[i])
    return temps


def correct_temp_callback():
    # All pins except number 16 can be configured to trigger a hard interrupt if their input changes.
    # You can set code (a callback function) to be executed on the trigger.
    # https: // docs.micropython.org / en / v1.13 / esp8266 / tutorial / pins.html

    # I want to have this callback trigger to shut off the pump
    # I think I can do this just by reading pin value. SOmething about Pin_IRQ?
    pass


def go_to_sleep(sleep_time):
    """
    Function puts the ESP into deep sleep for sleep_time milliseconds
    :param sleep_time: time to spend in deep sleep
    :return: none
    """
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, sleep_time)
    machine.deepsleep()


### RUN TIME BABY ###
SLEEP_TIME = 300000

while True:
    checktemp()
    if AP.isconnected():

    go_to_sleep()
