import network
import socket
import time
from machine import Pin, PWM

# =======================
# WiFi CONFIG (EDIT THESE)
# =======================
SSID = "Luke_iPhone"
PASSWORD = "123456789"

# =======================
# Gripper PWM CONFIG
# =======================
PWM_PIN = 18       # GPIO18
PWM_HZ = 50

OPEN_US  = 1900
CLOSE_US = 1100
STOP_US  = 1500

MOVE_TIME = 2.0    # seconds to run motor/servo
# =======================

# ----- PWM setup -----
pwm = PWM(Pin(PWM_PIN))
pwm.freq(PWM_HZ)

def set_us(us: int):
    # MicroPython PWM on ESP32 supports duty_ns()
    pwm.duty_ns(us * 1000)

def stop():
    set_us(STOP_US)

def open_gripper():
    set_us(OPEN_US)
    time.sleep(MOVE_TIME)
    stop()

def close_gripper():
    set_us(CLOSE_US)
    time.sleep(MOVE_TIME)
    stop()

# Always start neutral
stop()
time.sleep(0.3)

# ----- WiFi connect -----
def connect_wifi(ssid, password, timeout_s=15, retry_delay_s=2):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        return wlan

    print("Connecting to WiFi:", ssid)
    wlan.connect(ssid, password)

    start = time.ticks_ms()
    while not wlan.isconnected():
        if time.ticks_diff(time.ticks_ms(), start) > timeout_s * 1000:
            print("WiFi connection failed (timeout). Retrying...")
            try:
                wlan.disconnect()
            except:
                pass
            time.sleep(retry_delay_s)
            wlan.connect(ssid, password)
            start = time.ticks_ms()
        time.sleep(0.2)

    return wlan

def wait_for_ip(wlan):
    ip = wlan.ifconfig()[0]
    while ip == "0.0.0.0":
        time.sleep(0.2)
        ip = wlan.ifconfig()[0]
    return ip

# ----- HTTP helpers -----
def http_response(body: str):
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n"
        + body
    )

def start_server(port=80):
    addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    return s

# ----- Main loop -----
wlan = None
server = None

while True:
    # Ensure WiFi is connected
    if wlan is None or not wlan.isconnected():
        try:
            wlan = connect_wifi(SSID, PASSWORD)
            ip = wait_for_ip(wlan)
            print("Connected! IP:", ip)

            # (Re)start server after (re)connect
            if server:
                try:
                    server.close()
                except:
                    pass
                server = None

            server = start_server(80)
            print("Listening on http://%s/" % ip)
            print("Endpoints: /open  /close")

        except Exception as e:
            print("WiFi error:", e)
            time.sleep(2)
            continue

    # Handle HTTP requests
    try:
        cl, addr = server.accept()
        try:
            req = cl.recv(1024)
            if not req:
                cl.close()
                continue

            # Parse path from: GET /path HTTP/1.1
            line = req.split(b"\r\n", 1)[0]
            parts = line.split(b" ")
            path = parts[1].decode() if len(parts) > 1 else "/"

            if path.startswith("/open"):
                cl.send(http_response("OPEN for 2 seconds\n"))
                open_gripper()

            elif path.startswith("/close"):
                cl.send(http_response("CLOSE for 2 seconds\n"))
                close_gripper()

            else:
                cl.send(http_response("Use /open or /close\n"))

        finally:
            cl.close()

    except OSError as e:
        # Usually indicates network/socket hiccup; loop will reconnect if needed
        print("Socket error:", e)
        time.sleep(0.5)

