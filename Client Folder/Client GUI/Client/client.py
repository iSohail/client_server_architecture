
import os
import sys
import platform
if sys.version_info.major == 3:
    
    import tkinter as tk, tkinter.font as tkFont
    from tkinter import messagebox
    from tkinter import ttk
else:
    import tkiner as tk
    import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox

# Sockets library
import socket
from threading import Thread
import threading
import pathlib

import time

LARGE_FONT= ("Verdana", 16)

def connect_client():
    global host
    global port
    global client
    print('connecting to server')
    host = "127.0.0.1"
    port = 3399
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,port))
    print("[*] Connection has been extablished with server")
    from_server=str(client.recv(1024),'utf-8')
    
    if from_server == 'UNAUTHORIZED':
        return '0'
    
    return '1'


def get_current_firectory_files(from_server):
    encoded_message = '2'.encode()
    client.send(encoded_message)
    time.sleep(0.5)
    from_server="dir"
    encoded_message = from_server.encode()
    client.send(encoded_message)
    from_server=str(client.recv(4096),'utf-8')
    current_path=from_server.splitlines()[-1]
    path=current_path
    client.close()
    connect_client()
    
def get_files():
    global path
    global client
    import pickle
    encoded_message = '3'.encode()
    client.send(encoded_message)
    time.sleep(0.1)
    recieve_server = client.recv(4096)
    print(recieve_server,"reciener")
    recieve_server = pickle.loads(recieve_server)
    client.close()
    connect_client()    
    return recieve_server
    



def get_current_dir(*args,**kwargs):
    global path
    print(platform.system())
    if '2' in args:
        if platform.system() == "Windows":
            encoded_message = '2'.encode()
            client.send(encoded_message)
            time.sleep(0.5)
            from_server="ipconfig"
            encoded_message = from_server.encode()
            client.send(encoded_message)
            from_server=str(client.recv(4096),'utf-8')
            current_path=from_server.splitlines()[-1]
            path=current_path
            client.close()
            connect_client()
            encoded_message = '2'.encode()
            client.send(encoded_message)
            time.sleep(0.5)
            from_server="dir"
            encoded_message = from_server.encode()
            client.send(encoded_message)
            from_server=str(client.recv(4096),'utf-8')
            current_directories=from_server
            remove_last_line=current_directories.splitlines()
            lines = remove_last_line[:-1]
            for directories in lines:
                print(directories)
            client.close()
            connect_client()
        elif platform.system()=="Linux" or platform.system()=="Ubuntu":    
            encoded_message = '2'.encode()
            client.send(encoded_message)
            time.sleep(0.5)
            from_server="ifconfig"
            encoded_message = from_server.encode()
            client.send(encoded_message)
            from_server=str(client.recv(4096),'utf-8')
            current_path=from_server.splitlines()[-1]
            path=current_path
            client.close()
            connect_client()
            encoded_message = '2'.encode()
            client.send(encoded_message)
            time.sleep(0.5)
            from_server="pwd"
            encoded_message = from_server.encode()
            client.send(encoded_message)
            from_server=str(client.recv(4096),'utf-8')
            current_directories=from_server
            remove_last_line=current_directories.splitlines()
            lines = remove_last_line[:-1]
            for directories in lines:
                print(directories)
            client.close()
            connect_client()
   
    else:
        path = args

    

class Main(ThemedTk):
    """
    Example that is used to create screenshots for new themes.
    """
    def __init__(self):
        ThemedTk.__init__(self, themebg=True)
        
        global path

        print(sys.version_info.major)
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_columnconfigure(0, weight=1)   
        
        self.frame1 = tk.Frame(self.container)
        self.frame1.grid_propagate(False)  
        self.frame1.grid(row=0)
        
        frame = tk.LabelFrame(self.frame1, text=" Login ", font=("Arial 9 bold"), padx=100,pady=15)
        frame.pack(padx=20,pady=20)
        tk.Label(frame, text = "Username", font=("Arial 9 bold")).pack()
        self.username = tk.Entry(frame, width=25, relief="flat",font=("Arial 10"))
        self.username.pack()
        tk.Label(frame, text = "Password", font=("Arial 9 bold")).pack()
        self.password = tk.Entry(frame, width=25, relief="flat", font=("Arial 10"))
        self.password.pack()
        tk.Label(frame, text = "").pack()
        b1=tk.Button(frame, text = "Login", padx=74, pady=5, font=("Arial 10 bold"), border=0, command= lambda: self.authorize()).pack()
        tk.Label(frame, text = "").pack()
        b2=tk.Button(frame, text = "Exit", padx=80, pady=5, font=("Arial 10 bold"), border=0).pack()
        tk.Label(frame, text = "").pack()        
        
    
    def authorize(self):
        username = str(self.username.get())
        password = str(self.password.get())
        
        authenticated_users = [('sohail', '123'),('hammad','123'), ('maaz', '123'), ('shahrukh','123')]
        if((username,password) in authenticated_users):
            self.frame1.grid_forget()
            self.frame1.destroy()
            self.start_app()
        else:
            print('dsfnas')
            messagebox.showwarning("warning","Warning")  
            
    
    def start_app(self):
        label_frame = tk.Frame(self.container, borderwidth=5, width=1366, height=60, highlightcolor="black", highlightthickness=2)
        label_frame.grid_columnconfigure(0, weight=1)
        
        label_frame.grid(row=0, column=0, columnspan=2)
        label_frame.grid_propagate(False) 
        label_frame.config(background="#f5f5f5")
        
        self.label = ttk.Label(label_frame, text="Current Directory", font=("Helvetica", 14, 'bold'))
        self.label.grid(row=0, column=0)
        self.label1 = ttk.Label(label_frame, text=str(path), font=("Helvetica", 12))
        self.label1.grid(row=1, column=0)
        
        
        label_frame_bottom = tk.Frame(self.container, borderwidth=5, width=1366, height=50, highlightcolor="black", highlightthickness=2)
        label_frame_bottom.grid_columnconfigure(0, weight=1)
        label_frame_bottom.grid(row=2, column=0, columnspan=2)
        label_frame_bottom.grid_propagate(False) 
        label_frame_bottom.config(background="#f5f5f5")
        
        self.label_bottom = ttk.Label(label_frame_bottom, text="Created by Logical4io", font=("Helvetica", 14, 'bold'))
        self.label_bottom.grid(row=0, column=0, pady=10)      
        
        files_frame = tk.Frame(self.container, borderwidth=5, width=500, height=570, highlightcolor="black", highlightthickness=2)
        files_frame.grid_columnconfigure(0, weight=1)
        files_frame.grid(row=1, column=1)
        files_frame.pack_propagate(False) 
        files_frame.config(background="#f5f5f5")   
               
        label_files = ttk.Label(files_frame, text="Files", font=("Helvetica", 12))
        label_files.pack(side="top", pady=10)        
        
        Files(files_frame).pack(side="left", fill="both", expand=False)
        
        menu = MenuBar(self.container, self)
        self.config(menu=menu.menu)
        
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(self.container, self)
            self.frames[F] = frame
            frame.config(background="white")
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame(StartPage)        
        
    def show_frame(self, cont):
        print("Show frame")
        frame = self.frames[cont]
        frame.tkraise()
        
class Files(tk.Frame):
    def __init__(self, root):
        print('scroll called')
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        
        self.frame = tk.Frame(self.canvas, background="#ffffff", borderwidth=0)
        self.vsb = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        
        self.populate()
        
       

    def populate(self):
        print('files running')
        '''Put in some fake data'''
        
        frame = tk.Frame(self.frame, background="#fff", height=30, width=463, padx=4, pady=4, highlightcolor="black", highlightthickness=1)
        frame.grid_propagate(False)         
        
        ttk.Label(frame, text=".", width=5, background="white").grid(row=0, column=0)
        t="Name"
        ttk.Label(frame, text=t, width=40, background="white").grid(row=0, column=1, sticky="nw")
        ttk.Label(frame, text="Size", width=10, background="white").grid(row=0, column=2, sticky="nw")
        frame.grid(row=0, column=0)
        
        files = get_files()
        for index, row in enumerate(files):
            frame = tk.Frame(self.frame, background="#fff", height=30, width=463, padx=4, pady=4, highlightcolor="black", highlightthickness=1)
            frame.grid_propagate(False)             
            print(row[0])
            ttk.Label(frame, text="%s" %  str(index+1), width=5, background="white").grid(row=index+1, column=0)
            t=row[1]
            ttk.Label(frame, text=t, width=40, background="white").grid(row=index+1, column=1)
            t1=row[0]
            ttk.Label(frame, text=t1, width=10, background="white").grid(row=index+1, column=2)                
            frame.grid(row=index+1, column=0)
        threading.Timer(60, self.populate).start()
 
    
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
class Outputs(tk.Frame):
    def __init__(self, root, output=None):
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, width=180, background="#ffffff")
        self.canvas.grid_propagate(False)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.frame = tk.Frame(self.canvas, background="#ffffff", pady=5, padx=5)
        self.vsb = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        
        self.populate(output)
    
    def populate(self, output):
        print('files running')
        '''Put in some fake data'''
        frame = tk.Frame(self.frame, background="#fff")
        sticky = {"sticky": "nswe"}
        if(output==None):
            ttk.Label(frame, text="Copy").grid(row=0, column=0, **sticky) 
        else:
            print('fdfs')
                       
        frame.grid(row=0, column=0, **sticky)    
    
    def populate(self):
        print('files running')
        '''Put in some fake data'''
        frame = tk.Frame(self.frame, background="#fff")
        sticky = {"sticky": "nswe"}
        ttk.Label(frame, text="Copy").grid(row=0, column=0, **sticky)           
                       
        frame.grid(row=0, column=0, **sticky)    

    
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class Commands(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, width=180, background="#ffffff")
        self.canvas.grid_propagate(False)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.frame = tk.Frame(self.canvas, background="#ffffff", pady=5, padx=5)
        self.vsb = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.populate()
    
    def populate(self):
        print('files running')
        '''Put in some fake data'''
        frame = tk.Frame(self.frame, background="#fff")
        sticky = {"sticky": "nswe"}
        ttk.Button(frame, text="Copy", width=16).grid(row=0, column=0, **sticky)
        ttk.Button(frame, text="Move").grid(row=1, column=0, **sticky)
        ttk.Button(frame, text="Make Dir").grid(row=2, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=4, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=5, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=6, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=7, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=8, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=9, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=10, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=11, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=12, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=13, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=14, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=15, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=16, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=17, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=18, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=19, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=20, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=21, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=22, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=23, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=24, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=25, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=26, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=27, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=28, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=29, column=0, **sticky)
        ttk.Button(frame, text="Replace").grid(row=30, column=0, **sticky)            
                       
        frame.grid(row=0, column=0, **sticky)    

    
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



class MenuBar(tk.Menu):
    def __init__(self, parent, controller):
        tk.Menu.__init__(self, parent)
        print(controller,"this is controller")
        self.menu = tk.Menu(self, tearoff=False)
        self.sub_menu = tk.Menu(self.menu, tearoff=False)
        self.sub_menu1 = tk.Menu(self.menu, tearoff=False)
        self.sub_menu.add_command(label="Exit", command=self.destroy)
        self.sub_menu1.add_command(label="GUI", command=lambda: controller.show_frame(PageTwo))
        self.sub_menu1.add_command(label="Shell", command=lambda: controller.show_frame(PageThree))
        self.menu.add_cascade(menu=self.sub_menu, label="File")
        self.menu.add_command(label="Home", command=lambda: controller.show_frame(StartPage))
        self.menu.add_command(label="File Transfer", command=lambda: controller.show_frame(PageOne))
        self.menu.add_cascade(label="Commands", menu=self.sub_menu1)

    def quit(self):
        sys.exit(0)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(pady=100)
        self.top_frame = tk.Frame(self, background="#f5f5f5", width=700, pady=10, padx=10)
        self.frame = tk.Frame(self.top_frame, background="#f5f5f5", height=200, width=700, pady=10)
        self.frame.grid_propagate(False)        
        
                
        
        self.label1 = ttk.Label(self, text="Welcome!", font=LARGE_FONT)

        self.button1 = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))


        self.button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))  
        
        
        self.button_test = ttk.Button(self.frame, text="Choose File",
                            command= lambda: self.get_file_path())         
                
        self.label_welcome = ttk.Label(self.top_frame, text="Welcome!", font=("Helvetica", 16, 'bold'))
        self.label_point_notes = ttk.Label(self.frame, text="Notes", font=("Helvetica", 14, 'bold'))
        self.label_point1 = ttk.Label(self.frame, text="-> This is point 1", font=("Helvetica", 14))
        self.dropdown = ttk.OptionMenu(self, tk.StringVar(), "First value", "Second Value")
        self.entry = ttk.Entry(self, textvariable=tk.StringVar(value="Default entry value."))
        self.button = ttk.Button(self, text="Button")
        self.radio_one = ttk.Radiobutton(self, text="Radio one", value=True)
        self.radio_two = ttk.Radiobutton(self, text="Radio two", value=False)
        self.scroll = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.checked = ttk.Checkbutton(self, text="Checked", variable=tk.BooleanVar(value=True))
        self.unchecked = ttk.Checkbutton(self, text="Unchecked")
        self.tree = ttk.Treeview(self, height=4, show=("tree", "headings"))
        self.setup_tree()
        self.scale_entry = ScaleEntry(self, from_=0, to=50, orient=tk.HORIZONTAL, compound=tk.RIGHT)
        self.combo = AutocompleteCombobox(self, completevalues=["something", "something else"])
        self.progress = ttk.Progressbar(self, maximum=100, value=50)
        # Grid widgets
        self.set_grid_widgets()
    
    def get_file_path(self):
        self.filepath = tk.filedialog.askopenfilename()
        print(self.filepath)
    
    def setup_tree(self):
        """Setup an example Treeview"""
        self.tree.insert("", tk.END, text="Example 1", iid="1")
        self.tree.insert("", tk.END, text="Example 2", iid="2")
        self.tree.insert("2", tk.END, text="Example Child")
        self.tree.heading("#0", text="Example heading")
    
    def set_grid_widgets(self):
        """Put widgets in the grid"""
        sticky = {"sticky": "nswe"}
        self.label_welcome.grid(row=0, column=0)
        self.label_point_notes.grid(row=0, column=0)
        self.label_point1.grid(row=1, column=0)
        self.button_test.grid(row=2, column=0)
        self.frame.grid(row=1, column=0)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
    
    def grid_widgets(self):
        """Put widgets in the grid"""
        sticky = {"sticky": "nswe"}
        self.button1.grid(row=0, column=1, columnspan=2, **sticky)
        self.button2.grid(row=1, column=1, columnspan=2, **sticky)
        self.label1.grid(row=1, column=1, columnspan=2, **sticky)
        self.dropdown.grid(row=2, column=1, **sticky)
        self.entry.grid(row=2, column=2, **sticky)
        self.button.grid(row=3, column=1, columnspan=2, **sticky)
        self.radio_one.grid(row=4, column=1, **sticky)
        self.radio_two.grid(row=4, column=2, **sticky)
        self.checked.grid(row=5, column=1, **sticky)
        self.unchecked.grid(row=5, column=2, **sticky)
        self.scroll.grid(row=1, column=3, rowspan=8, padx=5, **sticky)
        self.tree.grid(row=6, column=1, columnspan=2, **sticky)
        self.scale_entry.grid(row=7, column=1, columnspan=2, **sticky)
        self.combo.grid(row=8, column=1, columnspan=2, **sticky)
        self.progress.grid(row=9, column=1, columnspan=2, padx=5, pady=5, **sticky)
        
        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.filepath=''
        self.config(pady=100)
        
        self.frame = tk.Frame(self, background="#f5f5f5", height=300, width=700, pady=50, padx=10)
        self.frame.grid_propagate(False)    
        
        self.button_choose = ttk.Button(self.frame, text="Choose File",
                            command= lambda: self.get_file_path()) 
        self.button_transfer = ttk.Button(self.frame, text="Transer",
                            command= lambda: self.transfer_file())         
                
        self.source_path = tk.StringVar()
        if(self.filepath==''):
            self.source_path.set('No File Path Selected')
        self.source_file_path = ttk.Label(self.frame, text="Source file path", font=("Helvetica", 14, 'bold'))
        self.source_file_label = ttk.Label(self.frame, textvariable=self.source_path, font=("Helvetica", 14))        
        
        
        self.set_grid_widgets()
        
    def get_file_path(self):
        self.filepath = tk.filedialog.askopenfilename()
        if(len(self.filepath)>0):
            self.source_path.set(str(self.filepath))
        else:
            self.source_path.set('No File Path Selected')
        print(self.filepath)
        
    def transfer_file(self):
        global client
        client.send("1".encode())
        print(self.filepath,"this is source path")
        path_of_file = self.filepath
        client.send(path_of_file.encode())
        time.sleep(0.1)
        path_of_file=path_of_file.replace('\\','/')
        with open(path_of_file, "rb") as video:
            buffer = video.read()
            print(buffer)
            client.sendall(buffer)
            print("Done sending..")
        print("File Transfered and received by server")
        client.close()
        connect_client()     
                
        
    def set_grid_widgets(self):
        """Put widgets in the grid"""
        sticky = {"sticky": "nswe"}
        self.source_file_path.grid(row=0, column=0, **sticky)
        self.button_choose.grid(row=1, column=0, pady=5, sticky='w')
        self.source_file_label.grid(row=2, column=0, **sticky, pady=5)
        self.button_transfer.grid(row=5, column=0, pady=5, sticky='e')
        self.frame.grid(row=0, column=0)
        self.frame.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)    


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.top_frame = tk.Frame(self, background="#f5f5f5")
        self.frame_left = tk.Frame(self.top_frame,  borderwidth=5, background="#f5f5f5", height=570, width=200, highlightcolor="black", highlightthickness=2)
        self.frame_left.grid_propagate(False)
        self.frame_left.pack_propagate(False)
        self.frame_right = tk.Frame(self.top_frame,  borderwidth=5, background="#f5f5f5", height=570, width=666, highlightcolor="black", highlightthickness=2)
        self.frame_right.grid_propagate(False)        
        
        Commands(self.frame_left).pack(side="left", fill="both", expand=False)
        
        self.source_file_path = ttk.Label(self.frame_left, text="Copy", font=("Helvetica", 14, 'bold'))
        self.set_grid_widgets()
        
        
    def set_grid_widgets(self):
        """Put widgets in the grid"""
        sticky = {"sticky": "nswe"}
        self.frame_left.grid(row=0, column=0)
        self.frame_right.grid(row=0, column=1)  
        self.top_frame.grid(row=0, column=0)
        self.frame_left.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)    
    
        
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        self.top_frame = tk.Frame(self, background="#f5f5f5", height=570, padx=10, pady=10, width=866, borderwidth=5, highlightcolor="#d9d9d9", highlightthickness=2)
        self.top_frame.grid_propagate(False)
        self.input_frame = tk.Frame(self.top_frame, height=100, width=832, padx=5, pady=10, borderwidth=5, highlightcolor="#d9d9d9", background="#fff", highlightthickness=2)
        self.input_frame.grid_propagate(False)
        self.output_frame = tk.Frame(self.top_frame, height=436, width=832,  borderwidth=5, highlightcolor="#d9d9d9", background="#fff", highlightthickness=2)
        self.output_frame.grid_propagate(False)         
        
        self.label_command = ttk.Label(self.input_frame, text="Command", font=("Helvetica", 14, 'bold'))
        self.entry_command = ttk.Entry(self.input_frame, font=("Helvetica", 14, 'bold'))
        self.button_command = ttk.Button(self.input_frame, text="Send", command= lambda: self.send_command())
        
        self.label_output = ttk.Label(self.output_frame, text="Output", font=("Helvetica", 14, 'bold'))
        self.output_scroll_frame = tk.Frame(self.output_frame, background="#000")
        
        self.chatBox = ttk.Scrollbar(self.output_scroll_frame)
        self.chat = tk.Text(self.output_scroll_frame, height=23, wrap='word', state='disabled',
                    yscrollcommand=self.chatBox.set)
        self.chatBox.configure(command=self.chat.yview)
        
        self.set_output()
        
        self.set_grid_widgets()
        
    def send_command(self):
        global client
        global current_path
        print('i am runnning')
        encoded_message = "2".encode()
        client.send(encoded_message)        
        time.sleep(0.1)
        sent_to_server = self.entry_command.get()
        
        sent_to_server = sent_to_server.lstrip()
        check_before_sending = sent_to_server[0:2]
        
        if platform.system()=="Windows":
            check_before_sending = check_before_sending.lower()
            
        if check_before_sending == 'cd':
            self.set_output("This command is not supported")
            return
        
        if len(sent_to_server)>0:
            print(sent_to_server, "This command is sending")
            encoded_message = sent_to_server.encode()
            client.send(encoded_message)
            from_server=str(client.recv(4096),'utf-8')
            print(from_server, "Something fishy")
            self.set_output(from_server)
            
            client.close()
            connect_client()                 
    
    def set_output(self, text=''):
        text = '[*]'+ text
        self.chat.configure(state='normal')
        self.chat.insert('end', text + '\n')
        self.chat.configure(state='disabled')    
        
    def set_grid_widgets(self):
        """Put widgets in the grid"""
        sticky = {"sticky": "nswe"}
        self.label_command.grid(row=0, column=0, **sticky)
        self.entry_command.grid(row=1, column=0, **sticky)
        self.button_command.grid(row=1, column=1, **sticky)
        
        self.label_output.grid(row=0, column=0, **sticky)
        self.output_scroll_frame.grid(row=1, column=0, **sticky)
        
        self.chat.grid(row=0, **sticky)
        self.chatBox.grid(row=0, column=1, **sticky)                
        
        self.output_scroll_frame.rowconfigure(0, weight=1)
        self.output_scroll_frame.columnconfigure(0, weight=1)
        self.input_frame.grid(row=0, column=0) 
        self.input_frame.columnconfigure(0, weight=1)
        self.output_frame.grid(row=1, column=0) 
        self.output_frame.columnconfigure(0, weight=1)
        self.top_frame.grid(row=0, column=0)
        self.columnconfigure(0, weight=1)       
                        
        

if __name__ == '__main__':
    authorized = connect_client()
    if authorized == '1':
        print('helo')
        get_current_dir('2')
        main = Main()
        main.geometry('1366x768')
        main.set_theme("arc")
        main.mainloop()
    elif authorized == '0':
        root = tk.Tk()
        root.withdraw()        
        messagebox.showerror("Error","User Unauthorized for access")       
