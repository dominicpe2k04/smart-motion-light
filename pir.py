from gpiozero import MotionSensor

_pir = None


def pir(pin):
    global _pir
    _pir = MotionSensor(pin)


def motion():
    if _pir is None:
        return False

    return _pir.motion_detected


def wait_for_motion():
    if _pir is None:
        return

    _pir.wait_for_motion()


def wait_for_no_motion():
    if _pir is None:
        return

    _pir.wait_for_no_motion()


def close():
    if _pir is not None:
        _pir.close()