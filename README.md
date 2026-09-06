# Raspberry Pi 5 Smart Motion Night Light

A smart automated night light built using a **Raspberry Pi 5**, **Python**, and **GPIO Zero**. The system detects human motion using an HC-SR501 PIR sensor, measures ambient light using an LDR with an RC timing circuit, and automatically controls a common-cathode RGB LED.

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

### Physical Pin Connections

```text
HC-SR501 VCC  → Raspberry Pi Pin 2  (5V)
HC-SR501 OUT  → Raspberry Pi Pin 7  (GPIO4)
HC-SR501 GND  → Raspberry Pi Pin 9  (GND)
```

### PIR Configuration

Recommended HC-SR501 settings:

```text
Sensitivity  → Approximately 50%
Time Delay   → Approximately 5 seconds
Jumper       → H / Repeatable Trigger
Warm-up      → 30–60 seconds after power-on
```

The PIR requires a warm-up period after power-on before motion readings become reliable.

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

### Connections

| LDR / Capacitor | Raspberry Pi 5 |
|-----------------|----------------|
| LDR Leg 1 | 3.3V |
| LDR Leg 2 | GPIO18 |
| Capacitor Leg 1 | GPIO18 |
| Capacitor Leg 2 | GND |

The LDR library normalizes the measured light level between:

```text
0.0 → Dark
1.0 → Bright
```

---

# RGB LED

The project uses a **common-cathode RGB LED**.

Each LED color channel uses a **220Ω series resistor**.

| RGB LED Pin | Resistor | Raspberry Pi GPIO | Physical Pin |
|-------------|----------|------------------:|-------------:|
| Red Anode | 220Ω | GPIO17 | Pin 11 |
| Green Anode | 220Ω | GPIO27 | Pin 13 |
| Blue Anode | 220Ω | GPIO22 | Pin 15 |
| Common Cathode | — | GND | Pin 6 |

### Connection

```text
GPIO17 ── 220Ω ── RED
GPIO27 ── 220Ω ── GREEN
GPIO22 ── 220Ω ── BLUE

Common Cathode ───── GND
```

---

# Complete GPIO Summary

| Function | GPIO | Physical Pin |
|----------|-----:|-------------:|
| PIR Motion Sensor | GPIO4 | Pin 7 |
| RGB Red | GPIO17 | Pin 11 |
| RGB Green | GPIO27 | Pin 13 |
| RGB Blue | GPIO22 | Pin 15 |
| LDR + Capacitor Junction | GPIO18 | Pin 12 |
| PIR VCC | 5V | Pin 2 |
| LDR VCC | 3.3V | Pin 1 |
| RGB Common Cathode | GND | Pin 6 |
| PIR GND | GND | Pin 9 |
| LDR Capacitor GND | GND | Pin 14 |

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

- Raspberry Pi 5
- Raspberry Pi OS
- Python 3
- GPIO Zero
- lgpio
- Python virtual environment

The project uses custom modular Python libraries for the PIR, LDR, and RGB LED.

---

# Installation

## Update System

```bash
sudo apt update
sudo apt upgrade -y
```

---

# Install GPIO Zero and GPIO Backend

Install the Raspberry Pi OS system packages:

```bash
sudo apt install python3-gpiozero python3-lgpio python3-venv
```

The project uses the system-installed GPIO libraries rather than installing the GPIO backend through pip.

---

# Create Virtual Environment

Create the virtual environment with access to system packages:

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

# Custom Libraries

## PIR Library

The project uses a custom `pir.py` library.

It provides:

- PIR initialization
- Motion detection
- Wait for motion
- Wait for no motion
- GPIO cleanup

Example:

```python
import pir

pir.pir(4)

if pir.motion():
    print("Motion detected")
```

---

# LDR Library

The project uses a custom `ldr.py` library for RC-timing light measurement.

It provides:

- LDR initialization
- RC charge-time measurement
- Light value from 0.0 to 1.0
- Light percentage
- Calibration support

Example:

```python
import ldr

ldr.ldr(18)

light = ldr.value()

print(light)
```

---

# RGB Library

The project uses a custom `rgb.py` library.

It provides:

- RGB LED initialization
- RGB color control
- LED OFF control

Example:

```python
import rgb

rgb.rgb(17, 27, 22)

rgb.color(255, 179, 77)
```

---

# Project Stages

The project is divided into five stages.

---

# Step 1 — PIR Test

Step 1 tests the HC-SR501 PIR independently.

Run:

```bash
python step1.py
```

The PIR is given time to warm up before testing.

Expected behavior:

```text
Motion detected!
No motion.
```

Move your hand in front of the PIR and verify that motion is detected.

---

# Step 2 — LDR Test

Step 2 tests the LDR and RC timing circuit.

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

The LDR threshold should be calibrated according to the actual environment.

Record the LDR value in normal room lighting and in darkness.

Example:

```text
Normal room light → 0.80
Dark room         → 0.15
```

A suitable darkness threshold can then be selected between the measured bright and dark values.

The starting threshold is:

```python
DARK_THRESHOLD = 0.4
```

This value should be adjusted according to the actual readings from the LDR.

---

# Step 3 — Motion-Only Night Light

Step 3 combines the PIR sensor and RGB LED.

The LDR is ignored at this stage.

Run:

```bash
python step3.py
```

Behavior:

```text
Motion detected → RGB LED ON
No motion       → RGB LED OFF
```

The RGB LED uses a warm-white color:

```python
WARM_WHITE = (255, 179, 77)
```

---

# Step 4 — True Night Light

Step 4 combines the PIR, LDR, and RGB LED.

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

The logic is:

```python
if motion_detected and light_value < DARK_THRESHOLD:
    rgb.color(255, 179, 77)
else:
    rgb.off()
```

### Expected Behavior

| Motion | Room Condition | LED |
|--------|-----------------|-----|
| No | Bright | OFF |
| Yes | Bright | OFF |
| No | Dark | OFF |
| Yes | Dark | ON |

---

# Step 5 — Final Smart Motion Night Light

Step 5 is the final version of the project.

Run:

```bash
python step5.py
```

The final version includes:

- PIR motion detection
- LDR light detection
- Darkness threshold
- RGB warm-white output
- Automatic LED timeout
- Event logging

### Timeout

The default timeout is:

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

View the log using:

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

Run Step 1:

```bash
python step1.py
```

Run Step 2:

```bash
python step2.py
```

Run Step 3:

```bash
python step3.py
```

Run Step 4:

```bash
python step4.py
```

Run Step 5:

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

# Verification Checklist

Before considering the project complete:

- [ ] PIR detects motion reliably
- [ ] LDR changes value between bright and dark
- [ ] RGB LED produces warm white
- [ ] Step 3 works with motion regardless of light level
- [ ] Step 4 requires both motion and darkness
- [ ] Step 5 automatically turns the LED off after the timeout
- [ ] `nightlight.log` records system events
- [ ] Ctrl+C turns the LED off
- [ ] GPIO resources are properly released

---

# Troubleshooting

## PIR Triggers Continuously

Possible causes:

- PIR is still warming up
- Sensitivity is too high
- Incorrect jumper configuration

Check:

```text
Jumper     → H
Sensitivity → Approximately 50%
```

Allow 30–60 seconds after powering the PIR.

---

## PIR Does Not Detect Motion

Check:

```text
VCC → 5V
OUT → GPIO4
GND → GND
```

Also make sure the sensor has completed its warm-up period.

---

## LDR Value Does Not Change

Check:

- LDR wiring
- GPIO18 connection
- 1µF capacitor connection
- 3.3V connection
- GND connection

The junction must connect:

```text
LDR + Capacitor + GPIO18
```

---

## LED Does Not Turn On

Check:

```text
GPIO17 → Red
GPIO27 → Green
GPIO22 → Blue
```

Make sure each channel has a **220Ω resistor**.

Also verify that the RGB LED is **common cathode**.

---

## LED Stays OFF in Darkness

Check the LDR value:

```bash
python step2.py
```

Then adjust:

```python
DARK_THRESHOLD = 0.4
```

according to the actual LDR calibration.

---

## LED Flickers Around the Threshold

The LDR value may be fluctuating around the darkness threshold.

For example:

```text
0.399
0.401
0.398
0.402
```

This can cause the LED to repeatedly switch states.

A possible future improvement is to add **hysteresis** using separate ON and OFF thresholds.

---

# Project Deliverables

The completed project should include:

## Photos

- Full Raspberry Pi + breadboard setup
- PIR sensor close-up showing trimpots and jumper
- LDR + capacitor circuit close-up
- LED OFF in a lit room with no motion
- LED ON in a dark room with motion
- Thonny screenshot showing the final Step 5 code

## Video

A 90–180 second demonstration showing:

- Motion-only mode
- Night-light behavior
- Bright-room test
- Dark-room + motion test
- Automatic timeout
- Terminal/log output

## Written Notes

Include:

- Total build time
- Actual `DARK_THRESHOLD`
- LDR calibration values
- Room conditions during calibration
- Any deviations from the build specification
- Problems encountered and solutions
- Suggestions for simplifying the project for a 9-year-old
- Hardest concept
- Any improvements or experiments

## Code

Include:

- `pir.py`
- `ldr.py`
- `rgb.py`
- `step1.py`
- `step2.py`
- `step3.py`
- `step4.py`
- `step5.py`
- Any experimental code
- A sample `nightlight.log` containing at least 5 minutes of operation

---

# Author

**Dominic**

GitHub: https://github.com/dominicpe2k04

Email: dominicpe2k04@gmail.com

---

Built using **Raspberry Pi 5**, **Python**, **GPIO Zero**, **lgpio**, and custom modular sensor libraries.
