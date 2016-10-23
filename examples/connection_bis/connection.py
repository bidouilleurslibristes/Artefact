# sudo pip install pyserial
import time

import serial

# ser = serial.Serial('/dev/cu.usbserial-DA00T1YU')
ser = serial.Serial('/dev/ttyACM0', timeout=1)
ser.flushInput()
ser.flushOutput()


def try_connection(serial_port):
    time.sleep(1)

    # Try to read a BONJOUR message
    txt = "toto"
    while not txt.startswith("BONJOUR"):
        nb_bytes = serial_port.inWaiting()
        if nb_bytes == 0:
            print("no bytes in try connection")
            return False

        txt = serial_port.readline().decode("ascii").strip()

    # Get the arduino unique id
    txt = txt.split(' ')[1]
    while serial_port.inWaiting() != 0:
        serial_port.read(serial_port.inWaiting())

    # Send back the response for connection
    print ("from arduino : ", txt)
    serial_port.write(txt.encode())

    # Wait for connection validation
    while not serial_port.inWaiting():
        time.sleep(0.01)

    # Verify the CONNECTED message
    text = serial_port.readline().decode("ascii").strip()
    print("response from arduino: ", text)
    if not text:
        return False
    if "CONNECTED" not in text:
        return False
    return True


connected = False
while not connected:
    connected = try_connection(ser)
    print("connected : ", connected)
    time.sleep(0.1)

while True:
    if ser.inWaiting() > 0:
        print(ser.readline().decode("ascii").strip())
