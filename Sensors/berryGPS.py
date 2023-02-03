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

    def checkForCharError(self, gpsLine):
        CharError = 0

        for c in gpsLine:                               # Check #3, Make sure that only readiable ASCII charaters and Carriage Return are seen.
            if (c < 32 or c > 122) and  c != 13:
                CharError+=1

        return CharError == 0

    def checkGPSLine(self, gpsLine):
        """
        basic sanity check on gps line
        make sure '$' doesnt appear twice and 83 is maximun NMEA sentenace length
        """
        return gpsLine.count(36) == 1 and len(gpsLine) < 84
        
    def checkForAllocationError(self, gpsChars):
        return gpsChars.find('txbuf') == -1

    def manualChecksum(self, gpsStr, chkSum):
        # Remove the $ and do a manual checksum on the rest of the NMEA sentence
         # Compare the calculated checksum with the one in the NMEA sentence
        for ch in gpsStr[1:]: 
            chkVal ^= ord(ch)
        return chkVal != int(chkSum, 16)


    
    def parseResponse(self, gpsLine):
        if(not self.checkGPSLine):
            return

        if(not self.checkForCharError()):
            return
        
        gpsChars = ''.join(chr(c) for c in gpsLine)
        if(not self.checkForAllocationError(gpsChars)):
            return

        gpsStr, chkSum = gpsChars.split('*',2)  # Check #5 only split twice to avoid unpack error
        gpsComponents = gpsStr.split(',')
        if(not self.manualChecksum(gpsStr, chkSum)):
            return
            
        self.gpschars = gpsChars

    def handle_ctrl_c(self, signal, frame):
        sys.exit(130)

    def readGPS(self):
        c = None
        response = []
        try:
            c = BUS.read_byte(address)
            if c == 255:
                return False
            elif c == 10:
                self.parseResponse(response)
            else:
                response.append(c)
            self.parseResponse(response)
        except IOError:
            self.connectBus()
        except Exception as err:
            self.logger.debugLog(err)

    def toString(self):
        self.readGPS()
        return self.gpschars

if __name__ == '__main__':
    import rocketLogger
    logger = rocketLogger.rocketLogger()
    gps = berryGPS(logger)
    while True:
        print(gps.toString())
        time.sleep(gpsReadInterval)