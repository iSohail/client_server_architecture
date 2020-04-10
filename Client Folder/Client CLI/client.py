
import socket
from threading import Thread
import threading
import pathlib
import os
import time


def connect_client():
  global host
  global port
  global client
  host = "127.0.0.1"
  port = 3399
  client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  client.connect((host,port))
  print("[*] Connection has been extablished with server")
  transfer(client)

def send_file(client):
    global current_directory_path
    path_of_file = input(str("Please enter the path to send"))
    client.send(path_of_file.encode())
    path_of_file=path_of_file.replace('\\','/')
    with open(path_of_file, "rb") as video:
        buffer = video.read()
        print(buffer)
        client.sendall(buffer)
        print("Done sending..")
    print("File Transfered and received by server")
    print(current_directory_path,"changes occuredddddddd")

    client.close()
    connect_client()
        

def send_commands(client):
  global ekor
  sent_to_server = input(str("[*] Please enter command to execute:"))
  if 'sendfile' in sent_to_server:
    print("send file hay client ki trf say")
    encoded_message = sent_to_server.encode()
    client.send(encoded_message)
    send_file(client)
  if not 'sendfile' in sent_to_server:
    if len(sent_to_server)>0:
      encoded_message = sent_to_server.encode()
      client.send(encoded_message)
      from_server=str(client.recv(4096),'utf-8')
      print(from_server,end = "")
      current_directory_path=from_server.splitlines()[-1]
      ekor = current_directory_path
      send_commands(client)
    else:
      send_commands(client)


def user_choice(client):
  global ekor
  choice = input("1:Send File:\n2:Send Commands:")
  client.send(choice.encode())
  if len(choice)>0:
    if choice == "1":
      send_file(client)      
    elif choice == "2":
      send_commands(client)
      
    else:
      client.connect((host,port))
      user_choice(client)
  else:
    user_choice(client)

def transfer(client):
  conti="start"
  if conti:
    user_choice(client)
connect_client()