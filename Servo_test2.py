from gpiozero.pins.pigpio import PiGPIOFactory #use this factory for jitter free
from gpiozero import Servo
from time import sleep
 
minPulseWidth=0.5/1000
maxPulseWidth=2.5/1000

servo = Servo(25, min_pulse_width=minPulseWidth, max_pulse_width=maxPulseWidth,pin_factory=PiGPIOFactory())

try:
    while True:      
        print("Set value range -1.0 to +1.0")
        for value in range(0,21):
            sleep(0.1)
            value2=(float(value)-10)/10
            servo.value=value2
            print(value2)

        print("Set value range +1.0 to -1.0")
        for value in range(20,-1,-1):
            value2=(float(value)-10)/10
            servo.value=value2
            print(value2)
            sleep(0.1)
except KeyboardInterrupt:
    print("Program stopped")
