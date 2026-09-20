import socket
import time

target_host = "0.0.0.0"
target_port = 9999

#creating socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connecting the client
client.connect((target_host, target_port))
#sending data
a=0
while a<10:
    client.send("how cool".encode())
    #receiving the data 
    response = client.recv(4096)
    print(response.decode())
    time.sleep(1)
    a+=1