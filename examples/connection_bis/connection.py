# sudo pip install pyserial
import time

import serial

# ser = serial.Serial('/dev/cu.usbserial-DA00T1YU')
ser = serial.Serial('/dev/ttyACM1', timeout=1, baudrate=115200)


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


def heartbeat(serial_port):
    heartbeat_text = "PING ?\n".encode()
    serial_port.write(heartbeat_text)
    text = serial_port.readline().decode("ascii").strip()
    print("heartbeat from arduino: ", text)
    if not text:
        return False
    if "PONG !" not in text:
        return False
    return True


while True:
    ser.flushInput()
    ser.flushOutput()

    connected = False
    while not connected:
        connected = try_connection(ser)
        print("connected : ", connected)
        time.sleep(0.1)

    last_heartbeat = 0
    while connected:
        if ser.inWaiting() > 0:
            print(ser.readline().decode("ascii").strip())
        if (time.time() - last_heartbeat) > 1:
            connected = heartbeat(ser)
            last_heartbeat = time.time()
