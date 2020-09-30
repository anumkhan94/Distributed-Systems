import socket
import time
from tkinter import *
from tkinter import ttk
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




# This function notifies server about its disconnection and closes the client socket on stop button press.
def stopClient():
    print("Client Disconnected")
    msg = clientName + " Disconnected"
    messagesList.insert(END, clientName + " Disconnected.")
    global s
    s.send(msg.encode())
    s.close()


def checkMessages(queuePref):
    print(queuePref)


if __name__ == "__main__":
    # creating a client GUI
    window = tk.Tk()
    window.title('Client')

    # GUi for client name input.
    text = tk.Label(master=window, text="Enter Client Name: ", width=50)
    e1 = Entry(window)

    text.pack()
    e1.pack()

    # this function executes on start button press and it fetches the client name from the user input.
    def get():
        global clientName
        clientName = e1.get()
        print("Im client: ", clientName)
        start_submit_thread(clientName)





    # GUI for start stop buttons.
    StartButton = tk.Button(window, text='Start', width=50, command=lambda: get())
    StartButton.pack()
    StopButton = tk.Button(window, text='Stop', width=50, command=stopClient)
    StopButton.pack()


    
    # GUI for message display.
    scrollbar = Scrollbar(window)
    scrollbar.pack(side=RIGHT, fill=Y)

    messagesList = Listbox(window, yscrollcommand=scrollbar.set, width=50)
    messagesList.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=messagesList.yview)


    # GUI for client input UPLOAD MESSAGES and DISPLAY MESSAGES.
    text2 = tk.Label(master=window, text="Enter Input Length (Numbers only): ", width=50)
    e2 = Entry(window)


    # this function executes on start button press and it fetches the client name from the user input.
    def getInputLength():
        global clientName
        inputLength = e2.get()
        print("Input: ", inputLength, uploadMessageDropDown.get())
        # start_submit_thread(clientName)


    text2.pack()
    e2.pack()

    # Combobox creation
    n = tk.StringVar()
    uploadMessageDropDown = ttk.Combobox(window, width=50, textvariable=n)

    # Adding combobox drop down list
    uploadMessageDropDown['values'] = ('Queue A',
                              'Queue B',
                              'Queue C')

    # monthchoosen.grid(column=1, row=4)
    uploadPref = uploadMessageDropDown.current(0)
    uploadMessageDropDown.pack()

    UploadMessageButton = tk.Button(window, text='Upload Message', width=50, command=lambda: getInputLength())
    UploadMessageButton.pack()

    text3 = tk.Label(master=window, text="Check for messages in Queue", width=50, pady=10)
    text3.pack()
    n = tk.StringVar()
    checkMessageDropDown = ttk.Combobox(window, width=50, textvariable=n)

    # Adding combobox drop down list
    checkMessageDropDown['values'] = ('Queue A',
                                       'Queue B',
                                       'Queue C')

    # monthchoosen.grid(column=1, row=4)
    checkMessageDropDown.current(0)
    checkMessageDropDown.pack()

    CheckMessageButton = tk.Button(window, text='Check Message', width=50, command=checkMessages(checkMessageDropDown.get()))
    CheckMessageButton.pack()


    window.mainloop()
