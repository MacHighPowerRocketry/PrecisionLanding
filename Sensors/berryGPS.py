from Sensors.sensor import sensor
from BerryIMU import IMU
import time
import smbus
import signal
import sys
BUS = None
address = 0x42
gpsReadInterval = 0.03

class berryGPS(sensor):

    def __init__(self, logger):
        super().__init__(logger)
        self.logger = logger
        signal.signal(signal.SIGINT, self.handle_ctrl_c)
        self.connectBus()

    def connectBus(self):
        self.bus = smbus.SMBus(1)
    
    def parseResponse(self, gpsLine):
        if(gpsLine.count(36) == 1):                           # Check #1, make sure '$' doesnt appear twice
            if len(gpsLine) < 84:                               # Check #2, 83 is maximun NMEA sentenace length.
                CharError = 0;
                for c in gpsLine:                               # Check #3, Make sure that only readiable ASCII charaters and Carriage Return are seen.
                    if (c < 32 or c > 122) and  c != 13:
                        CharError+=1
                if (CharError == 0):#    Only proceed if there are no errors.
                    gpsChars = ''.join(chr(c) for c in gpsLine)
                    if (gpsChars.find('txbuf') == -1):          # Check #4, skip txbuff allocation error
                        gpsStr, chkSum = gpsChars.split('*',2)  # Check #5 only split twice to avoid unpack error
                        gpsComponents = gpsStr.split(',')
                        chkVal = 0
                        for ch in gpsStr[1:]: # Remove the $ and do a manual checksum on the rest of the NMEA sentence
                            chkVal ^= ord(ch)
                        if (chkVal == int(chkSum, 16)): # Compare the calculated checksum with the one in the NMEA sentence
                            self.gpschars = gpsChars

    def handle_ctrl_c(self, signal, frame):
        sys.exit(130)

    def readGPS(self):
        c = None
        response = []
        try:
            while True: # Newline, or bad char.
                c = BUS.read_byte(address)
                if c == 255:
                    return False
                elif c == 10:
                    break
                else:
                    response.append(c)
            self.parseResponse(response)
        except IOError:
            self.connectBus()
        except Exception as err:
            self.logger.debugLog(err)

    def toString(self):
        self.parseResponse()
        return self.gpschars

if __name__ == '__main__':
    import rocketLogger
    logger = rocketLogger.rocketLogger()
    gps = berryGPS(logger)
    while True:
        print(gps.toString())
        time.sleep(gpsReadInterval)