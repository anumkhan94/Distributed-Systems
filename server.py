from _thread import *
import threading
import socket
import os
from tkinter import *
import tkinter as tk
import random
import time
import json

serverOn = True
clientsDict = {}
soc = socket.socket()
main_thread = None
c = socket.socket()


def threaded(c):
    msg = 'Connection accepted'
    c.send(msg.encode())
    c.send("hi from server".encode())

    while c:
        msg = c.recv(1024).decode()
        print(msg)

        msg = str(msg)
        if "Disconnected" in msg:
            words = msg.split(" ")
            print(words)
            del clientsDict[words[0]]
            # maintain messages
            messageList.insert(END, msg)
            print("inside disconnected")
            # maintain active client list
            print(clientsDict)

            if not clientsDict:
                clientList.configure(text="No active clients.")
            clients = clientsDict.keys()
            clientList.configure(text=clients)

        else:
            print("threaded else")
            name = msg[0: msg.find(",")]
            print("client " + name + " is now awake")
            messageList.insert(END, 'client ' + name + ' is now awake')
            clientsDict[name][2] = "active"
            t1 = clientsDict[name][0]
            print("Im awaken: ", t1, type(t1))


def selectClientThread():
    try:
        while soc:
            if not clientsDict:
                time.sleep(10)
                continue

            time.sleep(10)
            keys = list()

            for k, v in clientsDict.items():
                if v[2] == "active":
                    keys.append(k)

            if not keys:
                continue
            randKey = random.choice(keys)
            print("random key: ", randKey)

            t = clientsDict[randKey][0]
            c = clientsDict[randKey][1]

            print(t, type(t))

            nSeconds = random.randint(3, 9)
            print(nSeconds)
            # msg = '{"Pause": nSeconds}'
            msg = "Pause:" + str(nSeconds)
            # msg = json.loads(msg)
            messageList.insert(END, randKey + " sleeping for " + str(nSeconds) + " secs")
            clientsDict[randKey][2] = "sleep"
            c.send(msg.encode())

    except socket.error as err:
        print(str(err))


def manageClientRequests():
    try:
        while soc:
            c, add = soc.accept()
            msg = c.recv(1024)
            print(msg, type(c))
            recvmsg = str(msg)

            messageList.insert(END, recvmsg)
            clientName = recvmsg[recvmsg.rfind("clientname:"): -1]
            clientName = clientName[11:]
            print("request from " + str(add) + "client Name:" + clientName)
            messageList.insert(END, "request from " + str(add) + "client Name:" + clientName)
            if clientName in clientsDict:
                print("Duplicate Client " + clientName)
                c.send("Duplicate Client".encode())
                c.close()
            else:
                # forks a new thread for each client.
                newClientThread = threading.Thread(name=clientName, target=threaded, args=(c,))
                newClientThread.daemon = True
                newClientThread.start()
                print("Thread count: ", threading.active_count())
                clientsDict[clientName] = [newClientThread, c, "active"]
                print(clientsDict)

                # update active clients list
                if not clientsDict:
                    clientList.configure(text="No active clients.")

                clients = clientsDict.keys()
                clientList.configure(text=clients)


    except socket.error as errorMsg:
        print("main func: " + str(errorMsg))


def stopServer():
    global soc
    messageList.insert(END, "Server Stopped")
    print("server stopped")
    soc.close()


def createServer():
    try:
        global host
        global port
        global soc
        global serverOn
        host = ""
        port = 2894
        soc = socket.socket()
        soc.bind((host, port))
        print("server started on port " + str(port))
        messageList.insert(END, 'server started on port ' + str(port))
        soc.listen(5)

        manageClientRequests()
        # return soc
    except socket.error as errorMsg:
        print("server not created " + errorMsg)


def start_submit_thread(event):
    global main_thread
    main_thread = threading.Thread(name="ServerThread", target=createServer)
    main_thread.daemon = True
    main_thread.start()
    print(" Server Thread count: ", threading.active_count())

    sleepThread = threading.Thread(target=selectClientThread)
    sleepThread.daemon = True
    sleepThread.start()


if __name__ == "__main__":
    window = tk.Tk()

    window.title('Server')
    button = tk.Button(window, text='Start', width=25, command=lambda: start_submit_thread(None))
    button.pack()
    button = tk.Button(window, text='Stop', width=25, command=stopServer)
    button.pack()

    scrollbar = Scrollbar(window)
    scrollbar.pack(side=RIGHT, fill=Y)
    messageList = Listbox(window, yscrollcommand=scrollbar.set, width=50)
    messageList.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=messageList.yview)

    clientListLabel = tk.Label(master=window, text="Active Clients: ", width=50, bg="red")
    clientListLabel.pack(fill=tk.X)

    clientList = tk.Label(master=window, width=50, bg="yellow")
    clientList.pack(fill=tk.X)

    frame2 = tk.Frame(master=window, height=50)
    frame2.pack(fill=tk.X)

    window.mainloop()

