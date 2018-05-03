import socket
import re
import base64

pattern = "[a-zA-Z0-9\.'{}_-]+@\w+\.\w+"
ip="127.0.0.1"
port=25

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((ip,port))


print (client.recv(4096))


snd=raw_input("[=>>]Enter the sender's mail address: ")
if not re.match(pattern,snd):  
    print ("[!!]Invalid address ")
    exit(0)
    
client.send("mail from: <%s>\n"%snd)

print (client.recv(4096))


rcv=raw_input("[=>>]Enter the reciever's mail address: ")
if not re.match(pattern,rcv): 
    print ("[!!]Invalid address ")
    exit(0)
    
client.send("rcpt to:<%s>\n"%rcv)

print (client.recv(4096))

client.send("data\n")
print (client.recv(4096))

path = raw_input("[==>]Enter the path of file to be attached: ")
print ("[=>>]Enter the Body of the Mail(don't forget full stop[.] at the end):")
d=''
datta=''
while 1:
    d=raw_input()
    datta+=d
    if d=='.':
        break
if path is not None:
    with open(path,"rb") as en_file:
        en_str= base64.b64encode(en_file.read())

header="MIME-Version: 1.0\n"    

header+="Content-Type: multipart/mixed;  boundary = front '\n"
header+="--front\n"
header+="content-type: text/plain\n"
header+=datta+"\n"
header+="--front\n"
header+="content-type: image/jpg; name='image0001.jpg'\n"
header+="Content-Transfer-Encoding: base64\n"
header+="Content-Disposition: attachment; filename='image001.jpg'\n"
header+=en_str+"\n"
header+="--front--\n"

client.send("%s\n.\n"%header)

print (client.recv(4096))
q=raw_input("Do you wanna quit(Y/n): ")
if q =='y' or q == 'Y':
    client.send("quit\n")
    print client.recv(4096)
else:
    print ("you have to quit no othe r option :P ")
