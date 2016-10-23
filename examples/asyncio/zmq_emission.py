import json
import time
import zmq

c = zmq.Context()
s = c.socket(zmq.PUB)

protocol = "tcp"
port = "5556"
adress = "127.0.0.1"
url = "{}://{}:{}".format(protocol, adress, port)
s.bind(url)
print('Publisher bound to url : {}'.format(url))

i = 0
channel = "1"
while True:
    message = {"data": i}
    s.send_multipart([channel, json.dumps(message)])
    print(json.dumps(message))
    i += 1
    time.sleep(2)