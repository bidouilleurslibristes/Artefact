Code for a network between a Master and multiple slaves.

The master acts as a controller (in MVC) and streams the state to the slaves.
The slaves get the messages and update the serial devices statuses.


## ZMQC

 * simulate server reception : `zmqc -rb SUB 'tcp://0.0.0.0:5557'`
 * simulate server emission : `code/master/simulate_server_to_slaves_cli.py`
 * simulate slave emission : `zmqc -wb PUB 'tcp://0.0.0.0:5557'` (don't know if it works, need to send multipart, )
 * simulate slave reception : `zmqc -rc SUB 'tcp://master:5556'`