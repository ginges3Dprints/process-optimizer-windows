# Task Master Pro - Process Optimizer 🛠️

Task Master Pro is a lightweight, high-performance Windows optimization tool built in Python using Tkinter. It gives you advanced control over background processes, offering features that standard Windows Task Manager leaves out. 

It organizes your active tasks into distinct safety tiers, displays precise resource allocations, and allows you to liberate system memory with a single click.

---

## 🎯 Key Features

* **Smart Classification:** Automatically splits background activity into **Verified/Safe Programs** (browsers, launchers, game clients) and **Background Items/Potential Junk**.
* **1-Click Auto-Clean:** Instantly terminates unneeded background noise and displays exactly how many megabytes of RAM were successfully recovered.
* **Metadata Inspector:** Click any active item to view its exact directory path, unique Process ID (PID), and precise live memory usage.
* **Instant Web Audit:** Found something unrecognized? Click the **Google This Process** button to instantly audit the process online via your default browser.
* **Persistent Whitelisting:** Easily whitelist custom background tools or specific games so the Auto-Cleaner automatically skips them in future scans.
* **Self-Preservation System:** Hardcoded execution path checks ensure the app never accidentally flags or terminates itself while running.

---

## 🗺️ Project Roadmap & Future Features

We are actively working to make Task Master Pro the ultimate alternative to the Windows Task Manager. Here is what we have planned for upcoming releases:

### 🟢 Phase 1: Quality of Life & Customization (Next Release)
- [x] **Config File Persistence (`.json`):** Save your custom whitelist permanently to your hard drive so you don't have to re-type safe apps every time you reopen the tool.
- [x] **Dark Mode Toggle:** A sleek, modern dark user interface option for nighttime gaming sessions.
- [ ] **Real-time Live Refresh:** Automatically refresh the process lists every 5 seconds without needing to click the "Scan" button manually.

### 🟡 Phase 2: Automation & Advanced Optimization
- [ ] **Automated "Game Mode" Trigger:** Detect when a heavy game launcher (like Steam or Epic Games) opens, and automatically purge background junk in silence to maximize FPS.
- [ ] **CPU Usage Tracking:** Add a second line to the Inspector box showing active CPU percentage utilization alongside the RAM metrics.
- [ ] **Exportable System Logs:** Allow users to save their "Activity Console" text as a `.txt` file to diagnose persistent system slowdowns.

### 🔴 Phase 3: Performance Hardware Visualizers & Management
- [ ] **Mini Resource Graphs:** Add live visual canvas graphs tracking overall system RAM and CPU load directly on the dashboard.
- [ ] **Process Tree Tracking:** Group child processes (like multiple open browser tabs) under a single expandable parent name to keep the dashboard tidy.
- [ ] **Integrated App Control Panel:** A dedicated tab that reads Windows registry paths to list installed software and lets you launch native app uninstallers directly from the GUI.

### 🔵 Phase 4: Advanced Threat Detection & Quarantine Sandbox
- [ ] **Behavioral Diagnostics:** Introduce rules to automatically flag suspicious processes, such as hidden background tasks running without a user window or launching from temp folders.
- [ ] **Secure Quarantine Vault:** Instead of hard-killing unknown apps, add an option to safely freeze their threads and move their file payload into an isolated folder so they can't run unless you restore them.
- [ ] **Live Heuristic Risk Tags:** Display dynamic security threat levels inside the Process Inspector panel (e.g., `[SAFE]`, `[SUSPICIOUS]`, or `[CRITICAL THREAT]`) based on digital signatures and behavior.

---

## 💬 Community & Support

Need help setting up, found a bug, or want to request a feature? Join our community Discord server to connect with other users and get direct support:

👉 **[Join the Discord Server](https://discord.gg/PBWUWREdAK)**

## 🐛 Known Issues & Bug Tracker
If you encounter an unexpected behavior or crash while using Task Master Pro, please check the tracker below before opening a new issue.
1.[ ] when auto-clean unneeded processes TaskMaster Pro close (came back when i update the gui) easy fix for now just put TaskMasterPro.exe in custom white list.

### 📥 How to Report a Bug
If you find a bug that isn't listed here:
1. Navigate to the **Issues** tab at the top of this GitHub repository.
2. or join the Discord server above an make a ticket or carry on with the  with github
3. Click **New Issue** and describe what happened.
4. Provide your Windows Version, a quick screenshot of the layout error if applicable, and the exact steps to reproduce the crash.

---

## 🚀 How to Run or Build

If you do not wish to run the pre-provided executable file, you can easily build your own standalone version directly from the source code.

### Prerequisites (For Building)
1. Ensure you have **Python 3** installed on your system.
2. Place your script (`cleaner.py`) and your icon file (`spanner.ico`) in the same working directory.

### Quick Setup Scripts
We provide two shell scripts (`.sh`) to automate the installation and build phases using Git Bash, WSL, or a standard bash terminal:

1. **`install_dependencies.sh`**: Installs PyInstaller and required runtime libraries (`psutil`).
2. **`build_exe.sh`**: Compiles the source script into a standalone, single-file windows `.exe` with a hidden terminal console and the custom spanner thumbnail icon mapped automatically.
