# Message oriented persistent systems

An asynchronous messaging system consisting of a message broker (server) and three client processes has been developed.
Each client process will connect to the server over a socket connection. The server should be able to handle all three
clients simultaneously and display the status of the connected clients in real time. How to distinguish clients is left to
the developer’s discretion.
Upon startup, clients will prompt users to select one of two options:
1. Upload message; or,
2. Check for messages.
If a user selects ‘Upload message’, the client will prompt the user to input a decimal number, which will represent a
length in meters. The client will prompt the user to designate an output queue (described below), then proceed to
upload the message to the server.
If a user selects ‘Check for messages’, the client will prompt the user to select an output queue. The client will proceed
to poll the output queue. If no messages are present in the queue, the user should be notified that the queue is empty.
If any messages are available, those messages will be retrieved from the queue and displayed to the user.
The message broker will maintain three output queues: A, B, and C. Upon placing a message into the queue, the server
will perform a conversion of the input length received from the client into several different units of length. The
corresponding units of length for each queue are as follows.
A
• Meter
• Millimeter
• Centimeter
• Kilometer
• Astronomical Unit
B
• Parsec
• Light Year
• Inch
• Foot
• Yard
C
• Mile
• Nautical Mile
• American football field
• Hand
• Horse
