# Some inspiration I got for bluetooth is from https://forums.raspberrypi.com/viewtopic.php?t=352747
import bluetooth, ustruct
from micropython import const
from utime import sleep_ms
from machine import Pin

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
serverAddr = bytes(b'(\xcd\xc1\x04a\x1f') # The value inside bytes is the address of the headset Pi

distance1 = 0
distance2 = 0
distance3 = 0
distance4 = 0
distance5 = 0
distance6 = 0

def bt_irq(event, data):
    global receivedNumber, dataReceivedFlag
    if event == _IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, adv_type, rssi, adv_data = data
        address = bytes(addr)
        if address==serverAddr and not dataReceivedFlag:
            distance1, distance2, distance3, distance4, distance5, distance6 = ustruct.unpack('<i',bytes(adv_data))[0]
            dataReceivedFlag = True
    elif event == _IRQ_SCAN_DONE:
        print('scan finished.')
        
ble = bluetooth.BLE()
ble.active(True)
ble.irq(bt_irq)

scanDuration_ms = 100000
interval_us = 15000
window_us = 15000
active = False

dataReceivedFlag = False
ble.gap_scan(scanDuration_ms, interval_us, window_us, active)

distances = [distance1, distance2, distance3, distance4, distance5, distance6]

row1 = Pin(0, Pin.OUT)
row2 = Pin(2, Pin.OUT)
row3 = Pin(10, Pin.OUT)
row4 = Pin(18, Pin.OUT)
row5 = Pin(13, Pin.OUT)

rows = [row1, row2, row3, row4, row5]

col1 = Pin(28, Pin.OUT)
col2 = Pin(27, Pin.OUT)
col3 = Pin(22, Pin.OUT)
col4 = Pin(15, Pin.OUT)
col5 = Pin(8, Pin.OUT)
col6 = Pin(1, Pin.OUT)

cols = [col1, col2, col3, col4, col5, col6]

while True:
    if dataReceivedFlag:
        for i in range(6):
            if distances(i) < 250:
                cols(i) = 1
            else:
                cols(i) = 0
                
            if distances(i) >= 0 and distances(i) < 50:
                rows(0) = 1
            else:
                rows(0) = 0
            if distances(i) >= 50 and distances(i) < 100:
                rows(1) = 1
            else:
                rows(1) = 0
            if distances(i) >= 100 and distances(i) < 150:
                rows(2) = 1
            else:
                rows(2) = 0
            if distances(i) >= 150 and distances(i) < 200:
                rows(3) = 1
            else:
                rows(3) = 0
            if distances(i) >= 200 and distances(i) < 250:
                rows(4) = 1
            else:
                rows(4) = 0
