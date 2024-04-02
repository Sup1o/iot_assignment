import time
import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    commPort = "None"
    for port in ports:
        if "USB" in str(port):
            splitPort = str(port).split(" ")
            commPort = splitPort[0]
    return commPort

portName = getPort()
print(portName)

try:
    ser = serial.Serial(port=portName, baudrate=115200)
    print("Opened successfully")
except Exception as e:
    print("Failed to open the port:", e)

relay1_ON  = [0, 6, 0, 0, 0, 255, 200, 91]
relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]

def setDevice1(state):
    try:
        if state:
            ser.write(relay1_ON)
        else:
            ser.write(relay1_OFF)
        time.sleep(1)
        print(serial_read_data(ser))
    except Exception as e:
        print("Error:", e)

def serial_read_data(ser):
    try:
        bytesToRead = ser.inWaiting()
        if bytesToRead > 0:
            out = ser.read(bytesToRead)
            data_array = [b for b in out]
            print(data_array)
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                return value
            else:
                return -1
    except Exception as e:
        print("Error:", e)
    return 0

soil_temperature = [1, 3, 0, 6, 0, 1, 100, 11]
def readTemperature():
    try:
        serial_read_data(ser)
        ser.write(soil_temperature)
        time.sleep(1)
        return serial_read_data(ser)
    except Exception as e:
        print("Error:", e)
        return None

soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
def readMoisture():
    try:
        serial_read_data(ser)
        ser.write(soil_moisture)
        time.sleep(1)
        return serial_read_data(ser)
    except Exception as e:
        print("Error:", e)
        return None

while True:
    print("TEST SENSOR")
    print(readMoisture())
    time.sleep(1)
    print(readTemperature())
    time.sleep(1)
