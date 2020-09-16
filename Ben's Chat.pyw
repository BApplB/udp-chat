#Ben's UDP Chat. Peer-to-peer networking, using UDP Broadcasts.
"""Ben's UDP Chat. Most of the code designed below was by Ben Appleby,
credit to Matthew Chaffé for developing the original server-based version
(UDP Sender/Reciever GUI) and Tkinter update algorithm.""" 
#--
from tkinter import *
import os
import socket
import datetime
varz=[]
users=[]
lastmessage=['']
ip = socket.gethostbyname(socket.gethostname())

if(os.path.isfile('config.conf')!=True and os.path.getsize("config.conf")==368):
    quit()
try:
    t=open('feed.log','r')
    t.read()
    t.close()
except UnicodeDecodeError:
    t=open('feed.log','w')
    t.write("           -==UDP Chat : MDES Encrypted==-")
    t.close()
    
#------------------------------------------------------------------------------------
"""MDES - Multiplicity Data Encryption System
String-based symmetric encryption algorithm designed by Ben Appleby"""

from random import randint
k0=[83,54,33,63,76,158,52,200,191,103,145,179,73,64,183,126]
k=[]
for i in range(len(k0)):
	k.append(k0[i]*int(datetime.datetime.now().day))
sigma=k[0]+k[1]+k[2]+k[3]+k[4]+k[5]+k[6]+k[7]+k[8]+k[9]+k[10]+k[11]+k[12]+k[13]+k[14]+k[15]
shift=0
shift2=k[0]
def f(x): return 1/2*x**3-5.542*x+5
def df(x): return 3/2*x**2-5.542

def setKeyChar(inKey):
    k=[]
    for i in range(0,len(inKey)):
        k.append(ord(inKey[i]))
    print("Assigned a ",len(inKey)+1," byte key")

def setKey(inKey):
    k=[]
    for i in range(0,len(inKey)):
        k.append(int(inKey[i]))
    print("Assigned a ",len(inKey)+1," byte key")
        
def newRaphson(x,inKey,tol=1.09e-9):
    for i in range(25):
        dx=(f(x)-inKey)/df(x)
        x=x-dx
        if abs(dx) <tol: return x,i
    print("Too many iterations! \n")


def encrypt(DataIn):
    daOut=[]
    for i in range(0,len(DataIn)):
        shift=k[i%16]
        root,numIter = newRaphson(2,shift)
        daOut.append(int('%05d'%((round(root*(sigma/shift)))*ord(DataIn[i]))))
        shift2=shift
    return str(daOut)
#----------------------------------------------------------------------------------


def helper(message, shift):
	message = message.lower()
	secret = ""
	for c in message:
		if c in "abcdefghijklmnopqrstuvwxyz":
			num = ord(c)
			num += shift
			if num > ord("z"):
				num -= 26
			elif num < ord("a"):
				num += 26
			secret = secret + chr(num)
		else:
			secret = secret + c
	return secret

BadList = helper(open("config.conf").read(),-3).splitlines()

def getDate():
    date=str("%02d" % datetime.datetime.now().day)+"/"+str("%02d" %datetime.datetime.now().month)+"-"+str("%02d" %datetime.datetime.now().hour)+":"+str("%02d" %datetime.datetime.now().minute)
    return date
def update(repeat = 500):
    t=open('feed.log','r')
    msg=t.read()
    lineList = t.readlines()
    if('/users\\' in msg):
        t=open('feed.log','wb')
        t.close()
        t=open('feed.log','w')
        t.write("           -==UDP Chat : MDES Encrypted==-")
        t.close()
        send_presence()
    t.close()
    msg_box.delete(0.0,END)
    msg_box.insert(0.0, msg)
    msg_box.see(END)
    root.after(repeat, update, repeat)
    
def send_message():
    name=varz[0]
    msg = send_box.get()
    for i in BadList:
            msg = msg.replace(i.lower(),'*' *len(i))
            msg= msg.replace(i.upper(),'*' *len(i))
    
    if msg==("/clear\\"):
        t=open('feed.log','wb')
        t.close()
        t=open('feed.log','w')
        t.write("           -==UDP Chat : MDES Encrypted==-")
        t.close()
    if (len(msg)and(msg!=lastmessage[0])):
        lastmessage.pop()
        lastmessage.append(msg)
        msg = getDate()+"  "+name + ": " + msg
        msg = encrypt(msg)
        data = bytes(msg, "utf-8")
        UDPsock.sendto(data, server_addr)
    send_box.delete(0, END)

def send_presence():
    name=varz[0]
    if name=='Ben':
        msg='--==*Ben is online*==-'
    else:
        msg = name+' is online. ('+ip+')'
    msg = encrypt(msg)
    data = bytes(msg, "utf-8")
    UDPsock.sendto(data, server_addr)

def return_message(event):
    name=varz[0]
    msg = send_box.get()
    for i in BadList:
            msg = msg.replace(i,'*' *len(i))
    if msg==("/clear\\"):
        t=open('feed.log','wb')
        t.close()
        t=open('feed.log','w')
        t.write("           -==UDP Chat : MDES Encrypted==-")
        t.close()
    if (len(msg)and(msg!=lastmessage[0])and(msg!="/clear\\")):
        lastmessage.pop()
        lastmessage.append(msg)
        msg = getDate()+"  "+name + ": " + msg
        msg = encrypt(msg)
        data = bytes(msg, "utf-8")
        UDPsock.sendto(data, server_addr)
    send_box.delete(0, END)

def callback():
    name=e.get()
    if not((len(name)>16) or (name=="" or 'ben' in name.lower())):
        for i in BadList:
            name = name.replace(i.lower(),'*' *len(i))
        if(name==helper('zbwyhjovj*',-7)):
            name='Ben'
        varz.append(name)
        root.attributes("-topmost",True)
        send_presence()
        t=open('feed.log','a')
        t.write("\n Welcome, type /clear\ to clear chat and / users \ to see who's online.")
        t.close()
        master.destroy()

def callback_enter(event):
    name=e.get()
    if not((len(name)>16) or (name=="" or 'ben' in name.lower())):
        for i in BadList:
            name = name.replace(i.lower(),'*' *len(i))
        if(name==helper('zbwyhjovj*',-7)):
            name='Ben'
        varz.append(name)
        root.attributes("-topmost",True)
        send_presence()
        t=open('feed.log','a')
        t.write("\n Welcome, type /clear\ to clear chat and / users \ to see who's online.")
        t.close()
        master.destroy()
        
#GUI Commands
def do_popup(event):
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        popup.grab_release()
        
def get_users():
    send_box.delete(0,END)
    send_box.insert(0,'/users\\')
    send_message()
def clear_chat():
    send_box.delete(0,END)
    send_box.insert(0,'/clear\\')
    send_message()
def cmd_pm():
    pass

def cmd_date():
    t=open('feed.log','a')
    t.write("\n ----Date: "+getDate()+"----")
    t.close()

def on_closing():
    t=open('feed.log','wb')
    t.write(os.urandom(4096))
    t.close()
    root.destroy()
       
#~~Main GUI and Initialization

port = 13000
buf = 1024
UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if hasattr(socket,'SO_BROADCAST'):
    UDPsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
host = '<broadcast>'
addr = (host, port)

os.startfile('UDPRx.pyw')

UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if hasattr(socket,'SO_BROADCAST'):
    UDPsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
server_addr = (host, port)

root = Tk()
master=Tk()
photo1 = PhotoImage(file="send.png")
#--
name="User"
doOnce=True
frame=Frame(master)
frame.pack()


master.title("Enter Username")
mahlabel = Label(frame,text="Enter Username: ",font=("Tw Cen MT", 10))
mahlabel.pack()
e = Entry(frame)
e.pack()
e.focus_set()

b = Button(frame, text = "OK", width = 10, command = callback,font=("Tw Cen MT", 12))
b.pack()
master.attributes("-topmost",True)
master.bind("<Return>", callback_enter)
#--
popup = Menu(root, tearoff=0)
#popup.add_command(label="Send a PM",command=cmd_pm) #TODO
popup.add_command(label="Get Time/Date",command=cmd_date)
popup.add_separator()
popup.add_command(label="Get Users",command=get_users)
popup.add_command(label="Clear Chat",command=clear_chat)




root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Button-3>", do_popup)
root.attributes('-alpha', 0.90)
root.resizable(0,0)
root.iconbitmap('icon.ico')
root.title("Ben's Chat")
root.geometry("400x250")
root.grid()
root.bind("<Return>", return_message)
send_box = Entry(root, width = 35,font=("Tw Cen MT", 10))
send_box.grid(row = 0, column = 0)
send_box.focus_set()
send_bttn = Button(root, text = "Send",image=photo1, command = send_message,font=("Tw Cen MT", 10),bg="#ADD8E6")
send_bttn.grid(row = 0, column = 1)
msg_box = Text(root, width = 43, height = 10,wrap=WORD,font=("Tw Cen MT", 10),highlightthickness=2, highlightbackground="#ADD8E6",bg="#CFE1E7")
msg_box.grid(row = 1, column = 0, columnspan = 2)

update()

root.mainloop()

        
