# sudo pip install pyserial
import logging
import serial


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
steam_handler.setFormatter(formatter)
logger.addHandler(steam_handler)


protocol_version = "v0.0.1"

# ser = serial.Serial('/dev/cu.usbserial-DA00T1YU')
ser = serial.Serial('/dev/ttyACM0')


class ProtocolError(Exception):
    pass

def get_protocol_and_version_from_answer(response):
    """ Parses a response from a device. For the protocol version 0.0.1 only.

    Argument: serial line from tty device
    Returns: dict(protocol, version) parsed from the response
    Raises: Protocol error if the response doesn't match the protocol
    """
    line = response.strip().decode("ascii")
    logger.debug("GET_PROTOCOL_AND_VERSION -- got : {}".format(line))
    elements = line.split(" ")

    if len(elements) != 3:
        excep_text = "wrong response, got {}"
        raise ProtocolError(excep_text.format(response))

    message_expected = "connection_protocol"
    version_expected = "v0.0.1"

    message, version, device_id = elements
    if message.lower() != message_expected:
        excep_text = "wrong message, got {} - expected {}"
        raise ProtocolError(excep_text.format(message, message_expected))

    if version != version_expected:
        excep_text = "wrong version, got {} - expected {}"
        raise ProtocolError(excep_text.format(version, version_expected))

    res = {"version": "0.0.1", "device_id": ord(device_id)}
    logger.debug("Parsing ok : {}".format(res))
    return res

def is_connected(response):
    """ Test the last part of the handshake
    """
    logger.debug("IS CONNECTED -- response : {}".format(response))
    line = response.strip().decode("ascii")
    message_expected = "CONNECTED"
    if line == message_expected:
        return True
    return False

def get_complete_handshake():
    ser.write(bytearray("A", "ascii")).to_bytes(1, byteorder="big")
    logger.info("HANDSHAKE -- step 1 : send init message to device")

    initial_line = ser.readline()
    try:
        version_and_id = get_protocol_and_version_from_answer(initial_line)
    except ProtocolError as e:
        logger.exception(e)
        return False, None

    logger.info("HANDSHAKE -- step 2 : received protocol and id")

    arduino_id = version_and_id["device_id"]
    ser.write(bytes(arduino_id)).to_bytes(1, byteorder="big")
    ser.flush()

    logger.info("HANDSHAKE -- step 3 : sent ID back")

    connected_line = ser.readline()
    if is_connected(connected_line):
        logger.info("HANDSHAKE -- step 4 : received connection OK")
        return True, version_and_id

    return False, None


def init_connection():
    arduino_connected = False
    while not arduino_connected:
        arduino_connected, version_and_id = get_complete_handshake()
    logger.warning("INITIATED CONNECTION WITH : {}".format(version_and_id))
    return version_and_id


def main():
    version_and_id = init_connection()

    arduino_id = version_and_id["device_id"]
    print("Connected to arduino {} \o/".format(arduino_id))
    while True:
        print("From arduino {} : {}".format(arduino_id, ser.readline()))


if __name__ == '__main__':
    main()