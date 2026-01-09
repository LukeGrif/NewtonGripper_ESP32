
import network
import time

# --- EDIT THESE ---
SSID = "Luke_iPhone"
PASSWORD = "123456789"
# ------------------

def connect_wifi(ssid, password, timeout_s=15):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Optional: ensure we're not stuck in an old state
    if wlan.isconnected():
        print("Already connected:", wlan.ifconfig())
        return wlan

    print("Connecting to WiFi:", ssid)
    wlan.connect(ssid, password)

    start = time.ticks_ms()
    while not wlan.isconnected():
        if time.ticks_diff(time.ticks_ms(), start) > timeout_s * 1000:
            raise RuntimeError("WiFi connection failed (timeout). Check SSID/password/signal.")
        time.sleep(0.2)

    print("Connected!")
    print("IP config:", wlan.ifconfig())
    return wlan

try:
    wlan = connect_wifi(SSID, PASSWORD)
except Exception as e:
    print("WiFi error:", e)

