from machine import Pin, I2C
import time

# TCS34725 I2C-Adresse
TCS34725_ADDRESS = 0x29

# TCS34725 Register
COMMAND_BIT = 0x80
ENABLE_REGISTER = 0x00
ATIME_REGISTER = 0x01
CONTROL_REGISTER = 0x0F
CDATAL_REGISTER = 0x14

ENABLE_POWER_ON = 0x01
ENABLE_RGBC = 0x02
GAIN_4X = 0x01

# I2C Setup für ESP32 (SDA: GPIO21, SCL: GPIO22)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

def write_register(register, value):
    i2c.writeto_mem(TCS34725_ADDRESS, COMMAND_BIT | register, bytes([value]))

def read_register(register, num_bytes):
    return i2c.readfrom_mem(TCS34725_ADDRESS, COMMAND_BIT | register, num_bytes)

def init_tcs34725():
    write_register(ENABLE_REGISTER, ENABLE_POWER_ON)
    time.sleep(0.003)
    write_register(ENABLE_REGISTER, ENABLE_POWER_ON | ENABLE_RGBC)
    write_register(ATIME_REGISTER, 0xEB)  # 700ms Integration Time
    write_register(CONTROL_REGISTER, GAIN_4X)  # 4x Gain

def read_rgbc():
    data = read_register(CDATAL_REGISTER, 8)
    
    clear = data[1] << 8 | data[0]
    red = data[3] << 8 | data[2]
    green = data[5] << 8 | data[4]
    blue = data[7] << 8 | data[6]
    
    return red, green, blue, clear

def main():
    init_tcs34725()
    
    while True:
        red, green, blue, clear = read_rgbc()
        print(f"Rot: {red}, Grün: {green}, Blau: {blue}, Clear: {clear}")
        time.sleep(1)

if __name__ == "__main__":
    main()
