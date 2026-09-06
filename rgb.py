from gpiozero import RGBLED

_led = None


def rgb(red_pin, green_pin, blue_pin):
    global _led
    _led = RGBLED(red=red_pin, green=green_pin, blue=blue_pin)


def color(red, green, blue):
    if _led is None:
        return

    _led.color = (
        red / 255,
        green / 255,
        blue / 255
    )


def off():
    color(0, 0, 0)