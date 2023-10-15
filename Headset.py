# I used some ideas for bluetooth enabling from https://forums.raspberrypi.com/viewtopic.php?t=352747
from machine import Pin
import utime, ustruct, bluetooth

# Initialize triggers and echoes for all 6 sensors
trig1 = Pin(1, Pin.OUT)
echo1 = Pin(0, Pin.IN)
trig2 = Pin(3, Pin.OUT)
echo2 = Pin(2, Pin.IN)
trig3 = Pin(5, Pin.OUT)
echo3 = Pin(4, Pin.IN)
trig4 = Pin(7, Pin.OUT)
echo4 = Pin(6, Pin.IN)
trig5 = Pin(9, Pin.OUT)
echo5 = Pin(8, Pin.IN)
trig6 = Pin(11, Pin.OUT)
echo6 = Pin(10, Pin.IN)

# Set up bluetooth
ble = bluetooth.BLE()
ble.active(True)

# Set all triggers low
def trigsLow():
    trig1.low()
    trig2.low()
    trig3.low()
    trig4.low()
    trig5.low()
    trig6.low()
    
# Set all triggers high
def trigsHigh():
    trig1.high()
    trig2.high()
    trig3.high()
    trig4.high()
    trig5.high()
    trig6.high()
    
def calculateDistance(timePassed):
    return (timePassed * 0.0343) / 2

def getReadings():
    
    # Set triggers low and wait 2 microsecs
    trigsLow()
    utime.sleep_us(2)
    # Set triggers high for 5 microseconds and then stop
    trigsHigh()
    utime.sleep_us(5)
    trigsLow()
    
    # Helpful booleans to know if we are done getting data
    got1 = False
    got2 = False
    got3 = False
    got4 = False
    got5 = False
    got6 = False
    done = got1 and got2 and got3 and got4 and got5 and got6
    
    while not done:
        
        # If sensors haven't gotten values yet, record time without signals for each
        if not got1 and echo1.value() == 0:
            signaloff1 = utime.ticks_us()
        if not got2 and echo2.value() == 0:
            signaloff2 = utime.ticks_us()
        if not got3 and echo3.value() == 0:
            signaloff3 = utime.ticks_us()
        if not got4 and echo4.value() == 0:
            signaloff4 = utime.ticks_us()
        if not got5 and echo5.value() == 0:
            signaloff5 = utime.ticks_us()
        if not got6 and echo6.value() == 0:
            signaloff6 = utime.ticks_us()
        
        # Same thing as before but recording time sensors ARE getting data
        if echo1.value == 1:
            got1 = True
            signalon1 = utime.ticks_us()
        if echo2.value == 1:
            got2 = True
            signalon2 = utime.ticks_us()
        if echo3.value == 1:
            got3 = True
            signalon3 = utime.ticks_us()
        if echo4.value == 1:
            got4 = True
            signalon4 = utime.ticks_us()
        if echo5.value == 1:
            got5 = True
            signalon5 = utime.ticks_us()
        if echo6.value == 1:
            got6 = True
            signalon6 = utime.ticks_us()
            
        # Update if we are done
        done = got1 and got2 and got3 and got4 and got5 and got6
            
    # Calculate all distances
    distance1 = calculateDistance(signalon1 - signaloff1)
    distance2 = calculateDistance(signalon2 - signaloff2)
    distance3 = calculateDistance(signalon3 - signaloff3)
    distance4 = calculateDistance(signalon4 - signaloff4)
    distance5 = calculateDistance(signalon5 - signaloff5)
    distance6 = calculateDistance(signalon6 - signaloff6)

    distData = ustruct.pack('<i',distance1, distance2, distance3, distance4, distance5, distance6)
    ble.gap_advertise(int(1e6), adv_data = distData, connectable = False)

while True:
    getReadings()
    utime.sleep(0.1)
