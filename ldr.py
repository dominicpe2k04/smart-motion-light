import time
from gpiozero import OutputDevice, DigitalInputDevice

_pin = None

# Calibration (adjust these if necessary)
_MIN_TIME = 0.0005   # Bright
_MAX_TIME = 0.1000   # Dark


def ldr(pin):
    global _pin
    _pin = pin

def calibrate(min_time, max_time):
    global _MIN_TIME, _MAX_TIME
    _MIN_TIME = min_time
    _MAX_TIME = max_time

def _charge_time():
    # Discharge capacitor
    discharge = OutputDevice(_pin, active_high=True, initial_value=False)
    time.sleep(0.01)
    discharge.close()

    # Measure charging time
    sensor = DigitalInputDevice(_pin)

    start = time.perf_counter()

    while sensor.value == 0:
        if (time.perf_counter() - start) > _MAX_TIME:
            sensor.close()
            return _MAX_TIME

    elapsed = time.perf_counter() - start
    sensor.close()

    return elapsed


def value():
    if _pin is None:
        return None

    t = _charge_time()

    # Normalize to 0.0 - 1.0
    v = 1 - ((t - _MIN_TIME) / (_MAX_TIME - _MIN_TIME))

    if v < 0:
        v = 0

    if v > 1:
        v = 1

    return round(v, 3)


def percent():
    v = value()
    if v is None:
        return None
    return round(v * 100, 1)