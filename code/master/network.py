import logging
from threading import Thread
from collections import deque

import zmq


logger = logging.getLogger('root')


class MasterNetwork(Thread):
    """Network communication for the master."""

    def __init__(self, messages_to_slaves):
        """Constructor for the class.

        Arguments:
         * inbox: messages from the Master, used for slaves and / or devices
         * outbox: messages to send to the Master
        """
        Thread.__init__(self)

        self.messages_to_slaves = messages_to_slaves

        self.ctx = zmq.Context()
        self.poller = zmq.Poller()

        self._running = True
        logger.debug("new master network")

        self.arduinos_ids = list(range(17))

        self.arduino_messages = deque()
        self.status_messages = deque()

    def configure_socket_from_slaves_arduinos(self):
        """Create ZMQ socket listening to the master."""
        self.socket_from_arduinos = self.ctx.socket(zmq.SUB)
        self.socket_from_arduinos.bind("tcp://0.0.0.0:5557")
        for topic in self.arduinos_ids:
            self.socket_from_arduinos.setsockopt(zmq.SUBSCRIBE, topic)

        self.poller.register(self.socket_from_arduinos, zmq.POLLIN)

    def configure_socket_from_slaves_statuses(self):
        """Create ZMQ socket listening to the master."""
        self.socket_from_slaves_statuses = self.ctx.socket(zmq.SUB)
        self.socket_from_slaves_statuses.bind("tcp://0.0.0.0:5557")
        self.socket_from_slaves_statuses.setsockopt(zmq.SUBSCRIBE, b"slave")

        self.poller.register(self.socket_from_slaves_statuses, zmq.POLLIN)

    def configure_socket_to_slaves(self):
        """Create ZMQ socket emitting to the master."""
        self.socket_to_slaves = self.ctx.socket(zmq.PUB)
        self.socket_to_slaves.bind("tcp://0.0.0.0:5556")

    def run(self):
        """
        Run loop of the class.

        Send messages to master if any and listen to
        communications from the master (populating the inbox queue).

        We use a poller to get a timeout while listening,
        this way we can kill the loop and send messages without waiting for the next message.
        """
        while self._running:
            self.send_command()
            self.receive()
        logger.info("end NetworkCommunication")

    def stop(self):
        """Stop the main loop."""
        self._running = False

    def receive(self):
        """Receive messsages from slaves.

        We have two sockets, one for arduinos messages
        and one for slaves statuses (connections, error...)
        """
        sockets = dict(self.poller.poll(20))
        if not sockets:
            return

        if self.socket_from_arduinos in sockets:
            message = [s.decode() for s in self.sock_in.recv_multipart()]
            device_id, message_string = message
            self.arduino_messages.append((device_id, message_string))

        if self.socket_from_slaves_statuses in sockets:
            message = [s.decode() for s in self.sock_in.recv_multipart()]
            device_id, message_string = message
            self.status_messages.append((device_id, message_string))

    def send_command(self):
        """Send a command to the slaves, with a channel and a message."""
        while self.messages_to_slaves:
            msg = self.messages_to_slaves.pop()
            self.socket_to_slaves.send_multipart(msg)
