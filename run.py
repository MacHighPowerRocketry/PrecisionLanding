from Sensors import sensor
from Sensors.berryAccelerometer import *
from Sensors.berryGyroscope import *
from Sensors.berryMagnetometer import *
from Sensors.pressureSensor import *
import rocketLogger

logger = rocketLogger.rocketLogger()
logger.dataLog('AccXangle \t AccYangle \t gyroXangle \t gyroYangle \t gyroZangle \t heading  \n ')

accelerometer = berryAccelerometer(logger)
gyroscope = berryGyroscope(logger)
magnetometer = berryMagnetometer(logger)
tempPressureAltitudeSensor = BMP388()

def manageSensors():
    callSensorLogics()
    logSensorData()

def callSensorLogics():
    #add sensor logic calls here
    accelerometer.applySensorReadLogic()
    gyroscope.applySensorReadLogic()
    magnetometer.applySensorReadLogic(accelerometer.getPitch(), accelerometer.getRoll())
    

def logSensorData():
    temperature,pressure,altitude = bmp388.get_temperature_and_pressure_and_altitude()
    logger.dataLog(accelerometer.toString() + 
                gyroscope.toString() + 
                magnetometer.toString +
                tempPressureAltitudeSensor.toString()+
                "/n")
    
    

def main():
    while True:
        manageSensors()

if __name__=="__main__":
    main()
