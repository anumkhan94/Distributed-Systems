import socket
import time
from tkinter import *
import tkinter as tk
import threading

clientThread = None
s = socket.socket()
resumeThread = True
clientName = ""


def createClient(clientName):
    # Create a socket object
    global s
    global port
    s = socket.socket()
    port = 2894

    # connect to the server on local machine.
    s.connect(('127.0.0.1', port))

    # sending clientname to server
    msg = "clientname:" + clientName
    s.send(msg.encode())

    # receiving messages from server until the client socket is open.
    # The messages are parsed and handled accordingly.
    try:
        while s:
            recvmsg = s.recv(1024)
            recvmsg = recvmsg.decode()

            # check if it received connection accept message from server.
            if recvmsg == "Connection Accepted":
                print("Connection Accepted")
                messagesList.insert(END, recvmsg)

            # check if it received pause command and an integer along with it from server.
            elif "Pause:" in recvmsg:
                secs = recvmsg[6:]
                print("client waiting for " + secs + " seconds")

                messagesList.insert(END, "client waiting for " + secs + " seconds")
                secs = countdown(int(secs))
                # time.sleep(int(secs))
                msg = clientName + ", waited for " + str(secs) + " seconds"
                messagesList.insert(END, clientName + ", waited for " + str(secs) + " seconds")
                s.send(msg.encode())

            # checks for duplicate client name message and notifies client.
            elif ("Duplicate Client" in recvmsg):
                # close connection if client name already exists.
                messagesList.insert(END, recvmsg)
                print(recvmsg)
                s.close()  # client socket closed.
                break
            else:
                # display general messages.
                messagesList.insert(END, recvmsg)
                print(recvmsg)
                
    except socket.error as err:
        print(str(err))

# this function creates a new client thread on client side to avoid GUI freeze.
def start_submit_thread(clientName):
    global clientThread
    clientThread = threading.Thread(name="ClientThread", target=createClient, args=(clientName,))
    clientThread.daemon = True
    clientThread.start()
    print(" Client Thread count: ", threading.active_count())


# this function displays counter every time the client threads sleeps.
def countdown(secs):
    t = secs
    global resumeThread
    while t != 0 and resumeThread:
        counter.configure(text=t)
        time.sleep(1)
        t -= 1
    counter.configure()
    
    # if thread resume button is clicked it resumes.
    if resumeThread:
        return secs
    else:
        resumeThread = True
        return secs - t


# This function notifies server about its disconnection and closes the client socket on stop button press.
def stopClient():
    print("Client Disconnected")
    msg = clientName + " Disconnected"
    messagesList.insert(END, clientName + " Disconnected.")
    global s
    s.send(msg.encode())
    s.close()


if __name__ == "__main__":
    # creating a client GUI
    window = tk.Tk()
    window.title('Client')

    # GUi for client name input.
    text = tk.Label(master=window, text="Enter Client Name: ", width=50)
    e1 = Entry(window)

    # this function executes on start button press and it fetches the client name from the user input.
    def get():
        global clientName
        clientName = e1.get()
        print("Im client: ", clientName)
        start_submit_thread(clientName)

    text.pack()
    e1.pack()

    # GUI for start stop buttons.
    button = tk.Button(window, text='Start', width=50, command=lambda: get())
    button.pack()
    button = tk.Button(window, text='Stop', width=50, command=stopClient)
    button.pack()
    
    # GUI for message display.
    scrollbar = Scrollbar(window)
    scrollbar.pack(side=RIGHT, fill=Y)

    messagesList = Listbox(window, yscrollcommand=scrollbar.set, width=50)
    messagesList.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=messagesList.yview)

    # GUI for displaying live counter.
    counterLabel = tk.Label(window, text="Counter", width=10, bg="red")
    counterLabel.pack(fill=tk.X)

    counter = tk.Label(master=window, width=50, bg="yellow")
    counter.pack(fill=tk.X)


    # this function executes when resume thread button is pressed ny the user.
    def resumeT():
        global resumeThread
        resumeThread = False
        print(resumeThread)


    button = tk.Button(window, text='Resume', width=50, command=resumeT)
    button.pack()
    window.mainloop()
