# sudo pip install pyserial
import serial
import time

# ser = serial.Serial('/dev/cu.usbserial-DA00T1YU')
ser = serial.Serial('/dev/ttyACM0')


def tryConnection (serialPort):
    time.sleep(1)
    nbBytes = ser.inWaiting()
    if nbBytes == 0:
        return False

    txt = "toto"
    while not txt.startswith("BONJOUR"):
        txt = readLine().decode("ascii").strip()
        
    txt = ser.read(nbBytes).decode("ascii").strip()
    print(txt)
    
    

tryConnection(ser)

