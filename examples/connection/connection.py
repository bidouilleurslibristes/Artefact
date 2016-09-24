# sudo pip install pyserial
import serial

ser = serial.Serial('/dev/cu.usbserial-DA00T1YU')

while 0 == 0:
	line = ''
	s = ser.read()

	while s != '\n':
		line += s
		s = ser.read()

	print (line)

	line = line.split(' ')

	if len(line) > 1 and line[1].startswith('L01'):
		print (line[1])
		ser.write ('L01'.encode('ascii'))
		ser.flush()
	
#	ser.write(b'L01')
#	s = ser.read(10)
#	print (s)

