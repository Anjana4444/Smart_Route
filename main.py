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


        algo_frame= tk.LabelFrame(self.root, text="Pathfinding & Graph Algorithms",ng=PANEL,fg=ACCENT,padx=12,pady=12,font=("Helvetica",10,"bold"))
        algo_frame.pack(fill="x",padx=20,pady=10)

        ttk.Button(algo_frame, text="Shortest (Dijkstra)", style="Accent.TButton", command=self.find_shortest_path).grid(row=0, column=0, padx=10, pady=8)
        ttk.Button(algo_frame, text="A* Path", style="Accent.TButton", command=self.find_a_star_path).grid(row=0, column=1, padx=10, pady=8)
        ttk.Button(algo_frame, text="Compare Dijkstra vs A*", style="Ghost.TButton", command=self.compare_algorithms).grid(row=0, column=2, padx=10, pady=8)
        ttk.Button(algo_frame, text="BFS", style="Accent.TButton", command=self.find_bfs_path).grid(row=1, column=0, padx=10, pady=8)
        ttk.Button(algo_frame, text="DFS", style="Accent.TButton", command=self.find_dfs_path).grid(row=1, column=1, padx=10, pady=8)
        ttk.Button(algo_frame, text="Prim's MST", style="Accent.TButton", command=self.find_mst).grid(row=1, column=2, padx=10, pady=8)
        ttk.Button(algo_frame, text="Kruskal's MST", style="Accent.TButton", command=self.find_kruskal_mst).grid(row=1, column=3, padx=10, pady=8)

        traffic_frame = tk.LabelFrame(self.root, text="Traffic Control & Visualization", bg=PANEL, fg=ACCENT, padx=12, pady=12,font=("Helvetica", 10, "bold"))
        traffic_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(traffic_frame, text="Traffic Mode:", fg=TEXT, bg=PANEL).grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.traffic_mode = ttk.Combobox(traffic_frame, values=["Light", "Moderate", "Heavy"], state="readonly", width=12)
        self.traffic_mode.current(0)
        self.traffic_mode.grid(row=0, column=1, padx=10, pady=6)

        ttk.Button(traffic_frame, text="🚦 Simulate Traffic", style="Accent.TButton", command=self.simulate_traffic).grid(row=0, column=2, padx=10, pady=6)
        ttk.Button(traffic_frame, text="🔄 Reset Traffic", style="Accent.TButton", command=self.reset_traffic).grid(row=0, column=3, padx=10, pady=6)
        ttk.Button(traffic_frame, text="🌐 Visualize Graph", style="Ghost.TButton", command=self.visualize_graph).grid(row=0, column=4, padx=10, pady=6)

        console_frame = tk.Frame(self.root, bg=PANEL, padx=8, pady=8)
        console_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.output = tk.Text(console_frame, bg=OUTPUT_BG, fg=TEXT, insertbackground=TEXT,font=("Consolas", 10), wrap="word")
        self.output.pack(fill="both", expand=True)
        self.output.tag_config("info", foreground=TEXT)
        self.output.tag_config("success", foreground=SUCCESS)
        self.output.tag_config("warn", foreground=WARN)
        self.output.tag_config("error", foreground=ERR)

        status = tk.Frame(self.root, bg="#0C0C0E", height=24)
        status.pack(fill="x", side="bottom")
        self.status_label = tk.Label(status, text="Status: Ready", bg="#0C0C0E", fg="#AAAAAA", anchor="w", padx=10)
        self.status_label.pack(fill="x")

    def _log(self, msg, tag="info"):
        self.output.insert(tk.END, msg + "\n", tag)
        self.output.see(tk.END)
        self.status_label.config(text=f"Status: {msg}")

    def add_route(self):
        frm, to, dist = self.entry_from.get().strip(), self.entry_to.get().strip(), self.entry_distance.get().strip()
        if not (frm and to and dist):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        try:
            dist = float(dist)
        except ValueError:
            messagebox.showerror("Error", "Distance must be a number!")
            return
        
        self.graph.add_route(frm, to, dist)
        self._log(f"✅ Added route: {frm} ↔ {to} = {dist:.2f} km", "success")

        self.entry_from.delete(0, tk.END)
        self.entry_to.delete(0, tk.END)
        self.entry_distance.delete(0, tk.END)

    def view_routes(self):
        routes = self.graph.get_all_routes()
        self._log("\n--- All Routes ---", "info")
        for frm, to, dist in routes:
            self._log(f"{frm} ↔ {to} = {dist} km", "info")

    def _get_avg_speed(self):
        mode = self.traffic_mode.get()
        if mode == "Light":
            return 70
        elif mode == "Moderate":
            return 50
        else:
            return 35
        
    def _get_traffic_factor(self):
        mode = self.traffic_mode.get()
        if mode == "Light":
            return 1.1
        elif mode == "Moderate":
            return 1.3
        else:
            return 1.6
        
    def find_shortest_path(self):
        frm, to = self.entry_from.get().strip(), self.entry_to.get().strip()
        if not (frm and to):
            messagebox.showerror("Error", "Enter both cities!")
            return
        path, distance = self.graph.dijkstra(frm, to)
        if not path:
            self._log("⚠️ No path found!", "warn")
            return
        time = self.graph.calculate_travel_time(distance, self._get_avg_speed())
        self._log(f"\n[Dijkstra] {frm} → {to}\nPath: {' → '.join(path)}\nDistance: {distance:.2f} km\nEstimated Time: {time}", "info")
        self.graph.visualize_graph(highlight_path=path)

    def find_a_star_path(self):
        frm, to = self.entry_from.get().strip(), self.entry_to.get().strip()
        if not (frm and to):
            messagebox.showerror("Error", "Enter both cities!")
            return
        path, distance = self.graph.a_star(frm, to)
        if not path:
            self._log("⚠️ No path found!", "warn")
            return
        time = self.graph.calculate_travel_time(distance, self._get_avg_speed())
        self._log(f"\n[A*] {frm} → {to}\nPath: {' → '.join(path)}\nDistance: {distance:.2f} km\nEstimated Time: {time}", "info")
        self.graph.visualize_graph(highlight_path=path)



                            
        

    


            

