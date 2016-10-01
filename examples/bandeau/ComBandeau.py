import serial

ser_led = serial.Serial('/dev/ttyACM2',9600)
ser_button = serial.Serial('/dev/ttyACM1',9600)

def envoie (n):
    ser_led.write(n).to_bytes(1,byteorder='big')
    print("sent : {}".format(n))
    
def envoieListe (L):
    for n in range(15):
        envoie(L[n])

def lire ():
    s = ser_button.read()
    print(s)

def change ():
    c = ser_button.read()
    print(c)
    if c == b'1':
        envoieListe([b"1" for _ in range(15)])
        print("Appuie")
    else :
        envoieListe([b"2" for _ in range(15)])
        print("Appuie pas :D")

def main():
    change()

if __name__ == "__main__":
    main()
