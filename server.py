from tkinter import *
from tkinter import messagebox
import time
import socket
import smtplib
import sys
global s
global flag
global conn


#--------------------INTERFAZ GRAFICA-----------------------
root = Tk()
root.title("Shell Connector  -----> By: ISU - InfoSecUpiicsa Ci5C0")
root.iconbitmap("isu.ico")


mFrame=Frame(root,width="500",height="600",bg="ivory2")
mFrame.config(relief="raised",bd="12")
mFrame.pack(fill="both",expand="true")

hostMail = StringVar()
portMail = IntVar()
host = StringVar()
port = IntVar()
com = StringVar()
passw = StringVar()
email = StringVar()
asunto = StringVar()
dest = StringVar()
text = StringVar


#------------------- FUNCIONES -----------------------------

def send_email():
    tiempo = time.ctime()
    dest = mDest.get()
    asunto = mAs.get()
    email = mEmail.get()
    passw = mPass.get()
    hostm = mHostMail.get()
    portm = int(mPortMail.get())
    text = "Nueva Conexion a la direccion IP " + mDir.get() + "  Por el puerto " + mPort.get() + "  Con fecha y hora: " + tiempo
    body = "\r\n".join(("From: %s"%email,"To: %s"%dest,"Subject: %s"%asunto,"",text))

    server = smtplib.SMTP(hostm,portm)
    server.ehlo()
    server.starttls()
    server.login(email,passw)
    server.sendmail(email,dest,body)
    server.close()
    messagebox.showwarning("Correo enviado","El correo se a enviado correctamente")


def onEnter(event):
    sendCom()

def onEnterC(event):
    main()

def sendCom():
    com = mInput.get()
    send_commands(com)

def closeConnection():
    global conn
    conn.close()
    mCommands.insert(INSERT," CONEXIÓN TERMINADA \n")


def socket_bind():
    try:
        host = mDir.get()
        port = int(mPort.get())
        global s
        s = socket.socket()
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        mCommands.insert(INSERT,"Error al intentar conectar con el cliente: " + str(msg))
        mCommands.insert(INSERT,"Reintentando....")
        socket_bind()

def socket_accept():
    global conn
    conn,address = s.accept()
    mCommands.insert(INSERT, "SOCKET ENLAZADO POR EL PUERTO:" + mPort.get() + "\n")
    mCommands.insert(INSERT,"LA CONEXIÓN SE HA ESTABLECIDO CON EL HOST CON DIRECCIÓN["+address[0]+"] | Y SE CONTINUA POR EL PUERTO [" +str(address[1])+"] \n")


def send_commands(com):
    if com == 'quit':
        conn.close()
        s.close()
        sys.exit()
    if len(str.encode(com)) > 0:
        conn.send(str.encode(com))
        client_response = str(conn.recv(1024),'ISO-8859-1')
        mCommands.insert(END,client_response + "\n")



def main():
    socket_bind()
    socket_accept()


#--------------------------- TERMINA BLOQUE DE FUNCIONES CONTINUA BLOQUE DE INTERFAZ --------------------------------------------------------
Label(mFrame, text="Bienvenido a Shell Connector [Server]",fg="DodgerBlue4",font=("Arial Rounded MT Bold",15)).grid(row=0,column=1,columnspan=3,pady=5)

Label(mFrame, text="Datos para la conexion",fg="DodgerBlue4",font=("Arial Rounded MT Bold",12)).grid(row=1,column=0,pady=5)

Label(mFrame, text="Direccion IP:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=2,column=0,sticky="e",pady=5)
mDir = Entry(mFrame, width=30, justify="left",font=("Arial Rounded MT Bold",8),textvariable=host)
mDir.bind('<Return>',onEnterC)
mDir.grid(row=2,column=1,sticky="w",pady=5)


Label(mFrame, text="Puerto:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=3,column=0,sticky="e",pady=5)
mPort = Entry(mFrame, width=30,justify="left",font=("Arial Rounded MT Bold",8),textvariable=port)
mPort.bind('<Return>',onEnterC)
mPort.grid(row=3,column=1,sticky="w",pady=5)


btConectar = Button(mFrame,text="Conectar",width=30,bg="SteelBlue2",relief="groove",command=main)
btConectar.grid(row=2,column=3,columnspan=2,pady=5)

Label(mFrame,text="Output",font=("Arial Rounded MT Bold",8)).grid(row=4,column=0,pady=5)
mCommands = Text(mFrame,wrap=WORD)
mCommands.config(state="normal")
mCommands.grid(row=4,column=1,columnspan=4,sticky="w",pady=5)


scrollVert = Scrollbar(mFrame, command=mCommands.yview)
scrollVert.grid(row=4,column=6, sticky="nsew")


mCommands.config(yscrollcommand=scrollVert.set)

Label(mFrame,text="Input",font=("Arial Rounded MT Bold",8)).grid(row=5,column=0,pady=5)
mInput = Entry(mFrame,width=30,font=("Arial Rounded MT Bold",12),textvariable=com)
mInput.bind('<Return>',onEnter)
mInput.grid(row=5,column=1,columnspan=4,sticky="w",pady=5)

btCommand = Button(mFrame,text="Enviar",width=30,bg="steelblue2",relief="groove", command=sendCom)
btCommand.grid(row=5,column=4,pady=5)

Label(mFrame, text="Enviar correo electronico ",fg="DodgerBlue4",font=("Arial Rounded MT Bold",12)).grid(row=6,column=0,pady=5)

Label(mFrame, text="Remitente:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=7,column=0,sticky="e",pady=5)
mEmail = Entry(mFrame, width=30, justify="left",font=("Arial Rounded MT Bold",8),textvariable=email)
mEmail.grid(row=7,column=1,sticky="w",pady=5)

Label(mFrame, text="Destinatario:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=8,column=0,sticky="e",pady=5)
mDest = Entry(mFrame, width=30, justify="left",font=("Arial Rounded MT Bold",8),textvariable=dest)
mDest.grid(row=8,column=1,sticky="w",pady=5)

Label(mFrame, text="Asunto:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=9,column=0,sticky="e",pady=5)
mAs = Entry(mFrame, width=30, justify="left",font=("Arial Rounded MT Bold",8),textvariable=asunto)
mAs.grid(row=9,column=1,sticky="w",pady=5)

Label(mFrame, text="Contraseña:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=10,column=0,sticky="e",pady=5)
mPass = Entry(mFrame, width=30,justify="left",font=("Arial Rounded MT Bold",8),show="*",textvariable=passw)
mPass.grid(row=10,column=1,sticky="w",pady=5)

Label(mFrame, text="Servidor:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=11,column=0,sticky="e",pady=5)
mHostMail = Entry(mFrame, width=30, justify="left",font=("Arial Rounded MT Bold",8),textvariable=hostMail)
mHostMail.grid(row=11,column=1,sticky="w",pady=5)

Label(mFrame, text="Puerto:",fg="red",font=("Arial Rounded MT Bold",10)).grid(row=12,column=0,sticky="e",pady=5)
mPortMail = Entry(mFrame, width=30,justify="left",font=("Arial Rounded MT Bold",8),textvariable=portMail)
mPortMail.grid(row=12,column=1,sticky="w",pady=5)

btEnviar = Button(mFrame,text="Enviar Reporte",width=30,bg="chartreuse2",relief="groove",command=send_email)
btEnviar.grid(row=6,column=3,columnspan=2,pady=5)


root.mainloop()


