import sensor
import berryAccelerometer
import rocketLogger

logger = rocketLogger()
logger.dataLog('AccXangle \t AccYangle \t gyroXangle \t gyroYangle \t gyroZangle  \n')


def manageSensors()
    callSensorLogics()
    logSensorData()

def callSensorLogics():
    #add sensor logic calls here
    berryAccelerometer.applySensorReadLogic()

def logSensorData():
    logger.dataLog(berryAccelerometer.getSensorData()[0] + 
                " " + berryAccelerometer.getSensorData()[1] + 
                "/N")
    

def main():
    initalizeLogger()
    while True:
        manageSensors()

if __name__=="__main__":
    main()