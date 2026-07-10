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

## 💬 Community & Support

Need help setting up, found a bug, or want to request a feature? Join our community Discord server to connect with other users and get direct support:

👉 **[Join the Discord Server](https://discord.gg/9AChaMyFBe)**

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