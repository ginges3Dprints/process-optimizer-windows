#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
# Support module for Task Master Pro - 2026

import sys
import os
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import psutil

# Core Configuration Persistence Path
CONFIG_FILE = "task_master_config.json"

# In-Memory Tracking Registry Array Maps
system_whitelist = ["explorer.exe", "taskmgr.exe", "svchost.exe", "python.exe", "cleaner.py"]
scanned_junk_pool = []
scanned_safe_pool = []

def main(*args):
    '''Main entry point for the application GUI framework loops.'''
    global root
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    
    import cleaner
    global _top1, _w1
    _top1 = root
    _w1 = cleaner.Toplevel1(_top1)
    root.mainloop()

def init_backend_logic(gui_instance):
    '''Fires immediately post-compilation to establish local environments.'''
    load_persistent_config(gui_instance)
    log_to_console(gui_instance, "System Initialization complete.\nReady for system optimization check.")
    gui_instance.Scrolledtext_inspector.insert(tk.END, "Click 'Scan Active Processes' to analyze running process footprints.")

# ------------------ ENGINE SYSTEM LOGIC FUNCTIONS ------------------

def log_to_console(gui, text_line):
    '''Helper to append timestamp lines straight into the Activity Console box.'''
    gui.Scrolledtext_console.configure(state=tk.NORMAL)
    gui.Scrolledtext_console.insert(tk.END, f">> {text_line}\n")
    gui.Scrolledtext_console.see(tk.END)
    gui.Scrolledtext_console.configure(state=tk.DISABLED)

def handle_scan(gui):
    '''Scans active Windows processes and splits them into lists based on the whitelist.'''
    global scanned_junk_pool, scanned_safe_pool
    scanned_junk_pool.clear()
    scanned_safe_pool.clear()
    
    # Reset Visual Tables
    for row in gui.Scrolledtree_Safe.get_children(): gui.Scrolledtree_Safe.delete(row)
    for row in gui.Scrolledtree_Junk.get_children(): gui.Scrolledtree_Junk.delete(row)
    
    log_to_console(gui, "Running background optimization diagnostic pass...")
    gui.TProgressbar1['value'] = 20
    gui.top.update_idletasks()
    
    all_processes = list(psutil.process_iter(['pid', 'name', 'memory_info']))
    gui.TProgressbar1['value'] = 60
    gui.top.update_idletasks()

    for proc in all_processes:
        try:
            pinfo = proc.info
            p_name = pinfo['name']
            p_pid = pinfo['pid']
            p_mem = round(pinfo['memory_info'].rss / (1024 * 1024), 2) if pinfo['memory_info'] else 0.0
            
            if p_name.lower() in [w.lower() for w in system_whitelist]:
                scanned_safe_pool.append((p_name, p_pid, p_mem))
                gui.Scrolledtree_Safe.insert("", tk.END, text=p_name, values=(p_pid, p_mem))
            else:
                scanned_junk_pool.append((p_name, p_pid, p_mem))
                gui.Scrolledtree_Junk.insert("", tk.END, text=p_name, values=(p_pid, p_mem))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    gui.TProgressbar1['value'] = 100
    log_to_console(gui, f"Scan Complete. Found {len(scanned_safe_pool)} Safe, {len(scanned_junk_pool)} Unprotected processes.")
    
    # Update Inspector with Overview Summary Metrics
    gui.Scrolledtext_inspector.delete("1.0", tk.END)
    gui.Scrolledtext_inspector.insert(tk.END, f"--- FOOTPRINT REPORT ---\nTotal Apps Run: {len(all_processes)}\n")
    total_junk_ram = sum(item[2] for item in scanned_junk_pool)
    gui.Scrolledtext_inspector.insert(tk.END, f"Recoverable Ram: {round(total_junk_ram, 2)} MB\n\nClick 'Auto-Clean' to free up resources.")

def handle_clean(gui):
    '''Automatically purges background tasks that aren't on the whitelist.'''
    global scanned_junk_pool
    if not scanned_junk_pool:
        messagebox.showinfo("Optimization Engine", "No unneeded processes found. Run a Scan pass first!")
        return

    killed_count = 0
    recovered_ram = 0.0
    log_to_console(gui, f"Starting clean operation on {len(scanned_junk_pool)} tasks...")
    
    for proc_name, pid, ram in scanned_junk_pool:
        try:
            p = psutil.Process(pid)
            if p.name() == proc_name:
                p.kill()
                killed_count += 1
                recovered_ram += ram
        except Exception:
            continue
            
    log_to_console(gui, f"Success! Terminated {killed_count} processes. Freed {round(recovered_ram, 2)} MB RAM.")
    gui.TProgressbar1['value'] = 0
    handle_scan(gui) # Auto-refresh UI fields to showcase empty junk vectors

def handle_kill_selected(gui):
    '''Kills only the process manually selected by the user in the Junk tree view table.'''
    selected_item = gui.Scrolledtree_Junk.selection()
    if not selected_item:
        messagebox.showwarning("Target Registry", "Please click a process in the Background/Junk list to target.")
        return
        
    item_data = gui.Scrolledtree_Junk.item(selected_item[0])
    proc_name = item_data['text']
    pid = item_data['values'][0]
    
    try:
        p = psutil.Process(int(pid))
        p.kill()
        log_to_console(gui, f"Manually targeted and terminated custom hook: PID {pid} ({proc_name})")
        handle_scan(gui)
    except Exception as ex:
        messagebox.showerror("Target Registry Error", f"Could not end process {pid}: {str(ex)}")

# ------------------ WHITELIST COMPONENT OPERATIONS ------------------

def add_whitelist_item(gui):
    '''Registers a new application to the user's permanent whitelist.'''
    new_app = gui.Entry_Whitelist.get().strip()
    if not new_app:
        return
    if new_app.lower() not in [item.lower() for item in system_whitelist]:
        system_whitelist.append(new_app)
        gui.Scrolledlist_WhiteLists.insert(tk.END, new_app)
        gui.Entry_Whitelist.delete(0, tk.END)
        log_to_console(gui, f"Whitelisted application entry point: '{new_app}'")
        save_config_state(gui, silent=True)
    else:
        messagebox.showinfo("Registry Info", "That process signature is already whitelisted.")

def remove_whitelist_item(gui):
    '''Removes an application from the user's whitelist.'''
    selected_idx = gui.Scrolledlist_WhiteLists.curselection()
    if not selected_idx:
        return
    
    item_name = gui.Scrolledlist_WhiteLists.get(selected_idx[0])
    if item_name.lower() in ["explorer.exe", "taskmgr.exe", "python.exe", "cleaner.py"]:
        messagebox.showerror("System Core Protection", "Protected core system modules cannot be unmapped.")
        return
        
    system_whitelist.remove(item_name)
    gui.Scrolledlist_WhiteLists.delete(selected_idx[0])
    log_to_console(gui, f"Removed program signature from whitelist mapping: '{item_name}'")
    save_config_state(gui, silent=True)

# ------------------ PERSISTENCE & APPEARANCE CONFIGS ------------------

def apply_theme_change(gui):
    '''Switches application color configurations dynamically on dropdown select actions.'''
    theme = gui.theme_dropdown.get()
    
    if theme == "Dark Classic":
        gui.style.configure('.', background="#2b2b2b", foreground="#ffffff")
        gui.style.configure('TNotebook', background="#2b2b2b")
        gui.style.configure('TNotebook.Tab', background="#3e3e3e", foreground="#ffffff")
        
        # Explicit treeview color overrides (fixes black text clipping)
        gui.style.configure('Treeview', background="#1e1e1e", fieldbackground="#1e1e1e", foreground="#ffffff")
        gui.style.configure('Treeview.Heading', background="#3e3e3e", foreground="#ffffff")
        
        # Direct Element Redraw Pass
        for tab in [gui.TNotebook_all_Dask, gui.TNotebook_all_white, gui.TNotebook_all_settings]:
            tab.configure(background="#2b2b2b")
        for widget in [gui.Label_header, gui.Label_Safe, gui.Label_Junk, gui.Label_inspector, gui.Label_console, gui.Label1, gui.Checkbutton_StartUp]:
            widget.configure(background="#2b2b2b", fg="#ffffff")
        gui.Scrolledtext_console.configure(bg="#1e1e1e", fg="#00ff00")
        gui.Scrolledtext_inspector.configure(bg="#1e1e1e", fg="#ffffff")
        log_to_console(gui, "Theme profile updated: Dark Classic configured.")

    elif theme == "Light Modern":
        gui.style.configure('.', background="#f5f6fa", foreground="#2c3e50")
        gui.style.configure('TNotebook', background="#f5f6fa")
        gui.style.configure('TNotebook.Tab', background="#dcdde1", foreground="#2c3e50")
        
        # Resets treeviews to clean dark-on-light theme behaviors
        gui.style.configure('Treeview', background="#ffffff", fieldbackground="#ffffff", foreground="#1b1b1b")
        gui.style.configure('Treeview.Heading', background="#dcdde1", foreground="#2c3e50")
        
        for tab in [gui.TNotebook_all_Dask, gui.TNotebook_all_white, gui.TNotebook_all_settings]:
            tab.configure(background="#f5f6fa")
        for widget in [gui.Label_header, gui.Label_Safe, gui.Label_Junk, gui.Label_inspector, gui.Label_console, gui.Label1, gui.Checkbutton_StartUp]:
            widget.configure(background="#f5f6fa", fg="#2c3e50")
        gui.Scrolledtext_console.configure(bg="#ffffff", fg="#1b1b1b")
        gui.Scrolledtext_inspector.configure(bg="#ffffff", fg="#1b1b1b")
        log_to_console(gui, "Theme profile updated: Light Modern configured.")

    elif theme == "Cyberpunk Amber":
        gui.style.configure('.', background="#120c00", foreground="#ffb300")
        gui.style.configure('TNotebook', background="#120c00")
        gui.style.configure('TNotebook.Tab', background="#261a00", foreground="#ffb300")
        
        # Cyberpunk data matrix color configurations
        gui.style.configure('Treeview', background="#1a1100", fieldbackground="#1a1100", foreground="#ffb300")
        gui.style.configure('Treeview.Heading', background="#261a00", foreground="#ffb300")
        
        for tab in [gui.TNotebook_all_Dask, gui.TNotebook_all_white, gui.TNotebook_all_settings]:
            tab.configure(background="#120c00")
        for widget in [gui.Label_header, gui.Label_Safe, gui.Label_Junk, gui.Label_inspector, gui.Label_console, gui.Label1, gui.Checkbutton_StartUp]:
            widget.configure(background="#120c00", fg="#ffb300")
        gui.Scrolledtext_console.configure(bg="#1a1100", fg="#ffcc00")
        gui.Scrolledtext_inspector.configure(bg="#1a1100", fg="#ffcc00")
        log_to_console(gui, "Theme profile updated: Cyberpunk Amber configured.")

def save_config_state(gui, silent=False):
    '''Writes active environment tracking metrics out to a local JSON configuration map.'''
    payload = {
        "whitelist": system_whitelist,
        "theme": gui.theme_dropdown.get(),
        "startup_sweep": gui.che73.get()
    }
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(payload, f, indent=4)
        if not silent:
            messagebox.showinfo("Config Manager", "Application configuration parameters saved successfully.")
    except Exception as ex:
        if not silent: messagebox.showerror("Config Error", f"Could not preserve config metrics: {str(ex)}")

def load_persistent_config(gui):
    '''Reads structural settings parameters back out of file allocations on boot launches.'''
    global system_whitelist
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
            system_whitelist = data.get("whitelist", system_whitelist)
            
            # Map values back into visual structures
            gui.theme_dropdown.set(data.get("theme", "Dark Classic"))
            gui.che73.set(data.get("startup_sweep", 0))
            apply_theme_change(gui)
        except Exception:
            pass
            
    # Sync visual representation items array to the whitelist storage layout
    gui.Scrolledlist_WhiteLists.delete(0, tk.END)
    for entry in system_whitelist:
        gui.Scrolledlist_WhiteLists.insert(tk.END, entry)

if __name__ == '__main__':
    main()