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

    


            

