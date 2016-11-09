"""Implement the serial communication handshake and protocol.

This can be used to automatically connect to an arduino for instance.
Used during 2016 zoomachine edition
"""

import time
import logging
from threading import Thread

import serial
from serial.serialutil import SerialException
from serial.tools import list_ports


logger = logging.getLogger('root')


class SerialDeviceException(SerialException):
    """Exception for serial devices."""

    def __init__(self, device):
        """We give infos about the device that raised the excetion."""
        self.device = device


def list_devices_connected(patterns):
    """Enumerate plugged devices with USB PID/VID matching the patterns provided as argument."""
    for pattern in patterns:
        for port in list_ports.grep(pattern):
            yield port.device


class SerialDevice(Thread):
    """Open a serial communication to a given port.

    The connection will succed if the device implement a Simple
    Serial Communication Protocol (SSCP), described in the documentation.
    """

    def __init__(self, port, msg_in, msg_out: "defaultdict of iterables", msg_error):
        """Inialise a serial device."""
        Thread.__init__(self)

        self.connected = False
        self.device_id = None
        self.port = port
        self.serial = serial.Serial(port, timeout=1, baudrate=115200)
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        self.last_heartbeat = 0

        self.msg_in = msg_in
        self.msg_out = msg_out
        self.msg_error = msg_error

        self._stop = False

    def stop(self):
        """Stop the device mainloop."""
        self._stop = True

    def _disconnect(self):
        """Handle disconnection stuff."""
        self.connected = False
        self.device_id = None

    def _run(self):
        """Connect to a device and read / write / send periodic heartbeat."""
        while not self._stop:
            while not self.connected:
                self.connect()
                time.sleep(0.1)

            self.read_from_device()
            self.send_to_device()

            if (time.time() - self.last_heartbeat) > 1:
                self.heartbeat()
                self.last_heartbeat = time.time()
            time.sleep(0.01)

    def run(self):
        """Try to connect and raise SerialDeviceException if there is a disconnection."""
        try:
            self._run()
        except (SerialException, OSError):
            self.msg_error.append(self)
        except Exception as e:
            logger.error("Unknown exception")
            logger.exception(e)
            self.msg_error.append(self)
        else:
            logger.info("End of serial mainloop -- {}".format(self))
            self.msg_error.append(self)
            self._disconnect()
        finally:
            self.serial.close()

    def _read_device_id(self):
        txt = ""
        while not txt.startswith("BONJOUR"):
            nb_bytes = self.serial.inWaiting()
            if nb_bytes == 0:
                self._disconnect()
                continue
            txt = self.serial.readline().decode("ascii").strip()
        return txt.split(' ')[1]

    def _connection_verification(self):
        # Wait for connection validation
        while not self.serial.inWaiting():
            time.sleep(0.01)

        # Verify the CONNECTED message
        text = self.serial.readline().decode("ascii").strip()
        if not text:
            self._disconnect()
            return self.connected
        if "CONNECTED" not in text:
            self._disconnect()
            return self.connected

        self.connected = True
        return self.connected

    def connect(self):
        """Connect to a device using SSCP."""
        logger.debug("init connection")
        # Try to read a BONJOUR message and get the arduino unique id
        device_id = self._read_device_id()
        if not device_id:
            self._disconnect()
            return False

        # Send back the response for connection
        logger.debug("device id: {}".format(device_id))
        self.serial.write(device_id.encode())

        connected = self._connection_verification()
        if not connected:
            logger.debug(str(self))
            return False

        self.connected = True
        self.device_id = device_id
        logger.info(str(self))
        return True

    def heartbeat(self):
        """Send a heartbeat packet and check the response according SSCP.

        This is useful to check for disconnections with the device.
        """
        self.read_from_device()
        heartbeat_text = "PING ?\n".encode()
        self.serial.write(heartbeat_text)
        text = self.serial.readline().decode("ascii").strip()
        logger.debug("heartbeat from arduino: ".format(text))
        if not text and "PONG !" not in text:
            self._disconnect()
            logger.info(str(self))
            return False

        self.connected = True
        logger.debug(str(self))
        return True

    def read_from_device(self):
        """Read all lines from the serial and add them to msg_in box.

        The msg_in box is shared between all the instances connected
        to the host, so we need to specify the device ID that
        wrote the message.
        """
        while self.serial.inWaiting():
            message = self.serial.readline().decode("ascii").strip()
            self.msg_in.append((self.device_id, message))

    def send_to_device(self):
        r"""Send data from msg_out box to the connected arduino.

        The msg_out is a dictionnary of queues contenaing
        messages for each device and messages are the string
         transmitted to the arduino.
        If the string doen't end with carriage return (\n) we add it.
        """
        msg_out = self.msg_out[self.device_id]
        while msg_out:
            msg = msg_out.pop()
            if not msg.endswith('\n'):
                msg += "\n"
            logging.INFO(msg)
            self.serial.write(msg.encode)

    def __repr__(self):
        text_connected = "connected to {}".format(self.device_id)
        text_non_connected = "disconnected"
        text = text_connected if self.connected else text_non_connected
        return "SerialDevice {} -- bound to {}".format(text, self.port)
