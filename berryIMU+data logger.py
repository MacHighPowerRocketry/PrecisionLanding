#       Feel free to do whatever you like with this code.
#       Distributed as-is; no warranty is given.
#
#       https://ozzmaker.com/berryimu/

#       Modified by Chloe Zheng based on berryIMU-simple.py
#       This test:
#           * Get usable angles using a Complementary filter
#           * Save data to a txt file
#           * Run for 10(total_time) seconds, record data each 0.5(updaterate) second


import time
import math
from BerryIMU import IMU
import datetime
import os
import sys
import rocketLogger

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

updaterate = 0.5 #in seconds
current_time = 0 # record time, only for testing purpose
total_time = 10

################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values
# Calibrating the compass isnt mandatory, however a calibrated
# compass will result in a more accurate heading values.

magXmin =  0
magYmin =  0
magZmin =  0
magXmax =  0
magYmax =  0
magZmax =  0



'''
Here is an example:
magXmin =  -1748
magYmin =  -1025
magZmin =  -1876
magXmax =  959
magYmax =  1651
magZmax =  708
Dont use the above values, these are just an example.
'''
############### END Calibration offsets #################



gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0


IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass


a = datetime.datetime.now()


#Initial logging setup, temporarily here before refactor to main logic
"""
f = open("Acc+Gyro data.txt", "w+")
f.write('AccXangle \t AccYangle \t gyroXangle \t gyroYangle \t gyroZangle  \n')
f.close()
"""
logger = rocketLogger()
logger.dataLog('AccXangle \t AccYangle \t gyroXangle \t gyroYangle \t gyroZangle  \n')


while True and current_time <= total_time:
    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()

    #Apply compass calibration
    MAGx -= (magXmin + magXmax) /2
    MAGy -= (magYmin + magYmax) /2
    MAGz -= (magZmin + magZmax) /2

    ##Calculate loop Period(LP). How long between Gyro Reads
    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds/(1000000*1.0)
    #outputString = "Loop Time %5.2f " % ( LP )


    #Convert Gyro raw to degrees per second
    rate_gyr_x =  GYRx * G_GAIN
    rate_gyr_y =  GYRy * G_GAIN
    rate_gyr_z =  GYRz * G_GAIN


    #Calculate the angles from the gyro.
    gyroXangle+=rate_gyr_x*LP
    gyroYangle+=rate_gyr_y*LP
    gyroZangle+=rate_gyr_z*LP


    #Convert Accelerometer values to degrees
    AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
    AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

    #convert the values to -180 and +180
    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0



    #Complementary filter used to combine the accelerometer and gyro values.
    CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
    CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle



    #Calculate heading
    heading = 180 * math.atan2(MAGy,MAGx)/M_PI

    #Only have our heading between 0 and 360
    if heading < 0:
        heading += 360

    ####################################################################
    ###################Tilt compensated heading#########################
    ####################################################################
    #Normalize accelerometer raw values.
    accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
    accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


    #Calculate pitch and roll
    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm/math.cos(pitch))


    #Calculate the new tilt compensated values
    #The compass and accelerometer are orientated differently on the the BerryIMUv1, v2 and v3.
    #This needs to be taken into consideration when performing the calculations

    #X compensation
    if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2MDL)
        magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
    else:                                                                #LSM9DS1
        magXcomp = MAGx*math.cos(pitch)-MAGz*math.sin(pitch)

    #Y compensation
    if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2MDL)
        magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)
    else:                                                                #LSM9DS1
        magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)+MAGz*math.sin(roll)*math.cos(pitch)




    #Calculate tilt compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

    if tiltCompensatedHeading < 0:
        tiltCompensatedHeading += 360


    ##################### END Tilt Compensation ########################


    if 1:                       #Change to '0' to stop showing the angles from the accelerometer
        outputString = "  %5.2f\t\t%5.2f" % (AccXangle, AccYangle)

    if 1:                       #Change to '0' to stop  showing the angles from the gyro
        outputString +="\t\t%5.2f\t\t%5.2f\t\t%5.2f\t\t" % (gyroXangle,gyroYangle,gyroZangle)

    if 0:                       #Change to '0' to stop  showing the angles from the complementary filter
        outputString +=" %5.2f    %5.2f  " % (CFangleX,CFangleY)

    if 0:                       #Change to '0' to stop  showing the heading
        outputString +=" %5.2f    %5.2f " % (heading,tiltCompensatedHeading)


    ##################### Write data to file ########################

    """
    f = open("Acc+Gyro data.txt", "a")
    f.write(outputString)
    f.write("\n")
    f.close()
    print(outputString)
    """
    logger.dataLog(outputString + "\n")

    current_time += updaterate

    #slow program down a bit, makes the output more readable
    time.sleep(updaterate)
