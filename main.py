import tkinter as tk
from tkinter import ttk, messagebox
from graph_manager import GraphManager

BG = "#0F111A"
PANEL = "#181A22"
ACCENT = "#00FFAA"
TEXT = "#EAEAEA"
OUTPUT_BG = "#151616"
SUCCESS = "#7CFC9A"
WARN = "#FFD166"
ERR = "#FF6B6B"

class SmartRouteApp:
    def __init__(self,root):
        self.root =root
        self.root.title("SmartRoute+ - Intelligent Path Finder")
        self.root.geometry("1080x720")
        self.root.config(bg=BG)

        self.graph = GraphManager()
        self._setup_styles()
        self._build_ui()
        self._log("Welcome to SmartRoute+","info")

    def _setup_styles(self):
        style =ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        style.configure("Header.TLabel", font=("Helvetica",26, "bold"),foreground=ACCENT, background=BG)
        style.configure("Sub.TLabel", font=("Helvetica", 12), foreground="#BEBEBE", background=BG)
        style.configure("Accent.TButton",font=("Helvetica",10,"bold"),padding=6,foreground=BG,background=PANEL,borderwidth=0)
        style.map("Ghost.TButton",background=[("active", "#1E1F28"), ("!disabled", PANEL)])

    def _build_ui(self):
        header =tk.Frame(self.root, bg=BG)
        header.pack(pady=(20,5))
        ttk.Label(header, text="🚗 SmartRoute+", style="Header.TLabel").pack()

        route_frame= tk.LabelFrame(self.root, text="Route Management", bg=PANEL, fg=ACCENT,padx=12, pady=10, font=("Helvetica",10,"bold"))
        route_frame.pack(fill="x", padx=20, pady=15)
        tk.Label(route_frame, text="From:", fg=TEXT, bg=PANEL).grid(row=0,column=0, padx=8,pady=6)
        self.entry_from= ttk.Entry(route_frame,width=18)
        self.entry_from.grid(row=0,column=1,padx=8,pady=6)

        tk.Label(route_frame, text="To:",fg=TEXT, bg=PANEL).grid(row=0,column=2,padx=8,pady=6)
        self.entry_to= ttk.Entry(route_frame, width=18)
        self.entry_to.grid(row=0,column=5,padx=8,pady=6)

        tk.Label(route_frame, text="Distance (km:)",fg=TEXT, bg=PANEL).grid(row=0,column=4,padx=8,pady=6)
        self.entry_distance= ttk.Entry(route_frame,width=10)
        self.entry_distance.grid(row=0,column=5,padx=8,pady=6)

        ttk.Button(route_frame,text="Add Route",style="Accent.TButton", command=self.add_route).grid(row=0, column=6, padx=10)
        ttk.Button(round, text="View Routes", style="Ghost.TButton",command=self.view_routes).grid(row=0, column=7, padx=10)


                            
        

    


            

