
import os
import sys
if sys.version_info.major == 3:
    
    import tkinter as tk, tkinter.font as tkFont
    from tkinter import ttk
else:
    import Tkinter as tk
    import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox

# Sockets library
import socket
from threading import Thread
import threading
import pathlib

import psutil
import cpuinfo as cp
import time

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

print(os.name)

#host = "192.168.0.102"
#port = 9999
#client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#client.connect((host,port))


LARGE_FONT= ("Verdana", 16)




class Main(ThemedTk):
    """
    Example that is used to create screenshots for new themes.
    """
    def __init__(self):
        ThemedTk.__init__(self, themebg=True)
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_columnconfigure(0, weight=1)
              
        
        label_frame = tk.Frame(container, borderwidth=5, width=1366, height=60, highlightcolor="black", highlightthickness=2)
        label_frame.grid_columnconfigure(0, weight=1)
        label_frame.grid(row=0, column=0, columnspan=2)
        label_frame.grid_propagate(False) 
        label_frame.config(background="#f5f5f5")
        
        current_path=os.getcwd()
        
        self.label = ttk.Label(label_frame, text="Current Path", font=("Helvetica", 14, 'bold'))
        self.label.grid(row=0, column=0)
        
        self.label1 = ttk.Label(label_frame, text=current_path, font=("Helvetica", 12))
        self.label1.grid(row=1, column=0)
        
        
        label_frame_bottom = tk.Frame(container, borderwidth=5, width=1366, height=50, highlightcolor="black", highlightthickness=2)
        label_frame_bottom.grid_columnconfigure(0, weight=1)
        label_frame_bottom.grid(row=2, column=0, columnspan=2)
        label_frame_bottom.grid_propagate(False) 
        label_frame_bottom.config(background="#f5f5f5")
        
        self.label_bottom = ttk.Label(label_frame_bottom, text="Created by Logical4io", font=("Helvetica", 14, 'bold'))
        self.label_bottom.grid(row=0, column=0, pady=10)      
        
        files_frame = tk.Frame(container, borderwidth=5, width=500, height=570, highlightcolor="black", highlightthickness=2)
        files_frame.grid_columnconfigure(0, weight=1)
        files_frame.grid(row=1, column=1)
        files_frame.pack_propagate(False) 
        files_frame.config(background="#f5f5f5")   
               
        label_files = ttk.Label(files_frame, text="Process", font=("Helvetica", 12))
        label_files.pack(side="top", pady=10)        
        
        Process(files_frame).pack(side="left", fill="both", expand=False)
        
        menu = MenuBar(container, self)
        self.config(menu=menu.menu)
        
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)
            self.frames[F] = frame
            frame.config(background="white")
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        print("Show frame")
        frame = self.frames[cont]
        frame.tkraise()
        
class Process(tk.Frame):
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
        
        frame = tk.Frame(self.frame, background="#fff", height=30, width=463, padx=4, pady=4, highlightcolor="black", highlightthickness=1)
        frame.grid_propagate(False) 
        
        ttk.Label(frame, text=".", width=5, background="white").grid(row=0, column=0)
        t="name"
        ttk.Label(frame, text=t, width=30, background="white").grid(row=0, column=1, sticky="nw")
        ttk.Label(frame, text="username", width=10, background="white").grid(row=0, column=2, sticky="nw") 
        ttk.Label(frame, text="pid", width=10, background="white").grid(row=0, column=3, sticky="nw") 
        frame.grid(row=0, column=0)
        
        # getting process details of server
        procs = {p.pid: p.info for p in psutil.process_iter(attrs=['name', 'username', 'pid'])}       
        
        for index, row in enumerate(procs):
            frame = tk.Frame(self.frame, background="#fff", height=30, width=463, padx=4, pady=4, highlightcolor="black", highlightthickness=1)
            frame.grid_propagate(False)            
            ttk.Label(frame, text="%s" % str(index+1), width=5, background="white").grid(row=index+1, column=0)
            t=procs[row]["name"]
            ttk.Label(frame, text=t, width=30, background="white").grid(row=index+1, column=1)
            t1=procs[row]["username"]
            ttk.Label(frame, text=t1, width=10, background="white").grid(row=index+1, column=2)  
            t2=procs[row]["pid"]
            ttk.Label(frame, text=t2, width=10, background="white").grid(row=index+1, column=3)              
            frame.grid(row=index+1, column=0)
    
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
        self.sub_menu.add_command(label="System information", command=lambda: controller.show_frame(PageTwo))
        self.sub_menu.add_command(label="Exit", command=self.destroy)
        self.menu.add_cascade(menu=self.sub_menu, label="File")
        self.menu.add_command(label="Home", command=lambda: controller.show_frame(StartPage))
        self.menu.add_command(label="Clients", command=lambda: controller.show_frame(PageOne))
        self.menu.add_cascade(label="Permission", command=lambda: controller.show_frame(PageThree))

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
        
        self.destination_file_path = ttk.Label(self.frame, text="Destination path", font=("Helvetica", 14, 'bold'))
        self.destination_file_entry = ttk.Entry(self.frame, font=("Helvetica", 14, 'bold'))
        
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
        self.destination_file_path.grid(row=3, column=0, **sticky, pady=5)
        self.destination_file_entry.grid(row=4, column=0, **sticky, pady=5)
        self.button_transfer.grid(row=5, column=0, pady=5, sticky='e')
        self.frame.grid(row=0, column=0)
        self.frame.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)    


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        info = cp.get_cpu_info()
        mem = psutil.virtual_memory()
        procs = {p.pid: p.info for p in psutil.process_iter(attrs=['pid'])} 
            
        
        
        self.top_frame = tk.Frame(self, background="#f5f5f5", pady=10, padx=10)
        note = ttk.Notebook(self.top_frame)
        
        tab1 = ttk.Frame(note)
        tab2 = ttk.Frame(note)
        tab3 = ttk.Frame(note)
        
        cpu_label = ttk.Label(tab1, text="Vendor:")
        cpu_label.grid(row=0, column=0, pady=(5,5))
        cpu_label1 = ttk.Label(tab1, text=info['brand'])
        cpu_label1.grid(row=0, column=1)        
        
        cpu_label = ttk.Label(tab1, text="Processor:")
        cpu_label.grid(row=1, column=0, pady=(5,5))
        cpu_label1 = ttk.Label(tab1, text=info['count'])
        cpu_label1.grid(row=1, column=1)   
        
        cpu_label = ttk.Label(tab1, text="Architecture:")
        cpu_label.grid(row=2, column=0, pady=(5,5))
        cpu_label1 = ttk.Label(tab1, text=info['arch'])
        cpu_label1.grid(row=2, column=1)           
        
        cpu_label = ttk.Label(tab1, text="CPU count:")
        cpu_label.grid(row=3, column=0, pady=(5,5))
        cpu_label1 = ttk.Label(tab1, text=info['count'])
        cpu_label1.grid(row=3, column=1)
        
        cpu_label = ttk.Label(tab1, text="No of process running:")
        cpu_label.grid(row=4, column=0, pady=(5,5))
        cpu_label1 = ttk.Label(tab1, text=str(len(procs)))
        cpu_label1.grid(row=4, column=1)
        
        cpu_label = ttk.Label(tab1, text="uptime:")
        cpu_label.grid(row=5, column=0, pady=(5,5))
        cpu_label1 = ttk.Label(tab1, text=str(psutil.cpu_times().user))
        cpu_label1.grid(row=5, column=1)
        
        cpu_label = ttk.Label(tab1, text="Cpu utilization:")
        cpu_label.grid(row=6, column=0, pady=(5,5))
        cpu_label1 = ttk.Label(tab1, text=str(psutil.cpu_percent(interval=1))+"%")
        cpu_label1.grid(row=6, column=1)
        
        
        
        note.add(tab1, text = "CPU")
        
        note.add(tab2, text = "Memory")
        memory_label = ttk.Label(tab2, text="total")
        memory_label.grid(row=0, column=0, pady=(5,5))
        memory_label1 = ttk.Label(tab2, text=str(bytes2human(mem.total))+"mb")
        memory_label1.grid(row=0, column=1)
        
        memory_label = ttk.Label(tab2, text="Available")
        memory_label.grid(row=1, column=0, pady=(5,5))
        memory_label1 = ttk.Label(tab2, text=str(bytes2human(mem.available))+"mb")
        memory_label1.grid(row=1, column=1)
        
        memory_label = ttk.Label(tab2, text="used")
        memory_label.grid(row=2, column=0, pady=(5,5))
        memory_label1 = ttk.Label(tab2, text=str(bytes2human(mem.used))+"mb")
        memory_label1.grid(row=2, column=1)
        
        memory_label = ttk.Label(tab2, text="Free")
        memory_label.grid(row=3, column=0, pady=(5,5))
        memory_label1 = ttk.Label(tab2, text=str(bytes2human(mem.free))+"mb")
        memory_label1.grid(row=3, column=1)
        
        memory_label = ttk.Label(tab2, text="Active")
        memory_label.grid(row=4, column=0, pady=(5,5))
        memory_label1 = ttk.Label(tab2, text=str(bytes2human(mem.active))+"mb")
        memory_label1.grid(row=4, column=1)
        
        memory_label = ttk.Label(tab2, text="Inactive")
        memory_label.grid(row=5, column=0, pady=(5,5))
        memory_label1 = ttk.Label(tab2, text=str(bytes2human(mem.inactive))+"mb")
        memory_label1.grid(row=5, column=1)
        
        memory_label = ttk.Label(tab2, text="Buffers")
        memory_label.grid(row=6, column=0, pady=(5,5))
        memory_label1 = ttk.Label(tab2, text=str(bytes2human(mem.buffers))+"mb")
        memory_label1.grid(row=6, column=1)
        
        
        note.add(tab3, text = "Disk")
        disk_label = ttk.Label(tab3, text="Disk Usage", font=("Helvetica", 12, 'bold'))
        disk_label.grid(row=0, column=0, pady=(5,5), padx=(5,5))
        disk_label1 = ttk.Label(tab3, text="Total", font=("Helvetica", 12, 'bold'))
        disk_label1.grid(row=0, column=1, pady=(5,5), padx=(5,5))
        disk_label2 = ttk.Label(tab3, text="Used", font=("Helvetica", 12, 'bold'))
        disk_label2.grid(row=0, column=2, pady=(5,5), padx=(5,5))  
        disk_label3 = ttk.Label(tab3, text="Free", font=("Helvetica", 12, 'bold'))
        disk_label3.grid(row=0, column=3, pady=(5,5), padx=(5,5))  
        disk_label4 = ttk.Label(tab3, text="Used %", font=("Helvetica", 12, 'bold'))
        disk_label4.grid(row=0, column=4, pady=(5,5), padx=(5,5))  
        disk_label5 = ttk.Label(tab3, text="Type", font=("Helvetica", 12, 'bold'))
        disk_label5.grid(row=0, column=5, pady=(5,5), padx=(5,5))    
        disk_label6 = ttk.Label(tab3, text="Mount", font=("Helvetica", 12, 'bold'))
        disk_label6.grid(row=0, column=6, pady=(5,5), padx=(5,5))            
        
        row=1
        for part in psutil.disk_partitions(all=False):
            if os.name == 'posix':
                if 'ext4' not in part.fstype:
                    print('this is working now')
                    continue
                if 'iso9660' in part.opts or part.fstype == '':
                    # skip cd-rom drives with no disk in it; they may raise
                    # ENOENT, pop-up a Windows GUI error for a non-ready
                    # partition or just hang.
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            disk_label = ttk.Label(tab3, text=part.device)
            disk_label.grid(row=row, column=0, pady=(5,5), padx=(5,5))
            disk_label1 = ttk.Label(tab3, text=bytes2human(usage.total))
            disk_label1.grid(row=row, column=1, pady=(5,5), padx=(5,5))
            disk_label2 = ttk.Label(tab3, text=bytes2human(usage.used))
            disk_label2.grid(row=row, column=2, pady=(5,5), padx=(5,5))  
            disk_label3 = ttk.Label(tab3, text=bytes2human(usage.free))
            disk_label3.grid(row=row, column=3, pady=(5,5), padx=(5,5))  
            disk_label4 = ttk.Label(tab3, text=str(int(usage.percent)))
            disk_label4.grid(row=row, column=4, pady=(5,5), padx=(5,5))  
            disk_label5 = ttk.Label(tab3, text=part.fstype)
            disk_label5.grid(row=row, column=5, pady=(5,5), padx=(5,5))    
            disk_label6 = ttk.Label(tab3, text=part.mountpoint)
            disk_label6.grid(row=row, column=6, pady=(5,5), padx=(5,5))   
            row=row+1
                
        note.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)
        
        self.top_frame.pack(expand=1, fill=tk.BOTH)
    
        
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
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
        
        #Outputs(self.output_scroll_frame).pack(side="left", fill="both", expand=False)
        
        self.chatBox = ttk.Scrollbar(self.output_scroll_frame)
        self.chat = tk.Text(self.output_scroll_frame, height=23, wrap='word', state='disabled',
                    yscrollcommand=self.chatBox.set)
        self.chatBox.configure(command=self.chat.yview)
        
        self.set_output()
        
        self.set_grid_widgets()
        
    def send_command(self):
        global client
        print('i am runnning')
        encoded_message = "2".encode()
        client.send(encoded_message)        
        time.sleep(0.1)
        sent_to_server = self.entry_command.get()
        
        if len(sent_to_server)>0:
            encoded_message = sent_to_server.encode()
            client.send(encoded_message)
            from_server=str(client.recv(4096),'utf-8')
            self.set_output(from_server)
            client.close()
            connect_client()            
        
        #from_server=str(client.recv(4096),'utf-8')
        #sent_to_server = str(self.entry_command.get())
        #print(sent_to_server)
        #if len(sent_to_server)>0:
            #encoded_message = sent_to_server.encode()
            #client.send(encoded_message)
            #from_server=str(client.recv(4096),'utf-8')
            #self.set_output(from_server)       
    
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
    main = Main()
    main.geometry('1366x768')
    main.set_theme("arc")
    main.mainloop()
