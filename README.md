# Chat-Program
**Description**

This is a simple chat program that was created through socket programming in Python.

In this program messages and files can be sent by broadcast or unicast. 
Messages and files can be sent to clients that are offline using unicast.

When the client connects to the server, he must choose a nickname so that he can be identified.

All messages sent to the client while he was offline will be shown after choosing the nickname.

**Commands**

`/p (client name)` to send a private message to a client (unicast)

`/s (client name) (file name)` to send a private file to a client (unicast)

`/sall (file name)` to send a file to all clients connected to the server (broadcast)

`/o` to see the clients who are online 

To send a message to all online clients just write the message and press Enter.

**Compile Server**

python3 server.py

**Compile Client**

python3 client.py
