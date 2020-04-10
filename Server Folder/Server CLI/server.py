from socket import socket, gethostname,SOL_SOCKET,SO_REUSEADDR,error,AF_INET,SOCK_STREAM
import sys
import os
import platform
from pathlib import Path 
import threading
from _thread import *
from tkinter import *
import time
from subprocess import Popen, PIPE, STDOUT
import contextlib
import shutil 
n = 0
all_connections=[]
all_addresses=[]
allowed_clients=['127.0.0.1', '192.168.3.102', '192.168.1.110', '192.168.1.111']

def set_allow_clients():
  global allowed_clients
  allow_client = input('Allow client ip: ')
  allowed_clients.append(allow_client)

#Create a socket
def create_socket():
  global server
  global host
  global port
  try:  
    host = "192.168.3.111"
    port = 3399
    server  = socket(AF_INET,SOCK_STREAM)
    server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
  except error as socket_error:
    print("Socket Creation Error :"  ,socket_error)

#Binding the socket and listening for connections
def bind_socket():
  try: 
    global server
    global host
    global port
    print("[*] Binding the port :",str(port))
    server.bind((host,port))
    print('[*] Listening...')
    server.listen(10)
    establish_multiple_clients_connections(server)
  except error as socket_error:
    print("Socket Creation Error :"  ,socket_error +"\n"+"Retrying...") 
  bind_socket()


def delete_particular_connection_from_list(conn):
  conn.close()
  all_connections.remove(conn)
  #establish_multiple_clients_connections(server)


#Establish multiple clients connection and passing them to thread
def establish_multiple_clients_connections(server):
  try:
    global allowed_clients
    while True:
      print(all_connections,'Exsisting connections')
      # blocking call, waits to accept a connection
      conn, address = server.accept()
      print(conn, "This is connection object")
      
      if conn.getpeername()[0] in allowed_clients:
        if conn in all_connections:
          pass
        else:
          all_connections.append(conn)
        print("[*] Total Connections",len(all_connections))
        print("[*] Connection has been extablished : ","IP Address: ",address[0]," Port:",address[1])
        conn.send('AUTHORIZED'.encode())
        
        data=conn.recv(1024)
        choice=data.decode()
        start_new_thread(client_thread, (conn,address,choice,))
        print(threading.activeCount(), "number of threads")
      else:
        conn.send('UNAUTHORIZED'.encode())
        conn.close()
  except:
    print("[*] Connection is closed by the client")

#used to receive file from client 
def file_receiver_function(conn,server,choice):
    path_of_file = conn.recv(1024)
    print(path_of_file,"Path of file")
    filename_w_ext = os.path.basename(path_of_file)
    print(filename_w_ext,"Ye file hay with extension")
    filename, file_extension = os.path.splitext(filename_w_ext)
    decoded_filename=filename.decode()
    decoded_file_extension=file_extension.decode()
    print(decoded_filename)

    n=0
    check=True
    if check == True:
      while check:
        print("Starting to read bytes..")
        buffer = conn.recv(1024)
        print(buffer,"Ye raha asal buffer")
        with open(decoded_filename+decoded_file_extension, "wb") as video:
            n += 1
            i = 0
            while buffer:                
                video.write(buffer)
                print("buffer {0}".format(i))
                i += 1
                buffer = conn.recv(1024)
        print("Done reading bytes..")
        check= False
        break
      all_connections.remove(conn)
      conn.close()
      time.sleep(10)

#used to receive command from client       
def command_receiver_function(conn,server,choice):
  try:
    print("[*] Waiting for command line execution")
    current_working_directory = os.getcwd() + ">"
    data = conn.recv(4096)
    if b'sendfile' in data:
      file_receiver_function(conn,server,choice)
    if data.decode('UTF-8') == 'quit':
      print("[*] Connection is closed by the client")
      delete_particular_connection_from_list(conn)
    if data[:2].decode('UTF-8') == 'cd' or data[:2].decode('UTF-8') =='CD':
      print("This command is not supported")
      delete_particular_connection_from_list(conn)
    if not b'sendfile' in data:
      command = data.decode('UTF-8')
      cmd = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
      output_byte  = cmd.stdout.read()
      output_str = str(output_byte,'utf-8')
      current_working_directory = os.getcwd() + ">"
      conn.send(str.encode(output_str + current_working_directory +'\n'))
      print("[*] Connection is closed for current")
      delete_particular_connection_from_list(conn)      
      #command_receiver_function(conn,server,choice)  
  except:
    print("[*] Connection is closed by the client")
    delete_particular_connection_from_list(conn)
    pass    
  
def directory_receiver_function(conn,server,choice):
    directory = os.getcwd()
    
    dir_list = os.listdir(directory)
  
    # Loop and add files to list.
    pairs = []
    for file in dir_list:
  
      # Use join to get full file path.
      location = os.path.join(directory, file)
  
      # Get size and add to list of tuples.
      size = os.path.getsize(location)
      pairs.append((size, file))
  
    # Sort list of tuples by the first element, size.
    pairs.sort(key=lambda s: s[0])
  
    # Display pairs.
    for pair in pairs:
      print(pair)
      
    import pickle
    
    pair_tuple = pickle.dumps(pairs)

    conn.send(pair_tuple)
    delete_particular_connection_from_list(conn)    


def client_thread(conn,server,choice):
  if choice == "1":
    file_receiver_function(conn,server,choice)
  elif choice =="2":
    command_receiver_function(conn,server,choice)
  elif choice =="3":
    directory_receiver_function(conn,server,choice)  

create_socket()
bind_socket()
