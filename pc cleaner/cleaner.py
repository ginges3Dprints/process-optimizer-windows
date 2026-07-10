import os
import sys
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk
import psutil

IGNORE_PROCESSES = {
    "explorer.exe", "taskmgr.exe", "svchost.exe", "services.exe", 
    "lsass.exe", "wininit.exe", "csrss.exe", "smss.exe", 
    "winlogon.exe", "spoolsv.exe", "dwm.exe", "ctfmon.exe", 
    "conhost.exe", "sihost.exe", "shellexperiencehost.exe", 
    "startmenuexperiencehost.exe", "searchhost.exe", 
    "nvdisplay.container.exe", "amdfvr.exe", "igfxcuiservice.exe", 
    "runtimebroker.exe", "onedrive.exe"
}

DEFAULT_SAFE = {
    "chrome.exe", "msedge.exe", "firefox.exe", "spotify.exe", 
    "discord.exe", "steam.exe", "steamwebhelper.exe", "notepad.exe", 
    "vlc.exe", "teams.exe", "slack.exe"
}

class UltimatePowerCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Master Pro - Process Optimizer")
        self.root.geometry("950x620")
        self.root.configure(bg="#f5f6fa")
        
        # --- SPANNER ICON PATHING LOADER ---
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(__file__)
            
            icon_path = os.path.join(base_path, "spanner.ico")
            self.root.iconbitmap(icon_path)
        except Exception:
            pass 
        # -----------------------------------

        self.user_whitelist = set()
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.safe_apps = {}
        self.unknown_apps = {}
        self.selected_process_name = ""  
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        self.main_tab = tk.Frame(self.notebook, bg="#f5f6fa")
        self.settings_tab = tk.Frame(self.notebook, bg="#ffffff")
        
        self.notebook.add(self.main_tab, text=" Dashboard ")
        self.notebook.add(self.settings_tab, text=" Custom Whitelist Settings ")
        
        self.create_main_widgets()
        self.create_settings_widgets()

    def create_main_widgets(self):
        header = tk.Frame(self.main_tab, bg="#2c3e50", height=50)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        tk.Label(header, text="Task Master Pro Optimizer", fg="white", bg="#2c3e50", font=("Segoe UI", 12, "bold")).pack(side="left", padx=15, pady=12)
        
        body_frame = tk.Frame(self.main_tab, bg="#f5f6fa")
        body_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # LEFT COLUMN: Scrollable lists
        left_frame = tk.Frame(body_frame, bg="#f5f6fa")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.canvas = tk.Canvas(left_frame, borderwidth=0, background="#f5f6fa")
        self.scroll_frame = tk.Frame(self.canvas, background="#f5f6fa")
        self.scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", tags="self.scroll_frame")
        self.scroll_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.safe_group = ttk.LabelFrame(self.scroll_frame, text=" ✔ Verified / Safe Programs ")
        self.safe_group.pack(fill="x", padx=5, pady=5)
        self.safe_container = tk.Frame(self.safe_group, bg="#ffffff")
        self.safe_container.pack(fill="x", padx=5, pady=5)
        
        self.unknown_group = ttk.LabelFrame(self.scroll_frame, text=" ⚠ Background Items / Potential Junk ")
        self.unknown_group.pack(fill="x", padx=5, pady=5)
        self.unknown_container = tk.Frame(self.unknown_group, bg="#ffffff")
        self.unknown_container.pack(fill="x", padx=5, pady=5)
        
        # MIDDLE COLUMN: Process Inspector (Width rule assigned on creation line properly)
        middle_frame = ttk.LabelFrame(body_frame, text=" Process Inspector & Smart Search ", width=260)
        middle_frame.pack(side="left", fill="both", padx=5)
        middle_frame.pack_propagate(False)
        
        self.inspect_text = tk.Text(middle_frame, height=12, bg="#f1f2f6", font=("Segoe UI", 9), state="disabled", wrap="word")
        self.inspect_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.search_btn = ttk.Button(middle_frame, text="🔍 Google This Process", command=self.google_process, state="disabled")
        self.search_btn.pack(fill="x", padx=5, pady=5)
        
        # RIGHT COLUMN: Consoles and Control actions
        right_frame = tk.Frame(body_frame, bg="#f5f6fa", width=240)
        right_frame.pack(side="right", fill="both", padx=(5, 0))
        right_frame.pack_propagate(False)
        
        tk.Label(right_frame, text="Activity Console", bg="#f5f6fa", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.log_box = tk.Text(right_frame, height=10, bg="#ffffff", font=("Consolas", 9), state="disabled")
        self.log_box.pack(fill="both", expand=True, pady=(0, 10))
        
        self.scan_btn = ttk.Button(right_frame, text="1. Scan Active Processes", command=self.scan_pc)
        self.scan_btn.pack(fill="x", pady=2)
        
        self.autoclean_btn = ttk.Button(right_frame, text="⚡ Auto-Clean Unneeded Processes", command=self.auto_clean_junk, state="disabled")
        self.autoclean_btn.pack(fill="x", pady=2)
        
        self.close_btn = ttk.Button(right_frame, text="Kill Checked Elements Only", command=self.close_selected, state="disabled")
        self.close_btn.pack(fill="x", pady=2)

    def create_settings_widgets(self):
        settings_frame = tk.Frame(self.settings_tab, bg="#ffffff", padx=20, pady=20)
        settings_frame.pack(fill="both", expand=True)
        
        instructions = tk.Label(settings_frame, text="Add Trusted Process Names Manually:\nType its exact executable filename name below (e.g., mygame.exe) so the Auto-Cleaner skips it.", justify="left", bg="#ffffff", font=("Segoe UI", 10))
        instructions.pack(anchor="w", pady=(0, 10))
        
        input_frame = tk.Frame(settings_frame, bg="#ffffff")
        input_frame.pack(fill="x", pady=5)
        
        self.whitelist_entry = ttk.Entry(input_frame, font=("Segoe UI", 10), width=35)
        self.whitelist_entry.pack(side="left", padx=(0, 10))
        
        add_btn = ttk.Button(input_frame, text="Add to Whitelist", command=self.add_to_whitelist)
        add_btn.pack(side="left")
        
        tk.Label(settings_frame, text="Currently Configured Dynamic Safe Rules:", bg="#ffffff", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(15, 2))
        
        self.whitelist_box = tk.Listbox(settings_frame, height=12, font=("Segoe UI", 10))
        self.whitelist_box.pack(fill="both", expand=True, pady=5)
        
        remove_btn = ttk.Button(settings_frame, text="Remove Selected Rule", command=self.remove_from_whitelist)
        remove_btn.pack(anchor="e", pady=5)

    def log(self, message):
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")
        self.root.update()

    def update_inspector(self, info_text):
        self.inspect_text.config(state="normal")
        self.inspect_text.delete("1.0", tk.END)
        self.inspect_text.insert(tk.END, info_text)
        self.inspect_text.config(state="disabled")

    def show_process_details(self, proc, pid, name):
        self.selected_process_name = name
        self.search_btn.config(state="normal")
        try:
            exe_path = proc.exe()
            mem_info = proc.memory_info().rss / (1024 * 1024)
            details = f"NAME: {name}\n\nPID: {pid}\n\nRAM USAGE: {mem_info:.2f} MB\n\nDIRECTORY PATH:\n{exe_path}"
        except Exception:
            details = f"NAME: {name}\n\nPID: {pid}\n\nSTATUS:\nSystem Protected / Admin Access Required."
        self.update_inspector(details)

    def google_process(self):
        if self.selected_process_name:
            url = f"https://www.google.com/search?q={self.selected_process_name}"
            webbrowser.open(url)
            self.log(f"Opened web search for {self.selected_process_name}")

    def clear_ui(self):
        for widget in self.safe_container.winfo_children(): widget.destroy()
        for widget in self.unknown_container.winfo_children(): widget.destroy()
        self.safe_apps.clear()
        self.unknown_apps.clear()
        self.search_btn.config(state="disabled")
        self.selected_process_name = ""
        self.update_inspector("Click any process from the lists to view full location path, PID layout, RAM impact, or run a Google verification query.")

    def add_to_whitelist(self):
        text = self.whitelist_entry.get().strip().lower()
        if text:
            if text not in self.user_whitelist:
                self.user_whitelist.add(text)
                self.whitelist_box.insert(tk.END, text)
                self.whitelist_entry.delete(0, tk.END)
                messagebox.showinfo("Saved", f"'{text}' whitelisted.")
            else:
                messagebox.showwarning("Error", "Already whitelisted.")

    def remove_from_whitelist(self):
        selected = self.whitelist_box.curselection()
        if selected:
            item_text = self.whitelist_box.get(selected[0])
            self.user_whitelist.remove(item_text)
            self.whitelist_box.delete(selected[0])

    def scan_pc(self):
        self.scan_btn.config(state="disabled")
        self.clear_ui()
        self.log("=== Initializing Active Scan ===")
        
        current_pid = os.getpid()
        script_filename = os.path.basename(sys.executable).lower()
        base_script_name = os.path.basename(sys.argv[0]).lower()

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                p_info = proc.info
                p_name = p_info["name"]
                p_pid = p_info["pid"]

                if not p_name: continue
                p_name_lower = p_name.lower()

                # Self protection rules loop
                if (p_pid == current_pid or p_name_lower in ["python.exe", "pythonw.exe", script_filename, base_script_name, base_script_name.replace(".py", ".exe")]):
                    continue

                if p_name_lower in IGNORE_PROCESSES: continue

                var = tk.BooleanVar(value=False)
                def make_click_callback(p_obj=proc, p_id=p_pid, p_nm=p_name):
                    return lambda event: self.show_process_details(p_obj, p_id, p_nm)

                if p_name_lower in DEFAULT_SAFE or p_name_lower in self.user_whitelist:
                    row_frame = tk.Frame(self.safe_container, bg="#ffffff")
                    row_frame.pack(fill="x", padx=5, pady=1)
                    ttk.Checkbutton(row_frame, variable=var).pack(side="left")
                    lbl = tk.Label(row_frame, text=f"{p_name} (PID: {p_pid})", bg="#ffffff", anchor="w", cursor="hand2")
                    lbl.pack(side="left", fill="x", expand=True)
                    lbl.bind("<Button-1>", make_click_callback())
                    self.safe_apps[p_pid] = (p_name, proc, var)
                else:
                    row_frame = tk.Frame(self.unknown_container, bg="#ffffff")
                    row_frame.pack(fill="x", padx=5, pady=1)
                    ttk.Checkbutton(row_frame, variable=var).pack(side="left")
                    lbl = tk.Label(row_frame, text=f"⚠ {p_name} (PID: {p_pid})", bg="#ffffff", fg="#c0392b", anchor="w", cursor="hand2")
                    lbl.pack(side="left", fill="x", expand=True)
                    lbl.bind("<Button-1>", make_click_callback())
                    self.unknown_apps[p_pid] = (p_name, proc, var)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        self.log(f"Scan complete. Safe: {len(self.safe_apps)} | Flagged Junk: {len(self.unknown_apps)}")
        self.scan_btn.config(state="normal")
        if self.safe_apps or self.unknown_apps: self.close_btn.config(state="normal")
        if self.unknown_apps: self.autoclean_btn.config(state="normal")

    def auto_clean_junk(self):
        self.autoclean_btn.config(state="disabled")
        self.log("=== Running 1-Click Auto Clean ===")
        closed_count = 0
        total_ram_freed = 0.0
        
        for pid, (name, proc, var) in list(self.unknown_apps.items()):
            try:
                try:
                    ram_mb = proc.memory_info().rss / (1024 * 1024)
                except Exception:
                    ram_mb = 0.0
                
                proc.terminate()
                total_ram_freed += ram_mb
                self.log(f"Auto-Closed: {name}")
                closed_count += 1
            except Exception:
                pass
                
        self.log(f"Auto-Clean completed! Stopped {closed_count} items.")
        self.log(f"✨ Total Recovered RAM: {total_ram_freed:.2f} MB")
        self.clear_ui()
        messagebox.showinfo("Optimization Complete", f"Wiped out {closed_count} background tasks.\nRecovered {total_ram_freed:.2f} MB of system memory!")

    def close_selected(self):
        self.close_btn.config(state="disabled")
        self.log("=== Terminating Checked Items ===")
        closed_count = 0
        all_tracked = list(self.safe_apps.items()) + list(self.unknown_apps.items())
        for pid, (name, proc, var) in all_tracked:
            if var.get():
                try:
                    proc.terminate()
                    self.log(f"Closed: {name}")
                    closed_count += 1
                except Exception:
                    pass
        self.log(f"Action Finished. Stopped {closed_count} items.")
        self.clear_ui()
        messagebox.showinfo("Done", f"Terminated {closed_count} checked applications.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimatePowerCleaner(root)
    root.mainloop()