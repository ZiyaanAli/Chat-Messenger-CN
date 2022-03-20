from tkinter import *
from socket import *
import _thread
import nmap

from server import checkPortNum

def checkServerAlive(port,s):
            return s.connect_ex(('localhost', port)) == 0
    

def initialize_client(userIP, userPortNum):
    global ip, s, serverAliveMsg, successfulConnectionMsg
    s = socket(AF_INET, SOCK_STREAM)
    ip = userIP
    port = userPortNum
    if(checkServerAlive(port, s) == False):#check if true is returned or not
        serverAliveErrorMsg.grid(row = 8, column= 0)
        serverAliveErrorMsg.place(x=80, y = 36) 
        serverAliveErrorMsg.after(2500, serverAliveErrorMsg.destroy)
        return     
    else:
         #successful connection Msg:
        successfulConnectionMsg.grid(row = 8, column= 0)
        successfulConnectionMsg.place(x=120, y = 56) 
        successfulConnectionMsg.after(2500, successfulConnectionMsg.destroy)
    s.connect((userIP, port))
    # print("Junya")
    return s
def checkPortNum(portNum):
    if(portNum == ''):
        return "empty"
    portNum = int(portNum)
    if(portNum > 65355 or portNum < 0):
        portNum="incorrectPortNum"
    return portNum
def checkIP(userIP):
    if(userIP == ''):
        return "empty"
def connect():
    global emptyIPErrorMsgLabel, emptyIPPortErrorMsgLabel, successfulConnectionMsg
    userIP = ''
    emptyIPPortErrorMsgLabel.after(5000, emptyIPPortErrorMsgLabel.destroy)
    errorMsgLabel.after(5000, errorMsgLabel.destroy)
    emptyErrorMsgLabel.after(5000, emptyErrorMsgLabel.destroy)
    emptyIPErrorMsgLabel.after(5000, emptyIPErrorMsgLabel.destroy)
    user_IP_port = entry.get()
    if(user_IP_port == ''):
        emptyIPPortErrorMsgLabel.grid(row = 8, column= 0)
        emptyIPPortErrorMsgLabel.place(x=80, y = 36)
        return
    user_IP = user_IP_port.split(':')[0]
    user_Port = user_IP_port.split(':')[1]
    user_Port = int(user_Port)
    print(user_IP)
    print( user_Port)
    ip_check = checkIP(user_IP)
    portNum = checkPortNum(user_Port)    
    if(portNum == "empty"):
        emptyErrorMsgLabel.grid(row = 8, column= 0)
        emptyErrorMsgLabel.place(x=80, y = 36)
        return
    if(portNum == "incorrectPortNum"):
        portNum = 1234;#will assign default port no.
        entry.delete("0", END)
        entry.insert(0, "127.0.0.1:1234")
        #chatlog.delete("0", END)
        print(portNum)
        errorMsgLabel.grid(row = 8, column= 0)
        errorMsgLabel.place(x=80, y = 56)
    if(ip_check == "empty"):
        emptyIPErrorMsgLabel.grid(row = 8, column= 0)
        emptyIPErrorMsgLabel.place(x=80, y = 36)
    initialize_client(user_IP, portNum) 
def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)
    if state==0:
        chatlog.insert(END, 'YOU: ' + msg)
    else:
        chatlog.insert(END, 'SERVER: ' + msg)
    chatlog.config(state=DISABLED)
    chatlog.yview(END)
    
def send():
    global textbox
    global s
    msg = textbox.get("0.0", END)
    update_chat(msg, 0)
    s.send(msg.encode('ascii'))
    textbox.delete("0.0", END)
def receive():
    while 1:
        try:
            data = s.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass
def press(event):
    send()
def GUI():
    global chatlog
    global textbox
    global entry
    global errorMsgLabel
    global incorrectPortNum
    global conn
    global emptyPortNum
    global emptyErrorMsgLabel
    global emptyIPErrorMsgLabel, emptyIPPortErrorMsgLabel, serverAliveErrorMsg
    global successfulConnectionMsg

    incorrectPortNum = False
    emptyPortNum = False
    gui = Tk()
    gui.title("Client Chat Box")
    gui.geometry("980x430")
    chatlog = Text(gui, bg='grey')
    chatlog.config(state=DISABLED)
    sendbutton = Button(gui, bg='grey', fg='white', text='Send', command=send)
    connectBtn = Button(gui, bg='grey', fg= 'white', text='Built', command=connect)

    portLabel = Label(gui, text="Enter IP_Port: ")
    errorMsgLabel = Label(gui, text="Incorrect Port ")
    emptyErrorMsgLabel = Label(gui, text="Port Not Entered. Try Again")
    emptyIPErrorMsgLabel = Label(gui, text="IP Not Entered. Try Again")
    emptyIPPortErrorMsgLabel = Label(gui, text="Nothing Entered. Try Again")
    serverAliveErrorMsg = Label(gui, text="Server not listening. Try Again")
    successfulConnectionMsg = Label(gui, text="Connection Built.")
    entry = Entry(gui)
    textbox = Text(gui, bg='Grey')
    portLabel.grid(row=6, column=0)
    portLabel.place(x=1, y=4)
    entry.grid(row = 6, column=0)
    connectBtn.grid(row = 6, column= 0)
    entry.place(x=110, y=6, height=20, width=780)
    connectBtn.place(x=920, y= 3)
    chatlog_y = 30
    chatlog.place(x=6, y=chatlog_y, height=356, width=965)
    
    print(incorrectPortNum)
    if(incorrectPortNum == True):
        print("Inside incorrect portnum check: value =  " + incorrectPortNum)    
        errorMsgLabel.grid(row = 8, column= 0)
        errorMsgLabel.place(x=80, y = 36)
        chatlog_y = 100
    if(emptyPortNum):
        emptyErrorMsgLabel.grid(row = 8, column= 0)
        emptyErrorMsgLabel.place(x=80, y = 36)
        chatlog_y = 100
    textbox.place(x=6, y=401, height=20, width=865)
    sendbutton.place(x=900, y=401, height=20, width=50)
    textbox.bind("<KeyRelease-Return>", press)

    _thread.start_new_thread(receive, ())
    
    gui.mainloop()


if __name__ == '__main__':
    chatlog = textbox = None
    GUI()