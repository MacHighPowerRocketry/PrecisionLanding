# define BMP388 Device I2C address

I2C_ADD_BMP388_AD0_LOW = 0x76
I2C_ADD_BMP388_AD0_HIGH = 0x77
I2C_ADD_BMP388 = I2C_ADD_BMP388_AD0_HIGH

BMP388_REG_ADD_WIA = 0x00
BMP388_REG_VAL_WIA = 0x50

BMP388_REG_ADD_ERR = 0x02
BMP388_REG_VAL_FATAL_ERR = 0x01
BMP388_REG_VAL_CMD_ERR = 0x02
BMP388_REG_VAL_CONF_ERR = 0x04

BMP388_REG_ADD_STATUS = 0x03
BMP388_REG_VAL_CMD_RDY = 0x10
BMP388_REG_VAL_DRDY_PRESS = 0x20
BMP388_REG_VAL_DRDY_TEMP = 0x40

BMP388_REG_ADD_CMD = 0x7E
BMP388_REG_VAL_EXTMODE_EN = 0x34
BMP388_REG_VAL_FIFI_FLUSH = 0xB0
BMP388_REG_VAL_SOFT_RESET = 0xB6

BMP388_REG_ADD_PWR_CTRL = 0x1B
BMP388_REG_VAL_PRESS_EN = 0x01
BMP388_REG_VAL_TEMP_EN = 0x02
BMP388_REG_VAL_NORMAL_MODE = 0x30

BMP388_REG_ADD_PRESS_XLSB = 0x04
BMP388_REG_ADD_PRESS_LSB = 0x05
BMP388_REG_ADD_PRESS_MSB = 0x06
BMP388_REG_ADD_TEMP_XLSB = 0x07
BMP388_REG_ADD_TEMP_LSB = 0x08
BMP388_REG_ADD_TEMP_MSB = 0x09

BMP388_REG_ADD_T1_LSB = 0x31
BMP388_REG_ADD_T1_MSB = 0x32
BMP388_REG_ADD_T2_LSB = 0x33
BMP388_REG_ADD_T2_MSB = 0x34
BMP388_REG_ADD_T3 = 0x35
BMP388_REG_ADD_P1_LSB = 0x36
BMP388_REG_ADD_P1_MSB = 0x37
BMP388_REG_ADD_P2_LSB = 0x38
BMP388_REG_ADD_P2_MSB = 0x39
BMP388_REG_ADD_P3 = 0x3A
BMP388_REG_ADD_P4 = 0x3B
BMP388_REG_ADD_P5_LSB = 0x3C
BMP388_REG_ADD_P5_MSB = 0x3D
BMP388_REG_ADD_P6_LSB = 0x3E
BMP388_REG_ADD_P6_MSB = 0x3F
BMP388_REG_ADD_P7 = 0x40
BMP388_REG_ADD_P8 = 0x41
BMP388_REG_ADD_P9_LSB = 0x42
BMP388_REG_ADD_P9_MSB = 0x43
BMP388_REG_ADD_P10 = 0x44
BMP388_REG_ADD_P11 = 0x45