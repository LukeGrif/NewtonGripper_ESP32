# ESP32 Gripper Control (MicroPython)

This project runs on an **ESP32 using MicroPython** and exposes a simple **HTTP server** to control a gripper (or servo / ESC) over Wi-Fi.

On boot, the ESP32:
1. Connects to Wi-Fi
2. Starts an HTTP server
3. Listens for `/open` and `/close` commands

---

## Features
- Automatic Wi-Fi connection on boot
- Simple HTTP control interface
- PWM-based gripper / servo control
- Safe neutral PWM state on startup
- Recovers automatically from Wi-Fi drops

---

## Hardware
- ESP32
- Gripper / servo / ESC connected to **GPIO 18**
- External power supply for the motor / gripper (recommended)

---

## Setup

### 1. Flash MicroPython
Ensure MicroPython is installed on the ESP32.

### 2. Configure Wi-Fi
Edit the following in `main.py`:

```python
SSID = "YOUR_WIFI_NAME"
PASSWORD = "YOUR_WIFI_PASSWORD"
3. Upload Code
Copy main.py to the ESP32 using a tool such as:

mpremote

Thonny

rshell

The script will run automatically on boot.

Usage
After boot, the ESP32 prints its IP address to the serial console.

Open a browser or use curl:

Open gripper
perl
Copy code
http://<ESP32-IP>/open
Close gripper
perl
Copy code
http://<ESP32-IP>/close
Each command runs the motor for 2 seconds, then returns to a neutral PWM state.

PWM Configuration
PWM behaviour can be adjusted in main.py:

python
Copy code
OPEN_US   = 1900
CLOSE_US  = 1100
STOP_US   = 1500
MOVE_TIME = 2.0
Tune these values to suit your specific gripper, servo, or motor controller.

Notes
HTTP server runs on port 80

Ensure GPIO 18 supports PWM on your ESP32 variant

Do not power motors directly from the ESP32 3.3 V rail

Use a common ground between ESP32 and motor driver

Endpoints Summary
Endpoint	Action
/open	Opens gripper
/close	Closes gripper