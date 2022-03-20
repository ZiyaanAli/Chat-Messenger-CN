from tkinter import *
from socket import *
import _thread
import threading

def initialize_server(portNum):
    global conn, addr, s, listenMsg
    conn =0
    addr = 0
    s = socket(AF_INET, SOCK_STREAM)
    host = 'localhost'
    port = portNum
    print("HEY IM IN INIT SERVER f{port}")
    s.bind((host, port))
    s.listen(5)
    listenMsg.grid(row = 8, column= 0)
    listenMsg.place(x=150, y = 35)
    _thread.start_new_thread(handle, ())
    return conn
def handle():
    global conn,addr, successfulConnectionMsg, listenMsg
    while True:
        conn, addr = s.accept()
        successfulConnectionMsg.grid(row = 8, column= 0)
        successfulConnectionMsg.place(x=120, y = 56)
        listenMsg.after(1000, listenMsg.destroy)    
        successfulConnectionMsg.after(2500, successfulConnectionMsg.destroy)
def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)
    if state==0:
        chatlog.insert(END, 'YOU: ' + msg)
    else:
        chatlog.insert(END, 'CLIENT: ' + msg)
    chatlog.config(state=DISABLED)
    chatlog.yview(END)
def checkPortNum(portNum):
    if(portNum == ''):
        return "empty"
    portNum = int(portNum)
    if(portNum > 65355 or portNum < 0):
        portNum="incorrectPortNum"
    return portNum
def listen():
    global entry
    global errorMsgLabel
    global emptyErrorMsgLabel
    global conn
    global chatlog
    global emptyError
    global incorrectPortNum
    global emptyPortNum
    global successfulConnectionMsg    
    emptyErrorMsgLabel.after(5000, emptyErrorMsgLabel.destroy)
    errorMsgLabel.after(5000, errorMsgLabel.destroy)
    userPortNum = entry.get()
    portNum = checkPortNum(userPortNum)
    if(portNum == "empty"):
        emptyErrorMsgLabel.grid(row = 8, column= 0)
        emptyErrorMsgLabel.place(x=80, y = 36)
        return    
    if(portNum == "incorrectPortNum"):
        print(portNum)
        errorMsgLabel.grid(row = 8, column= 0)
        errorMsgLabel.place(x=70, y = 56)
        return
    print("BEFORE conn")
    print(type(portNum))
    thread = threading.Thread(target = initialize_server(portNum))
    thread.start()
    print("AFter conn")
def send():    
    global textbox
    global conn
    msg = textbox.get("0.0", END)
    update_chat(msg, 0)
    conn.send(msg.encode('ascii'))
    textbox.delete("0.0", END)
def receive():
    while 1:
        try:
            data = conn.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass
def msgPress(event):
    send()
def listenPress(event):
    listen()

def GUI():
    global chatlog
    global textbox
    global entry
    global errorMsgLabel
    global incorrectPortNum
    global conn
    global emptyPortNum
    global emptyErrorMsgLabel
    global successfulConnectionMsg, listenMsg
    incorrectPortNum = False 
    emptyPortNum = False
    gui = Tk()
    gui.title("Server Chat Box")
    gui.geometry("980x430")
    chatlog = Text(gui, bg='grey')
    chatlog.config(state=DISABLED)

    # buttons to send messages
    sendbutton = Button(gui, bg='grey', fg='white', text='SEND', command=send)
    listenBtn = Button(gui, bg='grey', fg= 'white', text='Listen', command=listen)
    portLabel = Label(gui, text="Port Number: ")
    errorMsgLabel = Label(gui, text="Incorrect Port Entered.")
    emptyErrorMsgLabel = Label(gui, text="Port Not Entered. Try Again")
    successfulConnectionMsg = Label(gui, text="Connection Built.")
    listenMsg = Label(gui, text="Listening.")
    entry = Entry(gui)
    textbox = Text(gui, bg='grey')
    portLabel.grid(row=6, column=0)
    portLabel.place(x=1, y=4)
    entry.grid(row = 6, column=0)
    listenBtn.grid(row = 6, column= 0)
    entry.place(x=80, y=6, height=20, width=800)
    listenBtn.place(x=900, y= 3)
    chatlog_y = 30
    chatlog.place(x=6, y=chatlog_y, height=356, width=965)
    textbox.place(x=6, y=401, height=20, width=865)
    sendbutton.place(x=900, y=401, height=20, width=50)
    textbox.bind("<KeyRelease-Return>", msgPress)
    listenBtn.bind("<KeyRelease-Return>", listenPress)
    _thread.start_new_thread(receive, ())
    gui.mainloop()
if __name__ == '__main__':
    chatlog = textbox = None
    #conn = initialize_server(1234)
    GUI()