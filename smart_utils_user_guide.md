# 🛠️ Smart-Utils - User Guide

**Smart-Utils** is a modern system administration panel, file management, OPKG packages, terminals and backup for **Keenetic** routers with the **Entware** environment.

---

## 🌟 Main features

### 1. 📁 Two-panel file manager (Total Commander)
- Classic two-panel interface with quick navigation through system paths (`/opt`, `/opt/etc`, `/tmp`, `/media`, `/`).
- **Hot keys:**
  - `Tab`: switch between left and right panels
  - `F3`: quick file preview
  - `F4`: built-in full-screen config editor with syntax highlighting and saving by `Ctrl + S`
  - `F5`: fast copying between panels
  - `F6`: move / rename
  - `F7`: creating a new folder
  - `F8`: deleting files and directories
  - `F9`: backup to `.tar.gz` or `.zip`
  - `F10`: change access rights (`chmod`) in the graphics window
- **Drag-and-Drop:** Drag and drop files from your computer directly into your browser window for instant downloading.

### 2. 💻 Web terminal
- **CLI terminal:** direct control of the KeeneticOS console (`ndmc` / `(config)>`) with fast system commands (`show version`, `show interface`, `show ip route`, `show log`).
- **SSH Terminal:** Fully featured Linux console PTY Entware (`/opt/bin/sh`, `/opt/bin/bash`) with full support for colors, hotkeys (`Ctrl+C`, `Ctrl+Z`, `nano`, `mc`, `top`, `htop`).

### 3. 📦 OPKG Package Manager
- **Repository directory:** view, add and delete custom `.conf` feeds.
- **Directory of popular repositories:** ready-made pre-installed repositories (Snakelair, AmneziaWG / AWG Manager, Zapret / NFQWS, Sing-Box Naive, Entware Main) with **live search** by names, descriptions and child packages.
- Install, remove, update packages in 1 click with a live console of OPKG process logs.

### 4. 📊 System and process analyzer
- Load graphs for CPU, cores, memory, Swap, disk drives and network traffic.
- Interactive table of processes (`top`/`htop`) with sorting by columns (% CPU, % MEM, PID, RSS), searching and sending signals `SIGTERM` / `SIGKILL`.

### 5. 💾 Backup and Restore
- Export and restore the complete list of installed OPKG packages.
- Creation of compressed `.tar.gz` archives of `/opt/etc/` configuration files and their rollback in one click.

### 6. ⚡ Logging to RAM (tmpfs)
- By default, the Smart-Utils service writes logs to RAM (`/tmp/smart-utils.log`), which completely eliminates wear and tear on the router's flash memory.

---

## 🚀 Installation

```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-utils
```

After installation, open the web interface:
`http://192.168.1.1:8090` (or your router's IP address)

---

## 🗑️ Complete removal of Smart-Utils

### Automatically (in one command):
```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-utils
```

### Manually via SSH:
```bash
/opt/etc/init.d/S99smart-utils stop
killall -9 smart-utils 2>/dev/null
opkg remove smart-utils --force-remove --force-depends
rm -f /opt/etc/init.d/S99smart-utils /tmp/smart-utils.log /opt/var/log/smart-utils.log
rm -rf /opt/etc/smart-utils
```
