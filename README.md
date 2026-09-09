# ⚡ Snakelair Keenetic Entware OPKG Repository

**Snakelair Keenetic Entware OPKG Repository** - a repository of **OPKG** packages for **Keenetic** routers with the **Entware** environment installed.

---

## 📦 Available packages in the repository

### 1. 🛠️ `smart-utils` (v1.0.29)
**Universal web-based system administration and router management Keenetic:**
- **Two-panel file manager:** classic Total Commander-style interface, F3–F10 hotkeys, full-screen config editor with syntax highlighting, archiver (tar.gz/zip), changing access rights (chmod) and Drag-and-Drop downloading files directly to the browser.
- **Two web terminals:**
  - **CLI terminal:** direct control of the KeeneticOS command line (`ndmc` / `(config)>`).
  - **SSH Terminal:** access to Linux / Entware Shell session (`/opt/bin/sh`, `/opt/bin/bash`) with full support for colors and hotkeys.
- **OPKG package manager:** directory of repositories/feeds, directory of popular repositories with live search and description of child packages, installation, removal, update of packages and output of logs in real time.
- **System and CPU analyzer:** real-time graphs of CPU load, cores, memory, Swap, disks and network traffic, as well as an interactive process table (`top`/`htop`) with sorting and signal management (SIGTERM/SIGKILL).
- **Backup and restore:** export/import of OPKG package list, creation and rollback of configuration archives `/opt/etc/`.
- **Logging:** secure logging into RAM (RAM `/tmp/smart-utils.log`) without wearing out the flash drive.
- **Web interface:** `http://192.168.1.1:8090` (or IP of your router)
- [📘 **Smart-Utils User Guide (smart_utils_user_guide.md)**](smart_utils_user_guide.md)

---

### 2. ⚡ `smart-route` (v1.0.66)
**System service for dynamic multi-interface routing, seamless interception of failed connections (Failover Relay) and hardware kernel offloading (IPSet / NDM):**
- Automatic selection of the fastest VPN channel in case of failures and blocking (Race/Sequential).
- Hardware offload of the Linux kernel (0% load on the router processor).
- Support of exclusion lists (.ru, .рф, banks, government services) for direct WAN access.
- Built-in cores Sing-box, Xray, Shadowsocks, WireGuard.
- **Web Interface:** `http://192.168.1.1:8088`
- [📘 **Complete Smart-Route User Guide (smart_route_user_guide.md)**](smart_route_user_guide.md)

---

### 3. 📷 `smart-photo` (v1.0.39)
**Personal home photo server in Google Photos style directly on the Keenetic router for connected USB drives:**
- An endless photo chronicle feed (Infinite Scroll) with fast display.
- Scan and view photos and videos from USB-connected storage devices (flash drives, HDD, SSD).
- Instant generation and caching of thumbnails on the fly.
- Full-screen viewer (Lightbox) with zoom, slideshow and viewing EXIF ​​metadata (camera, shutter speed, aperture, GPS).
- Automatic grouping by dates, folders and albums.
- **Web Interface:** `http://192.168.1.1:8089`
- [📷 **Smart-Photo User Guide (smart_photo_USER_GUIDE.md)**](smart_photo_USER_GUIDE.md)

---

### 4. 🛡️ `smart-vpn` (v1.0.27)
**Unified web-based management center for all types of VPN connections and anti-censorship engines for Keenetic routers:**
- **Native KeeneticOS tunnels:** WireGuard, SSTP, OpenVPN, IPsec with asynchronous polling and status caching.
- **AmneziaWG (AWG 2.0 / 3.0) support:** Full obfuscation control (Jc, Jmin/Jmax, S1-S4, H1-H4), Anti-TSPU presets and Curve25519 public key calculation.
- **QuakeLive-VPN stealth protocol:** Gaming VPN based on id Tech 3 NetChan with player scoreboard, probing protection and token generation.
- **Sing-Box subsystem:** visual designer with 7 tabs (VLESS Reality, ShadowTLS v3, Trojan), CPU Watchdog and configuration validator.
- **Deployment on VPS via SSH:** automatic configuration of a remote server in one click with selection of a web port.
- **Web interface:** `http://192.168.1.1:8091` (or IP of your router)
- [🛡️ **Smart-VPN User Guide (USER_GUIDE.md)**](https://github.com/snakelair/SmartVpn/blob/main/USER_GUIDE.md)

---

### 5. 🎮 `ql-vpn` (v1.0.65)
**New generation high-speed stealth tunnel based on the id Tech 3 NetChan (Quake Live) protocol:**
- **100% masking of network traffic:** packets are indistinguishable from real Quake Live network multiplayer, resistant to traffic analysis and DPI signature blocking.
- **Platform support:** Linux VPS (server/gateway) and Windows (client with system tray and GUI).
- **Ultra-low ping:** direct UDP tunneling, AES-128-GCM and ChaCha20-Poly1305 hardware encryption.
- **Standalone web control center:** web interface (:8092) for monitoring players, generating `qlvpn://` tokens, measuring latency and managing routing.
- **Built-in self-updating system:** Automatic update of the binary and service in one click directly from the web interface.
- **Web Interface:** `https://<ip-сервера>:8092`
- [🎮 **QuakeLive-VPN User Guide (ql_vpn_user_guide.md)**](ql_vpn_user_guide.md) - installation, architecture and detailed map of files on VPS

---

## 🚀 Quick installation

### 1. Automatic installation (in one command):

Connect to the router (or VPS) via SSH and run:

```bash
# Установить Smart-Utils (Веб-панель, Терминалы, Файловый менеджер, OPKG):
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-utils

# Установить Smart-Route (Маршрутизация и обход блокировок):
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-route

# Установить Smart-Photo (Персональная фотогалерея на USB):
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-photo

# Установить Smart-VPN (WireGuard, AWG, Sing-box, QuakeLive-VPN на роутер):
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-vpn

# Установить QuakeLive-VPN Server (на Linux VPS / удаленный сервер):
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install-qlvpn.sh | bash
# или через универсальный установщик:
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s ql-vpn
```

---

### 2. Manually connecting the OPKG repository:

Create a repository configuration file in `/opt/etc/opkg/keenetic.conf`:

```bash
ARCH=$(uname -m | sed 's/mips/mipsel-3.4/' | sed 's/aarch64/aarch64-3.10/' | sed 's/armv7l/armv7-3.2/')
echo "src/gz keenetic-custom https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/entware/${ARCH}" > /opt/etc/opkg/keenetic.conf

# Обновите список пакетов и установите нужные сервисы:
opkg update
opkg install smart-utils
opkg install smart-route
opkg install smart-photo
opkg install smart-vpn
```

---

## 🔄 Package update

```bash
opkg update && opkg upgrade smart-utils smart-route smart-photo smart-vpn
```

---

## 🗑️ Complete removal of packages and repository

### 1. Automatic removal in one command:

```bash
# Интерактивное меню удаления:
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh

# Быстрое удаление конкретного пакета (с очисткой службы, правил и конфигов):
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-utils
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-route
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-photo
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-vpn
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s ql-vpn

# Полное удаление ВСЕХ пакетов Snakelair и отключение репозитория OPKG:
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s all
```

---

### 2. Manual removal via SSH console:

<details>
<summary><b>🛠️ Пошаговые команды ручного удаления для каждого пакета</b></summary>

#### Removing `smart-utils`:
```bash
/opt/etc/init.d/S99smart-utils stop
killall -9 smart-utils 2>/dev/null
opkg remove smart-utils --force-remove --force-depends
rm -f /opt/etc/init.d/S99smart-utils /tmp/smart-utils.log /opt/var/log/smart-utils.log
rm -rf /opt/etc/smart-utils
```

#### Removing `smart-route`:
```bash
/opt/etc/init.d/S99smart-route stop
killall -9 smart-route 2>/dev/null
opkg remove smart-route --force-remove --force-depends
rm -f /opt/etc/init.d/S99smart-route /tmp/smart-route.log /opt/var/log/smart-route.log
rm -rf /opt/etc/smart-route
# Сброс правил iptables и ipset:
iptables -t nat -D PREROUTING -p tcp -m multiport --dports 80,443 -j REDIRECT --to-ports 10880 2>/dev/null
iptables -t nat -D PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 10853 2>/dev/null
for s in $(ipset list -n 2>/dev/null | grep -E '^sr_'); do ipset flush "$s"; ipset destroy "$s"; done
```

#### Removing `smart-photo`:
```bash
/opt/etc/init.d/S99smart-photo stop
killall -9 smart-photo 2>/dev/null
opkg remove smart-photo --force-remove --force-depends
rm -f /opt/etc/init.d/S99smart-photo /tmp/smart-photo.log /opt/var/log/smart-photo.log
rm -rf /opt/etc/smart-photo /opt/var/cache/smart-photo
```

#### Removing `smart-vpn`:
```bash
/opt/etc/init.d/S99smart-vpn stop
killall -9 smart-vpn sing-box awg 2>/dev/null
opkg remove smart-vpn --force-remove --force-depends
rm -f /opt/etc/init.d/S99smart-vpn /tmp/smart-vpn.log /opt/var/log/smart-vpn.log
rm -rf /opt/etc/smart-vpn
```

#### Removing `ql-vpn` (QuakeLive-VPN Server on Linux VPS):
```bash
systemctl stop ql-vpn && systemctl disable ql-vpn
killall -9 ql-vpn 2>/dev/null
rm -f /usr/local/bin/ql-vpn /etc/systemd/system/ql-vpn.service /etc/sysctl.d/99-qlvpn.conf
rm -rf /etc/ql-vpn
systemctl daemon-reload
```

#### Completely disabling the OPKG repository:
```bash
rm -f /opt/etc/opkg/keenetic.conf /opt/var/opkg-lists/keenetic-custom
opkg update
```

</details>

---

## 🌐 Correspondence between Keenetic models and architectures

|Architecture|Keenetic router models|
| :--- | :--- |
| **`mipsel-3.4`** | Viva, Extra, Speedster, Giga (KN-1010/1011), Omni, Skipper, Air, Buddy |
| **`armv7-3.2`** | Hero (KN-1011/KN-1012), Titan (KN-1810), Giant (KN-2610), Ultra (KN-1810) |
| **`aarch64-3.10`** | Peak (KN-2710), Ultra (KN-1811), Titan (KN-1812), Hero 4G+ (KN-2311) |
| **`x86_64`** |x86 Entware / Virtual machines|
| **`mips-3.4`** | Keenetic MIPS Big-Endian |


---

## 💬 Community and feedback

- 📢 **Telegram channel and updates:** [t.me/KeeneticSmartUtils](https://t.me/KeeneticSmartUtils)
- 💬 **Discussion topic on the Keenetic forum:** [Applications Smart-Utils, Smart-Route, Smart-Photo](https://forum.keenetic.ru/topic/30698-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-smart-utils-smart-route-smart-photo-snakelair-keenetic-entware-opkg-repository/)
- 🐞 **Bug report and suggestion tracker:** [github.com/snakelair/Keenetic/issues](https://github.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/issues)
- 💻 **Smart-Utils source code:** [github.com/snakelair/SmartUtils](https://github.com/snakelair/SmartUtils)


