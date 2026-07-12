#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
# GUI module updated for Task Master Pro - 2026

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path

_location = os.path.dirname(__file__)
import cleaner_support

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.'''
        top.geometry("1315x560+300+200")
        top.minsize(176, 1)
        top.maxsize(1924, 1050)
        top.resizable(True, True)
        top.title("Task Master Pro")
        top.configure(background="#2b2b2b")

        self.top = top
        self.combobox = tk.StringVar()
        self.che73 = tk.IntVar()

        # Master Theme Styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # --- COMPACT TEXT ADJUSTMENTS FOR TABLES & BUTTONS ---
        self.style.configure('Treeview.Heading', font=("Segoe UI", 8, "bold"))
        self.style.configure('Treeview', font=("Segoe UI", 8), rowheight=18)
        self.style.configure('TButton', font=("Segoe UI", 7, "bold"))
        
        self.style.configure('.', background="#2b2b2b", foreground="#ffffff", font=("Segoe UI", 10))
        self.style.configure('TNotebook', background="#2b2b2b", borderwidth=0)
        self.style.configure('TNotebook.Tab', background="#3e3e3e", foreground="#ffffff", padding=[15, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#4a4a4a')], foreground=[('selected', '#ffffff')])

        # Master Notebook Container
        self.TNotebook_all = ttk.Notebook(self.top)
        self.TNotebook_all.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ------------------ TAB 1: DASHBOARD ------------------
        self.TNotebook_all_Dask = tk.Frame(self.TNotebook_all, bg="#2b2b2b")
        self.TNotebook_all.add(self.TNotebook_all_Dask, text=" Dashboard ")

        self.Label_header = tk.Label(self.TNotebook_all_Dask, text="Task Master Pro Engine", font=("Segoe UI", 16, "bold"), bg="#2b2b2b", fg="#ffffff")
        self.Label_header.place(relx=0.03, rely=0.02)

        # Safe Programs List View
        self.Label_Safe = tk.Label(self.TNotebook_all_Dask, text="Verified / Safe Processes", bg="#2b2b2b", fg="#5cb85c", font=("Segoe UI", 10, "bold"))
        self.Label_Safe.place(relx=0.03, rely=0.10)
        
        self.Scrolledtree_Safe = ScrolledTreeView(self.TNotebook_all_Dask)
        self.Scrolledtree_Safe.place(relx=0.03, rely=0.16, relheight=0.32, relwidth=0.45)
        self.Scrolledtree_Safe.configure(columns=("PID", "Memory"))
        self.Scrolledtree_Safe.heading("#0", text="Process Name", anchor=W)
        self.Scrolledtree_Safe.heading("PID", text="PID", anchor=W)
        self.Scrolledtree_Safe.heading("Memory", text="Memory (MB)", anchor=W)
        self.Scrolledtree_Safe.column("#0", width=180)
        self.Scrolledtree_Safe.column("PID", width=80)
        self.Scrolledtree_Safe.column("Memory", width=100)

        # Potential Junk List View
        self.Label_Junk = tk.Label(self.TNotebook_all_Dask, text="Background Items / Potential Junk", bg="#2b2b2b", fg="#d9534f", font=("Segoe UI", 10, "bold"))
        self.Label_Junk.place(relx=0.03, rely=0.52)
        
        self.Scrolledtree_Junk = ScrolledTreeView(self.TNotebook_all_Dask)
        self.Scrolledtree_Junk.place(relx=0.03, rely=0.58, relheight=0.36, relwidth=0.45)
        self.Scrolledtree_Junk.configure(columns=("PID", "Memory"))
        self.Scrolledtree_Junk.heading("#0", text="Process Name", anchor=W)
        self.Scrolledtree_Junk.heading("PID", text="PID", anchor=W)
        self.Scrolledtree_Junk.heading("Memory", text="Memory (MB)", anchor=W)
        self.Scrolledtree_Junk.column("#0", width=180)
        self.Scrolledtree_Junk.column("PID", width=80)
        self.Scrolledtree_Junk.column("Memory", width=100)

        # Inspector & Search Frame
        self.Label_inspector = tk.Label(self.TNotebook_all_Dask, text="Process Inspector Insights", bg="#2b2b2b", fg="#ffffff")
        self.Label_inspector.place(relx=0.51, rely=0.10)
        
        self.Scrolledtext_inspector = ScrolledText(self.TNotebook_all_Dask, bg="#1e1e1e", fg="#ffffff", insertbackground="white")
        self.Scrolledtext_inspector.place(relx=0.51, rely=0.16, relheight=0.32, relwidth=0.22)

        # Activity Terminal Output Console
        self.Label_console = tk.Label(self.TNotebook_all_Dask, text="System Activity Console", bg="#2b2b2b", fg="#ffffff")
        self.Label_console.place(relx=0.75, rely=0.10)
        
        self.Scrolledtext_console = ScrolledText(self.TNotebook_all_Dask, bg="#1e1e1e", fg="#00ff00", insertbackground="white")
        self.Scrolledtext_console.place(relx=0.75, rely=0.16, relheight=0.32, relwidth=0.22)

        # Control Station & Progress Gauges
        self.TProgressbar1 = ttk.Progressbar(self.TNotebook_all_Dask, orient="horizontal", mode="determinate")
        self.TProgressbar1.place(relx=0.51, rely=0.58, relwidth=0.46, height=20)

        # --- DIRECT INLINE FONT ENFORCEMENT TO SIZE 7 TO AVOID CLIPPING ---
        self.btn_scan = tk.Button(self.TNotebook_all_Dask, text="🔍 1. Scan Active Processes", bg="#0275d8", fg="white", font=("Segoe UI", 7, "bold"), command=lambda: cleaner_support.handle_scan(self))
        self.btn_scan.place(relx=0.51, rely=0.68, height=40, width=210)

        self.btn_clean = tk.Button(self.TNotebook_all_Dask, text="⚡ 2. Auto-Clean Background Junk", bg="#5cb85c", fg="white", font=("Segoe UI", 7, "bold"), command=lambda: cleaner_support.handle_clean(self))
        self.btn_clean.place(relx=0.75, rely=0.68, height=40, width=210)

        self.btn_kill = tk.Button(self.TNotebook_all_Dask, text="❌ Kill Target Selection Only", bg="#d9534f", fg="white", font=("Segoe UI", 7, "bold"), command=lambda: cleaner_support.handle_kill_selected(self))
        self.btn_kill.place(relx=0.51, rely=0.80, height=40, width=210)

        # ------------------ TAB 2: WHITELIST ------------------
        self.TNotebook_all_white = tk.Frame(self.TNotebook_all, bg="#2b2b2b")
        self.TNotebook_all.add(self.TNotebook_all_white, text=" Custom Whitelist ")

        lbl_entry = tk.Label(self.TNotebook_all_white, text="Enter Process Executable (e.g., spotify.exe):", bg="#2b2b2b", fg="white")
        lbl_entry.place(relx=0.03, rely=0.05)

        self.Entry_Whitelist = tk.Entry(self.TNotebook_all_white, bg="#3e3e3e", fg="white", insertbackground="white", font=("Segoe UI", 11))
        self.Entry_Whitelist.place(relx=0.03, rely=0.10, height=30, relwidth=0.40)

        self.Button_Add = tk.Button(self.TNotebook_all_white, text="➕ Add to Whitelist", bg="#5cb85c", fg="white", font=("Segoe UI", 7, "bold"), command=lambda: cleaner_support.add_whitelist_item(self))
        self.Button_Add.place(relx=0.45, rely=0.10, height=30, width=150)

        self.Button_Remove = tk.Button(self.TNotebook_all_white, text="➖ Remove Selected", bg="#d9534f", fg="white", font=("Segoe UI", 7, "bold"), command=lambda: cleaner_support.remove_whitelist_item(self))
        self.Button_Remove.place(relx=0.60, rely=0.10, height=30, width=150)

        self.Scrolledlist_WhiteLists = ScrolledListBox(self.TNotebook_all_white, bg="#1e1e1e", fg="white", font=("Segoe UI", 11))
        self.Scrolledlist_WhiteLists.place(relx=0.03, rely=0.20, relheight=0.70, relwidth=0.94)

        # ------------------ TAB 3: SETTINGS ------------------
        self.TNotebook_all_settings = tk.Frame(self.TNotebook_all, bg="#2b2b2b")
        self.TNotebook_all.add(self.TNotebook_all_settings, text=" Settings ")

        self.Label1 = tk.Label(self.TNotebook_all_settings, text="Global Application Theme Selection:", bg="#2b2b2b", fg="white")
        self.Label1.place(relx=0.03, rely=0.05)

        self.theme_dropdown = ttk.Combobox(self.TNotebook_all_settings, textvariable=self.combobox, state="readonly")
        self.theme_dropdown.place(relx=0.03, rely=0.10, height=30, relwidth=0.30)
        self.theme_dropdown['values'] = ('Dark Classic', 'Light Modern', 'Cyberpunk Amber')
        self.theme_dropdown.bind("<<ComboboxSelected>>", lambda e: cleaner_support.apply_theme_change(self))

        self.Checkbutton_StartUp = tk.Checkbutton(self.TNotebook_all_settings, text="Enable Automation Sweep on Startup", variable=self.che73, bg="#2b2b2b", fg="white", activebackground="#2b2b2b", activeforeground="white", selectcolor="#2b2b2b")
        self.Checkbutton_StartUp.place(relx=0.03, rely=0.22)

        self.btn_Apply = tk.Button(self.TNotebook_all_settings, text="Save Settings Config", bg="#0275d8", fg="white", font=("Segoe UI", 7, "bold"), command=lambda: cleaner_support.save_config_state(self))
        self.btn_Apply.place(relx=0.03, rely=0.35, height=35, width=160)

        # Complete post-initialization setups via support module hooks
        cleaner_support.init_backend_logic(self)

# --- PAGE Custom Class Wrappers for Autoscrolling Component Modules ---
class AutoScroll(object):
    def __init__(self, master):
        try: vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except: pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try: self.configure(yscrollcommand=self._autoscroll(vsb))
        except: pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try: vsb.grid(column=1, row=0, sticky='ns')
        except: pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1: sbar.grid_remove()
            else: sbar.grid()
            sbar.set(first, last)
        return wrapped

def _create_container(func):
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledListBox(AutoScroll, tk.Listbox):
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

def start_up():
    cleaner_support.main()

if __name__ == '__main__':
    # Force PyInstaller to look in the correct directory for config/icon files
    import os, sys
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(__file__))
        
    cleaner_support.main()