"""Communication stuff between master and slave raspi.

Slave side of the channel.

We use zmq for the communication.
"""

from threading import Thread
import logging
from sound import Manager as SoundManager

import zmq


logger = logging.getLogger('root')


class NetworkCommunication(Thread):
    """Network communication class between master and slave.

    Contains 2 network channel :
      * one SUB to get messages from the Master
      * one PUB to send messages to the Master

    The Master binds to 2 two sockets so we can have all
    Slaves using only 2 sockets to speak to the master.
    """

    def __init__(
            self, master_adress: "str",
            inbox: "dict of iterable", outbox: "iterable",
            topics: "iterable" = None
    ):
        """Constructor for the class.

        Arguments:
         * inbox: messages from the Master, used for slaves and / or devices
         * outbox: messages to send to the Master
         * topics: the topics to subscribe to. If any, we listen to everything
        """
        Thread.__init__(self)

        self.topics = topics or [b""]

        self.master_adress = master_adress

        self.ctx = zmq.Context()
        self.poller = zmq.Poller()
        self.configure_socket_in()
        self.configure_socket_out()

        self.messages_from_master = inbox
        self.messages_to_master = outbox

        self._running = True
        self._sound_manager = SoundManager()
        logger.debug("new network")

    def run(self):
        """
        Run loop of the class.

        Send messages to master if any and listen to
        communications from the master (populating the inbox queue).

        We use a poller to get a timeout while listening,
        this way we can kill the loop and send messages without waiting for the next message.
        """
        while self._running:
            self.send_messages_to_master()
            self.receive_messages_from_master()
        logger.info("end NetworkCommunication")

    def stop(self):
        """Stop the main loop."""
        self._running = False

    def configure_socket_in(self):
        """Create ZMQ socket listening to the master."""
        server_adress_in = "tcp://{}:5556".format(self.master_adress)

        self.sock_in = self.ctx.socket(zmq.SUB)
        self.sock_in.connect(server_adress_in)

        for topic in self.topics:
            self.sock_in.setsockopt(zmq.SUBSCRIBE, topic)
        self.poller.register(self.sock_in, zmq.POLLIN)

    def configure_socket_out(self):
        """Create ZMQ socket emitting to the master."""
        server_adress_out = "tcp://{}:5557".format(self.master_adress)
        self.sock_out = self.ctx.socket(zmq.PUB)
        self.sock_out.connect(server_adress_out)

        server_adress_statuses_out = "tcp://{}:5558".format(self.master_adress)
        self.sock_out_statuses = self.ctx.socket(zmq.PUB)
        self.sock_out_statuses.connect(server_adress_statuses_out)

    def send_messages_to_master(self):
        """Send messages in the outbox to the master."""
        while self.messages_to_master:
            msg = self.messages_to_master.popleft()
            msg = [s.encode() for s in msg]
            if b"status" in msg[0]:
                logger.debug("sending status : {}".format(msg))
                self.sock_out_statuses.send_multipart(msg)
            else:
                logger.debug("sending {} to master".format(msg))
                self.sock_out.send_multipart(msg)

    def receive_messages_from_master(self):
        """Receive messages from the master and populate the inbox for the correct device."""
        sockets = dict(self.poller.poll(2))
        if not sockets:
            return
        msg = self.sock_in.recv_multipart()  # we only have one listening socket
        msg = [s.decode() for s in msg]

        if msg[0] == "sound":
            self._sound_manager.play(msg[1])

        logger.info("received {} from master".format(msg))
        device_id, message_string = msg
        self.messages_from_master[device_id].append(
            message_string)
