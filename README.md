# ⚡ Snakelair Keenetic Entware OPKG Repository

This repository is an English-language fork/localization of the original Snakelair Keenetic ecosystem project.

> Original project: https://github.com/snakelair/Keenetic  
> Special thanks to the original author and contributors for creating and maintaining the original Keenetic / Entware ecosystem.

**Snakelair Keenetic Entware OPKG Repository** — an OPKG package repository for **Keenetic** routers with the **Entware** environment installed.

---

## 📦 Available packages in the repository

### 1. 🛠️ `smart-utils` (v1.0.43)
**A universal web-based system administration and router control panel for Keenetic:**
- **Two-panel file manager:** classic Total Commander-style interface, hotkeys F3–F10, full-screen editor with syntax highlighting, archive creation (`tar.gz` / `zip`), and file operations.
- **Two web terminals:**
  - **CLI terminal:** direct control of the KeeneticOS command line (`ndmc` / `(config)>`).
  - **SSH terminal:** access to the Linux / Entware shell (`/opt/bin/sh`, `/opt/bin/bash`) with full color support and hotkeys.
- **OPKG package manager:** repository/feed catalog, popular repositories list with live search and package metadata, installation, removal, and updates.
- **System and CPU analyzer:** real-time graphs for CPU, core usage, memory, swap, disk, and network traffic, plus an interactive process table (`top` / `htop`).
- **Backup and restore:** export/import the OPKG package list and create/restore configuration archives.
- **Logging:** safe logging to RAM (`/tmp/smart-utils.log`) without wearing out flash memory.
- **Web interface:** `http://192.168.1.1:8001` (or your router IP)
- [📘 **Smart-Utils User Guide (smart_utils_user_guide.md)**](smart_utils_user_guide.md)

---

### 2. ⚡ `smart-route` (v1.0.229)
**A system service for dynamic multi-interface routing and seamless failover interception:**
- Automatic selection of the fastest VPN channel during outages or restrictions (Race / Sequential).
- Linux kernel hardware offload (0% CPU load on the router).
- Support for exclusion lists (.ru, .рф, banks, government services) for direct WAN access.
- Built-in Sing-box, Xray, Shadowsocks, and WireGuard cores.
- **Web interface:** `http://192.168.1.1:8002`
- [📘 **Smart-Route User Guide (smart_route_user_guide.md)**](smart_route_user_guide.md)

---

### 3. 📷 `smart-photo` (v1.0.165)
**Personal home photo server in the style of Google Photos, running directly on Keenetic routers with USB storage attached:**
- Infinite photo timeline with fast loading.
- Scanning and viewing photos and videos from USB devices (flash drives, HDDs, SSDs).
- Instant thumbnail generation and on-the-fly caching.
- Full-screen viewer (lightbox) with zoom, slideshow, and EXIF metadata viewing (camera, shutter speed, aperture, GPS).
- Automatic grouping by date, folder, and album.
- **Web interface:** `http://192.168.1.1:8003`
- [📷 **Smart-Photo User Guide (smart_photo_USER_GUIDE.md)**](smart_photo_USER_GUIDE.md)

---

### 4. 🛡️ `smart-vpn` (v1.0.144)
**A unified web center for managing all VPN connection types and anti-censorship cores for Keenetic routers:**
- **Native KeeneticOS tunnels:** WireGuard, SSTP, OpenVPN, IPsec with asynchronous polling and status caching.
- **AmneziaWG (AWG 2.0 / 3.0) support:** full obfuscation control (`Jc`, `Jmin/Jmax`, `S1-S4`, `H1-H4`), anti-TSPU presets, and Curve25519 public-key calculations.
- **QuakeLive-VPN Stealth protocol support:** dedicated anti-cheat and token generation for game traffic.
- **Sing-box subsystem:** visual constructor with 7 tabs (VLESS Reality, ShadowTLS v3, Trojan), CPU watchdog, and config validator.
- **Deployment on VPS via SSH:** one-click setup for remote servers with a preferred portal.
- **Web interface:** `http://192.168.1.1:8004` (or your router IP)
- [🛡️ **Smart-VPN User Guide (USER_GUIDE.md)**](USER_GUIDE.md)

---

### 5. 🎮 `ql-vpn` (v1.0.144)
**A next-generation high-speed stealth tunnel based on the id Tech 3 NetChan (Quake Live) protocol.**
- 100% network traffic masking: packets are indistinguishable from real Quake Live traffic and resistant to TSPU/DPI analysis.
- Supported platforms: Linux VPS (server/gateway) and Windows client (with system tray and GUI).
- Ultra-low latency: direct UDP tunneling with hardware-accelerated AES-128-GCM and ChaCha20-Poly1305 encryption.
- Autonomous web control center: monitoring players, token generation (`qlvpn://`), latency measurement, and routing management.
- Built-in self-update system: direct in-panel binary and service updates.
- **Web interface:** `https://<server-ip>:8005`
- [🎮 **QuakeLive-VPN User Guide (ql_vpn_user_guide.md)**](ql_vpn_user_guide.md)

---

### 6. 📹 `smart-nvr` (v1.0.0)
**High-performance video surveillance gateway and video conferencing system for Hiseeu / Xiongmai recorders and iCSee cameras.**
- Live video and archive streaming over the internet via KeenDNS, VPN, or WAN without direct port forwarding.
- 0% transcoding: the router CPU is not used for decoding; H.264/H.265 playback is handled by the client.
- Automatic device discovery for IP cameras and NVRs in ~1.5 seconds.
- **Web interface:** `http://172.16.1.1:8006` (or your router IP)

---

## 🚀 Quick installation

### 1. Automatic installation for the full ecosystem

Connect to the router (or VPS) via SSH and run:

```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh
```

### 2. Install a specific package

```bash
# Install Smart-Utils
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-utils

# Install Smart-Route
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-route

# Install Smart-Photo
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-photo

# Install Smart-VPN
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-vpn

# Install SmartNVR
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-nvr

# Install QuakeLive-VPN server on Linux VPS / remote server
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install-qlvpn.sh | bash
# or via the universal installer:
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s ql-vpn
```

### 3. Manual connection to the OPKG repository

Create a repository config file at `/opt/etc/opkg/snakelair.conf`:

```bash
ARCH=$(opkg print-architecture 2>/dev/null | grep -v 'all' | sort -k3 -n | tail -1 | awk '{print $2}')
[ -z "$ARCH" ] && ARCH=$(uname -m | sed 's/aarch64/aarch64-3.10/' | sed 's/armv7l/armv7-3.2/' | sed 's/mips$/mips-3.4/' | sed 's/mipsel/mipsel-3.4/')
echo "src/gz snakelair https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/entware/${ARCH}" > /opt/etc/opkg/snakelair.conf
```

Then update the package index and install the required services:

```bash
opkg update
opkg install smart-utils
opkg install smart-route
opkg install smart-photo
opkg install smart-vpn
opkg install smart-nvr
```

### 🔄 Package updates

```bash
opkg update && opkg upgrade smart-utils smart-route smart-photo smart-vpn smart-nvr
```

### 🗑️ Complete removal of packages and repository

#### 1. Automatic removal in a single command

```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh
```

#### 2. Remove a specific package quickly (with service/config cleanup)

```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-utils
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-route
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-photo
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-vpn
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s ql-vpn
```

#### 3. Fully remove all Snakelair packages and disable the OPKG repository

```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s all
```

#### 4. Manual removal via SSH console

```bash
# Stop services
/opt/etc/init.d/S99smart-utils stop
/opt/etc/init.d/S99smart-route stop
/opt/etc/init.d/S99smart-photo stop
/opt/etc/init.d/S99smart-vpn stop

# Remove packages
opkg remove smart-utils --force-remove --force-depends
opkg remove smart-route --force-remove --force-depends
opkg remove smart-photo --force-remove --force-depends
opkg remove smart-vpn --force-remove --force-depends
```

---

## 🌐 Keenetic model compatibility and architecture alignment

| Architecture | Keenetic routers |
| :--- | :--- |
| `mipsel-3.4` | Viva, Extra, Speedster, Giga (KN-1010/1011), Omni, Skipper, Air, Buddy |
| `armv7-3.2` | Hero (KN-1011/KN-1012), Titan (KN-1810), Giant (KN-2610), Ultra (KN-1810) |
| `aarch64-3.10` | Peak (KN-2710), Ultra (KN-1811), Titan (KN-1812), Hero 4G+ (KN-2311) |
| `x86_64` | x86 Entware / Virtual Machines |
| `mips-3.4` | Giga SE (KN-2410), Keenetic MIPS Big-Endian (QCA9563 / QCA9558) |

---

## 📱 Android and Android TV apps

For quick installation, scan the QR code with your smartphone camera or click the direct APK link:

| App | Description | Download APK | QR code |
| :--- | :--- | :--- | :--- |
| 🎮 QuakeLive-VPN | A stealth-focused Android game with ultra-low latency and DPI protection. | `QuakeLiveVPN.apk` | QR QuakeLive-VPN |
| 📸 SmartPhotoSync | Automatic photo and video synchronization from smartphone to USB drive on a router. | `SmartPhotoAndroid.apk` | QR SmartPhotoSync |
| 📺 SmartPhotoTV | Photo gallery and media player for Android TV and game consoles, using a remote control. | `SmartPhotoTV.apk` | QR SmartPhotoTV |

---

## 💬 Community and feedback

- 📢 Telegram community and updates: `t.me/SmartKeenetic`
- 💬 Forum topic on the Keenetic forum: Smart-Utils, Smart-Route, and Smart-Photo applications.
- 🐞 Bug reporting and feature request tracker: `https://github.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/issues`
- 💻 Source code for Smart-Utils: `https://github.com/snakelair/SmartUtils`

---

## 🙏 Acknowledgements

This fork is based on the original Snakelair Keenetic project and keeps the original functionality while localizing the project documentation to English and adapting repository URLs to this fork.

We sincerely thank the original author and contributors for their excellent work in creating and maintaining this ecosystem.
