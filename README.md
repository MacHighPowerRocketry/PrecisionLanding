# PrecisionLanding

# Outline:

Servo.py: 
Code for running servo moters, to be given data from other class

Sensor.py:
Code for receviing sensor data, to send to main run

datalogger.py
Log sensor data to file

run.py
Controller class, grabs sensor data from sensor.py, sends to both datalogger.py (to log to file) and to an algogrythm to determine servo action, which sends data to servo.py
