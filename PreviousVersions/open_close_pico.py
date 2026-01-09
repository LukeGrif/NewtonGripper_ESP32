from machine import Pin, PWM
import utime

pwm = PWM(Pin(9))
pwm.freq(50)

def set_us(us):
    pwm.duty_ns(us * 1000)   # microseconds -> nanoseconds

print("Neutral")
set_us(1500)
utime.sleep(2)

print("Open (1900us)")
set_us(1900)
utime.sleep(2)

print("Neutral")
set_us(1500)
utime.sleep(2)

print("Close (1100us)")
set_us(1100)
utime.sleep(2)

print("Neutral")
set_us(1500)

