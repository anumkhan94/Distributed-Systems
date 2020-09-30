# Socket Programming.

A system consisting of a server and three client processesis developed where each client process will connect to the server
over a socket connection and register a username at the server. The server should be able to handle all three clients
simultaneously and display the names of the connected clients in real time.
Two or more clients may not use the same username simultaneously. Should the server detect a concurrent conflict in
username, the client’s connection should be rejected, and the client’s user should be prompted to input a different
name.

Every ten seconds, the server will randomly select a connected client and send that client an integer between 3 and 9.
Upon receiving the integer, the client will pause (e.g., sleep or otherwise suspend) the thread managing the connection
to the server for a period equaling the value received from the server, in seconds. The client’s GUI will maintain a
decrementing countdown timer indicating when the thread will resume, as well as a button to skip the wait and resume
the thread’s operation immediately.

When the client thread is finished waiting, it will reply to the server with a message stating, “Client <name> waited <#>
seconds for server.” The server will display this message on its GUI. This sequence will be repeated until the
components are manually terminated by the user.
