# sudo pip install pyserial
import logging
import serial

try:
    from raven.handlers.logging import SentryHandler
    from raven import Client
    from raven.conf import setup_logging
    raven_ok = True
except ImportError:
    raven_ok = False

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
steam_handler.setFormatter(formatter)
logger.addHandler(steam_handler)

if raven_ok:
    client = Client('https://5351cd7e946648c2a537ed641f5b4663:56cb93aa44df4e0a92e4fec93fc9ccd8@sentry.io/103075')
    handler = SentryHandler(client, level=logging.ERROR)
    setup_logging(handler)

protocol_version = "v0.0.1"

# ser = serial.Serial('/dev/cu.usbserial-DA00T1YU')
ser = serial.Serial('/dev/ttyACM0', timeout=1)


class ProtocolError(Exception):
    pass

class TimeoutError(Exception):
    pass


def read_serial():
    response = ser.readline()
    if not response:
        raise TimeoutError
    return response

def get_protocol_and_version_from_answer():
    """ Parses a response from a device. For the protocol version 0.0.1 only.

    Argument: serial line from tty device
    Returns: dict(protocol, version) parsed from the response
    Raises: Protocol error if the response doesn't match the protocol
    """
    response = read_serial()
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

def is_connected():
    """ Test the last part of the handshake
    """
    connected_line = read_serial()

    logger.debug("IS CONNECTED -- response : {}".format(connected_line))
    try:
        line = response.strip().decode("ascii")
    except UnicodeDecodeError:
        return False
    message_expected = "CONNECTED"
    if line == message_expected:
        return True
    return False

def get_complete_handshake():
    ser.write(bytearray("A", "ascii")).to_bytes(1, byteorder="big")
    logger.info("HANDSHAKE -- step 1 : send init message to device")

    try:
        version_and_id = get_protocol_and_version_from_answer()
    except ProtocolError as e:
        logger.exception(e)
        return False, None

    logger.info("HANDSHAKE -- step 2 : received protocol and id")

    arduino_id = version_and_id["device_id"]
    ser.write(bytes(arduino_id)).to_bytes(1, byteorder="big")
    ser.flush()

    logger.info("HANDSHAKE -- step 3 : sent ID back")

    if is_connected():
        logger.info("HANDSHAKE -- step 4 : received connection OK")
        return True, version_and_id

    return False, None


def init_connection():
    arduino_connected = False
    while not arduino_connected:
        try:
            arduino_connected, version_and_id = get_complete_handshake()
        except TimeoutError:
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