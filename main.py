import time
from datetime import datetime

import pir
import ldr
import rgb


# Initialize devices
pir.pir(4)
ldr.ldr(18)
rgb.rgb(17, 27, 22)


# Settings
WARM_WHITE = (255, 179, 77)
DARK_THRESHOLD = 0.4
ON_TIMEOUT = 15


# Store the time of the most recent motion
last_motion_time = 0


def log(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("nightlight.log", "a") as file:
        file.write(f"{timestamp}  {event}\n")

    print(f"{timestamp}  {event}")


print("Warming up PIR...")
time.sleep(30)

log("System ready")


try:
    while True:

        motion_detected = pir.motion()
        light_value = ldr.value()

        is_dark = light_value < DARK_THRESHOLD

        if motion_detected and is_dark:

            last_motion_time = time.time()

            rgb.color(*WARM_WHITE)

            print(f"Motion + Dark -> LED ON | Light: {light_value}")

        elif time.time() - last_motion_time > ON_TIMEOUT:

            rgb.off()

        time.sleep(0.1)


except KeyboardInterrupt:
    print("\nStopping...")


finally:
    rgb.off()
    pir.close()

    log("System stopped")