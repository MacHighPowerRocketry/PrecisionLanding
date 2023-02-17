# PrecisionLanding

# Outline:

Servo.py: 
Code for running servo moters, to be given data from other class

Sensor.py:
Code for receviing sensor data, to send to main run

rocketLogger.py
Log sensor and debug data to file, in /logs

run.py
Controller class, grabs sensor data from sensor.py, sends to both datalogger.py (to log to file) and to an algogrythm to determine servo action, which sends data to servo.py

Setup:

1. Clone the repo both on your local machine and the rocket's raspberry pi. 
2. Run pip install -r requirements.txt
3. On the raspberry pi, enable SSH and GPIO On the raspberry pi.
4. run Autorun/setup_autorunner.sh to allow the code to run on boot

