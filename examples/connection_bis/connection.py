# sudo pip install pyserial
import serial
import time
import binascii

# ser = serial.Serial('/dev/cu.usbserial-DA00T1YU')
ser = serial.Serial('/dev/ttyACM1')


def tryConnection (serialPort):
    time.sleep(1)

    txt = "toto"
    while not txt.startswith("BONJOUR"):
        nbBytes = ser.inWaiting()
        if nbBytes == 0:
            return False
        
        txt = ser.readline().decode("ascii").strip()

    txt = txt.split(' ')[1]
    while ser.inWaiting() != 0:
        ser.read(ser.inWaiting())
        
    print (txt)
    ser.flush()
    ser.write(txt.encode())
    ser.flush()

    #time.sleep(1)
    
    #print(ser.read(ser.inWaiting()).decode("ascii"))
    
    

tryConnection(ser)
while True:
    if ser.inWaiting() > 0:
        print(ser.readline().decode("ascii").strip())
