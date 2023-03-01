from Sensors.sensor import sensor
import time
import smbus
import signal
import sys
address = 0x42
gpsReadInterval = 0.03


class berryGPS(sensor):

    def __init__(self, logger):
        sensor.__init__(self, logger)
        self.logger = logger
        signal.signal(signal.SIGINT, self.handle_ctrl_c)
        self.connectBus()
        self.gpsString = None
        self.bus = None
        self.connectBus()

    def connectBus(self):
        self.bus = smbus.SMBus(1)
        #print(self.bus)

    def handle_ctrl_c(signal, frame):
        sys.exit(130)

    def parseResponse(self, gpsLine):
        #print(gpsLine)
        if (gpsLine.count(36) == 1):
            if len(gpsLine) < 84:
                CharError = 0
                for c in gpsLine:
                    if (c < 32 or c > 122) and c != 13:
                        CharError += 1
                if (CharError == 0):
                    gpsChars = ''.join(chr(c) for c in gpsLine)
                    if (gpsChars.find('txbuf') == -1):
                        gpsStr, chkSum = gpsChars.split('*', 2)
                        gpsComponents = gpsStr.split(',')
                        chkVal = 0
                        for ch in gpsStr[1:]:
                            chkVal ^= ord(ch)
                        if (chkVal == int(chkSum, 16)):
                            self.gpsString += "\n" +  gpsChars

    def readGPS(self):
        c = None
        response = []
        #print(self.bus)
        try:
            while True:
                c = self.bus.read_byte(0x42)
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
	self.gpsString = ""
        for i in range(8):
           self.readGPS()
        return self.gpsString


if __name__ == '__main__':
    import rocketLogger
    logger = rocketLogger.rocketLogger()
    gps = berryGPS(logger)
    while True:
        print(gps.toString())
        time.sleep(gpsReadInterval)
