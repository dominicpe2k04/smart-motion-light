````markdown
# Raspberry Pi 5 Smart Motion Night Light

A smart automated night light built using a **Raspberry Pi 5**, **Python**, and **GPIO Zero**. The system detects human motion using a PIR sensor, measures ambient light using an LDR with an RC timing circuit, and automatically controls an RGB LED.

The LED turns on only when **motion is detected AND the room is dark**, and automatically turns off after a configurable timeout.

---

# Features

- PIR Motion Detection
- Ambient Light Detection using RC-Timing LDR
- Motion + Darkness Based LED Automation
- RGB LED Warm White Night Light
- Configurable Darkness Threshold
- Automatic LED Timeout
- Timestamped Event Logging
- Modular Sensor Libraries
- Raspberry Pi 5 GPIO Control
- Clean GPIO Shutdown
- Python Virtual Environment Support

---

# Hardware Requirements

| Component | Quantity |
|------------|----------|
| Raspberry Pi 5 | 1 |
| HC-SR501 PIR Motion Sensor | 1 |
| LDR / Photoresistor | 1 |
| 1µF Capacitor | 1 |
| Common-Cathode RGB LED | 1 |
| 220Ω Resistors | 3 |
| Breadboard | 1 |
| Jumper Wires | Several |

---

# GPIO Connections

## HC-SR501 PIR Motion Sensor

| PIR Pin | Raspberry Pi 5 |
|---------|----------------|
| VCC | 5V |
| OUT | GPIO4 |
| GND | GND |

Physical pin connections:

```text
HC-SR501 VCC  → Pin 2  (5V)
HC-SR501 OUT  → Pin 7  (GPIO4)
HC-SR501 GND  → Pin 9  (GND)
````

### PIR Configuration

* Sensitivity: approximately 50%
* Time Delay: approximately 5 seconds
* Jumper: H / Repeatable Trigger
* Warm-up time: 30–60 seconds after power-on

---

# LDR (RC Timing Circuit)

The Raspberry Pi 5 does not provide a conventional analog input, so the LDR is measured using an RC timing circuit.

```text
                 LDR
3.3V Pin 1 ─────/\/\/\─────┬──── GPIO18 Pin 12
                           │
                         1µF
                       Capacitor
                           │
                           └──── GND Pin 14
```

Connections:

| LDR / Capacitor | Raspberry Pi 5 |
| --------------- | -------------- |
| LDR Leg 1       | 3.3V           |
| LDR Leg 2       | GPIO18         |
| Capacitor Leg 1 | GPIO18         |
| Capacitor Leg 2 | GND            |

The LDR reading is normalized between:

```text
0.0 → Dark
1.0 → Bright
```

---

# RGB LED

The project uses a **common-cathode RGB LED**.

Each LED channel must use a **220Ω series resistor**.

| RGB LED        | Resistor | Raspberry Pi GPIO | Physical Pin |
| -------------- | -------- | ----------------: | -----------: |
| Red            | 220Ω     |            GPIO17 |       Pin 11 |
| Green          | 220Ω     |            GPIO27 |       Pin 13 |
| Blue           | 220Ω     |            GPIO22 |       Pin 15 |
| Common Cathode | —        |               GND |        Pin 6 |

Connection:

```text
GPIO17 ── 220Ω ── RED
GPIO27 ── 220Ω ── GREEN
GPIO22 ── 220Ω ── BLUE

Common Cathode ───── GND
```

---

# GPIO Summary

| Function                 |   GPIO | Physical Pin |
| ------------------------ | -----: | -----------: |
| PIR Motion               |  GPIO4 |        Pin 7 |
| RGB Red                  | GPIO17 |       Pin 11 |
| RGB Green                | GPIO27 |       Pin 13 |
| RGB Blue                 | GPIO22 |       Pin 15 |
| LDR + Capacitor Junction | GPIO18 |       Pin 12 |

---

# Directory Structure

```text
smart_motion/
├── pir.py
├── ldr.py
├── rgb.py
├── step1.py
├── step2.py
├── step3.py
├── step4.py
├── step5.py
├── ldr_test.py
├── nightlight.log
├── venv/
└── README.md
```

---

# Software Requirements

* Raspberry Pi 5
* Raspberry Pi OS
* Python 3
* GPIO Zero
* lgpio
* Python virtual environment

No external sensor libraries are required.

---

# Installation

## Update System

```bash
sudo apt update
sudo apt upgrade -y
```

## Install GPIO Zero and GPIO Backend

```bash
sudo apt install python3-gpiozero python3-lgpio python3-venv
```

The project uses the Raspberry Pi OS system GPIO libraries rather than installing the GPIO backend through pip.

---

# Create Virtual Environment

```bash
python3 -m venv --system-site-packages venv
```

Activate it:

```bash
source venv/bin/activate
```

Verify GPIO Zero and lgpio:

```bash
python -c "import gpiozero, lgpio; print('GPIO OK')"
```

Expected output:

```text
GPIO OK
```

---

# Custom Sensor Libraries

## PIR Library

`pir.py` provides:

* PIR initialization
* Motion detection
* Wait for motion
* Wait for no motion
* GPIO cleanup

Example:

```python
import pir

pir.pir(4)

if pir.motion():
    print("Motion detected")
```

---

## LDR Library

`ldr.py` provides:

* LDR initialization
* RC charge-time measurement
* Light value from 0.0 to 1.0
* Light percentage
* Calibration support

Example:

```python
import ldr

ldr.ldr(18)

light = ldr.value()

print(light)
```

---

## RGB Library

`rgb.py` provides:

* RGB LED initialization
* RGB color control
* LED OFF control

Example:

```python
import rgb

rgb.rgb(17, 27, 22)

rgb.color(255, 179, 77)
```

---

# Project Stages

## Step 1 — PIR Test

Tests the HC-SR501 independently.

Run:

```bash
python step1.py
```

Expected behavior:

```text
Motion detected!
No motion.
```

---

## Step 2 — LDR Test

Tests the LDR and RC timing circuit.

Run:

```bash
python step2.py
```

The LDR should produce values between:

```text
0.0 → Dark
1.0 → Bright
```

Cover the LDR with your hand and observe the reading.

Then shine a light on the LDR and observe the reading increase.

---

# LDR Calibration

Measure the LDR under the actual room conditions.

Example:

```text
Normal room light → 0.80
Dark room         → 0.15
```

The darkness threshold should be selected between the measured bright and dark values.

Default starting value:

```python
DARK_THRESHOLD = 0.4
```

Adjust this value according to the actual LDR readings.

---

# Step 3 — Motion-Only Night Light

Run:

```bash
python step3.py
```

At this stage the LDR is ignored.

Behavior:

```text
Motion detected → RGB LED ON
No motion       → RGB LED OFF
```

Warm white:

```python
WARM_WHITE = (255, 179, 77)
```

---

# Step 4 — True Night Light

Run:

```bash
python step4.py
```

The LED turns on only when both conditions are true:

```text
Motion detected
       AND
Room is dark
       ↓
   LED ON
```

Logic:

```python
if motion_detected and light_value < DARK_THRESHOLD:
    rgb.color(255, 179, 77)
else:
    rgb.off()
```

Expected behavior:

| Motion | Room   | LED |
| ------ | ------ | --- |
| No     | Bright | OFF |
| Yes    | Bright | OFF |
| No     | Dark   | OFF |
| Yes    | Dark   | ON  |

---

# Step 5 — Final Smart Motion Night Light

Run:

```bash
python step5.py
```

The final version adds:

* Darkness detection
* Motion detection
* Warm-white RGB LED
* Automatic timeout
* Event logging

Default timeout:

```python
ON_TIMEOUT = 15
```

After the last valid motion event, the LED remains on for approximately 15 seconds and then turns off.

---

# Event Logging

The final program records events in:

```text
nightlight.log
```

View the log:

```bash
cat nightlight.log
```

Example:

```text
2026-09-06 19:30:10  System ready
2026-09-06 19:30:25  Motion + Dark -> LED ON
2026-09-06 19:30:40  Timeout -> LED OFF
```

---

# Running the Project

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the required stage:

```bash
python step1.py
```

```bash
python step2.py
```

```bash
python step3.py
```

```bash
python step4.py
```

```bash
python step5.py
```

---

# System Operation

```text
                ┌──────────────┐
                │  HC-SR501    │
                │ PIR Sensor   │
                └──────┬───────┘
                       │
                       ▼
                Motion Detected?
                       │
                       │
                ┌──────▼───────┐
                │ Raspberry Pi │
                │      5       │
                └──────┬───────┘
                       ▲
                       │
                ┌──────┴───────┐
                │     LDR      │
                │ Light Sensor │
                └──────────────┘
                       │
                       ▼
                 Room Dark?
                       │
                       ▼
             Motion AND Darkness
                       │
                       ▼
                ┌──────────────┐
                │   RGB LED    │
                │  Warm White  │
                └──────────────┘
                       │
                       ▼
                 15s Timeout
                       │
                       ▼
                    LED OFF
```

---

# Verification Checklist

Before considering the project complete:

* [ ] PIR detects motion reliably
* [ ] LDR changes value between bright and dark
* [ ] RGB LED produces warm white
* [ ] Step 3 works with motion regardless of light level
* [ ] Step 4 requires both motion and darkness
* [ ] Step 5 automatically turns the LED off after the timeout
* [ ] `nightlight.log` records system events
* [ ] Ctrl+C turns the LED off
* [ ] GPIO resources are properly released

---

# Troubleshooting

## PIR triggers continuously

Possible causes:

* PIR still warming up
* Sensitivity too high
* PIR jumper configuration

Check:

```text
Jumper → H
Sensitivity → approximately 50%
```

Allow 30–60 seconds after powering the PIR.

---

## PIR does not detect motion

Check:

```text
VCC → 5V
OUT → GPIO4
GND → GND
```

Also make sure the sensor has completed its warm-up period.

---

## LDR value does not change

Check:

* LDR wiring
* GPIO18 connection
* 1µF capacitor connection
* 3.3V connection
* GND connection

The junction must be:

```text
LDR + Capacitor + GPIO18
```

---

## LED does not turn on

Check:

```text
GPIO17 → Red
GPIO27 → Green
GPIO22 → Blue
```

Make sure each channel has a **220Ω resistor**.

Also verify that the RGB LED is **common cathode**.

---

## LED stays OFF in darkness

Check the LDR value:

```bash
python step2.py
```

Then adjust:

```python
DARK_THRESHOLD = 0.4
```

according to your actual LDR calibration.

---

## LED flickers around the threshold

The LDR value may be fluctuating around the darkness threshold.

For example:

```text
0.399
0.401
0.398
0.402
```

This can cause the LED to repeatedly switch states.

A future improvement is to add **hysteresis** using separate ON and OFF thresholds.

---

# Project Architecture

The project uses three reusable hardware libraries:

```text
pir.py
    ↓
HC-SR501 PIR

ldr.py
    ↓
LDR + RC Timing Circuit

rgb.py
    ↓
RGB LED
```

The project stages progressively combine these libraries:

```text
Step 1
PIR

Step 2
LDR

Step 3
PIR + RGB

Step 4
PIR + LDR + RGB

Step 5
PIR + LDR + RGB
       +
Timeout + Logging
```

---

# Author

**Dominic**

GitHub: [https://github.com/dominicpe2k04](https://github.com/dominicpe2k04)

Email: [dominicpe2k04@gmail.com](mailto:dominicpe2k04@gmail.com)

---

Built using **Raspberry Pi 5**, **Python**, **GPIO Zero**, **lgpio**, and custom modular sensor libraries.

```
```
