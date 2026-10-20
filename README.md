 Snakelair, Keenetic, Entware, OPKG Repository

Snakelair Keenetic Entware OPKG Repository – an OPKG repository for Keenetic routers that have Entware installed.
📦 Available Packages in the Repository
1. 🛠️ smart-utils (v1.0.43)

A versatile web-based system for managing and controlling a Keenetic router.

    A two-pane file manager: a classic interface reminiscent of Total Commander, with hotkeys F3-F10, a full-screen configuration editor with syntax highlighting, an archiver (tar.gz/zip), and the ability to change file permissions (chmod) and drag-and-drop files directly into the browser.
    Two web terminals:
        CLI Terminal: Direct command-line control for KeeneticOS ( ndmc / (config)> ).
        SSH Terminal: Access to Linux/Entware shell sessions ( /opt/bin/sh , /opt/bin/bash ) with full color support and keyboard shortcuts.
    OPKG package manager: repository/feed catalog, a catalog of popular repositories with live search and descriptions of dependent packages, package installation, removal, and updates, with real-time log output.
    System and CPU Analyzer: real-time graphs of CPU, cores, memory, swap, disk, and network traffic, as well as an interactive process table ( top / htop ) with sorting and signal control (SIGTERM/SIGKILL).
    Backup and Restore: Export/import of the OPKG package list, creation and reversion of configuration archives.
    Logging: Safe logging to RAM (RAM /tmp/smart-utils.log ) without wearing out flash storage.
    Web interface: http://192.168.1.1:8001 (or your router's IP address)
    📘 Smart-Utils User Guide (smart_utils_user_guide.md)

2. ⚡ smart-route (v1.0.229)

System-level service for dynamic multi-interface routing, seamless failover connection interception, and hardware-based kernel offloading (IPSet/NDM):

    Automatic selection of the fastest VPN channel during outages and restrictions (Race/Sequential).
    Hardware offload kernel for Linux (0% CPU utilization on router).
    Support for exclusion lists (.ru, .рф, banks, government services) for direct WAN access.
    Built-in cores: Sing-box, Xray, Shadowsocks, WireGuard.
    Web interface: http://192.168.1.1:8002
    📘 Smart-Route User Guide (smart_route_user_guide.md)

3. 📷 smart-photo (v1.0.165)

A personal home photo server, similar to Google Photos, directly on your Keenetic router, for USB storage devices:

    Infinite scroll with fast loading.
    Scanning and viewing photos and videos from USB drives (flash drives, HDDs, SSDs).
    Instant generation and caching of thumbnails while browsing.
    Full-screen viewer with zoom, slideshow, and EXIF metadata viewing (camera, shutter speed, aperture, GPS).
    Automatic grouping by date, folder, and album.
    Web interface: http://192.168.1.1:8003
    📷 Smart-Photo User Guide (smart_photo_USER_GUIDE.md)

4. 🛡️ smart-vpn (v1.0.144)

A unified web center for managing all types of VPN connections and anti-censorship modules for Keenetic routers.

    Native KeeneticOS tunnels: WireGuard, SSTP, OpenVPN, IPsec with asynchronous polling and status caching.
    Support for AmneziaWG (AWG 2.0 / 3.0): full control over obfuscation (Jc, Jmin/Jmax, S1-S4, H1-H4), presets for "Anti-TSP," and calculation of Curve25519 public keys.
    QuakeLive-VPN Stealth Protocol: An ID Tech 3-based VPN with an in-game scoreboard, anti-cheat features, and token generation.
    Sing-Box Subsystem: A visual constructor with 7 tabs (VLESS Reality, ShadowTLS v3, Trojan), CPU Watchdog, and a configuration validator.
    Deployment on VPS via SSH: Automatically configure your remote server with a single click, choosing your preferred web portal.
    Web interface: http://192.168.1.1:8004 (or your router's IP address)
    🛡️ Smart-VPN User Guide (USER_GUIDE.md)

5. 🎮 ql-vpn (v1.0.144)

High-speed stealth tunnel of the next generation, based on the id Tech 3 NetChan (Quake Live) protocol.

    100% network traffic masking: packets are indistinguishable from real Quake Live network traffic, resistant to TSPU analysis and DPI signature blocking.
    Supported Platforms: Linux VPS (server/gateway) and Windows (client with system tray and GUI).
    Ultra-low latency: direct UDP tunneling, hardware-accelerated AES-128-GCM and ChaCha20-Poly1305 encryption.
    Autonomous web-based control center: web interface (:8005) for monitoring players, token generation ( qlvpn:// ), latency measurement, and routing management.
    Built-in self-updating system: automatic updates for the binary and service with a single click, directly from the web interface.
    Web interface: https://<ip-сервера>:8005
    🎮 QuakeLive-VPN User Guide (ql_vpn_user_guide.md) – Installation, architecture, and detailed file map on a VPS

6. 📹 smart-nvr (version 1.0.0)

A high-performance video surveillance gateway and video conferencing system for Hiseeu/Xiongmai recorders and iCSee cameras.

    Live video and archive streaming: secure access to cameras and NVR from an external network via the internet (KeenDNS, VPN, WAN) without direct port forwarding.
    0% transcoding: The router's processor is not used for decoding; H.264/H.265 playback is handled by the client.
    Network discovery for security cameras: scans your home network in 1.5 seconds, identifying models, serial numbers, and adding devices with a single click.
    Web interface: http://172.16.1.1:8006 (or your router's IP address)

🚀 Quick Installation
1. Automatic installation (for a single team):

Connect to the router (or VPS) via SSH and execute:

# Интерактивное меню установки всех компонентов экосистемы:
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh

# Или прямая установка конкретного пакета:
# Установить Smart-Utils (Веб-панель, Терминалы, Файловый менеджер, OPKG):
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s smart-utils

# Установить Smart-Route (Маршрутизация и обход блокировок):
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s smart-route

# Установить Smart-Photo (Персональная фотогалерея на USB):
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s smart-photo

# Установить Smart-VPN (WireGuard, AWG, Sing-box, QuakeLive-VPN на роутер):
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s smart-vpn

# Установить SmartNVR (Шлюз видеонаблюдения Hiseeu/iCSee и веб-центр NVR):
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s smart-nvr

# Установить QuakeLive-VPN Server (на Linux VPS / удаленный сервер):
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install-qlvpn.sh | bash
# или через универсальный установщик:
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s ql-vpn

2. Manual connection to the OPKG repository:

Create a repository configuration file at /opt/etc/opkg/snakelair.conf :

ARCH=$(opkg print-architecture 2>/dev/null | grep -v 'all' | sort -k3 -n | tail -1 | awk '{print $2}')
[ -z "$ARCH" ] && ARCH=$(uname -m | sed 's/aarch64/aarch64-3.10/' | sed 's/armv7l/armv7-3.2/' | sed 's/mips$/mips-3.4/' | sed 's/mipsel/mipsel-3.4/')
echo "src/gz snakelair https://raw.githubusercontent.com/snakelair/Keenetic/main/entware/${ARCH}" > /opt/etc/opkg/snakelair.conf

# Обновите список пакетов и установите нужные сервисы:
opkg update
opkg install smart-utils
opkg install smart-route
opkg install smart-photo
opkg install smart-vpn
opkg install smart-nvr

🔄 Package Updates

opkg update && opkg upgrade smart-utils smart-route smart-photo smart-vpn smart-nvr

🗑️ Complete deletion of packages and repositories
1. Automatic deletion in a single command:

# Интерактивное меню удаления:
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/uninstall.sh | sh

# Быстрое удаление конкретного пакета (с очисткой службы, правил и конфигов):
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/uninstall.sh | sh -s smart-utils
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/uninstall.sh | sh -s smart-route
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/uninstall.sh | sh -s smart-photo
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/uninstall.sh | sh -s smart-vpn
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/uninstall.sh | sh -s ql-vpn

# Полное удаление ВСЕХ пакетов Snakelair и отключение репозитория OPKG:
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/uninstall.sh | sh -s all

2. Manual removal via SSH console:
🛠️ Step-by-step manual removal instructions for each package

🌐 Keenetic Model Compatibility and Architecture Alignment
Architecture 	Keenetic routers
mipsel-3.4 	Viva, Extra, Speedster, Giga (KN-1010/1011), Omni, Skipper, Air, Buddy
armv7-3.2 	Hero (KN-1011/KN-1012), Titan (KN-1810), Giant (KN-2610), Ultra (KN-1810)
aarch64-3.10 	Peak (KN-2710), Ultra (KN-1811), Titan (KN-1812), Hero 4G+ (KN-2311)
x86_64 	x86 Entware / Virtual Machines
mips-3.4 	Giga SE (KN-2410), Keenetic MIPS Big-Endian (QCA9563/QCA9558)
📱 Android and Android TV Apps

For quick installation, scan the QR code with your smartphone's camera or click the direct APK link:
App 	Description 	Download APK 	QR code for the camera
🎮 QuakeLive-VPN 	A stealth-focused Android game with ultra-low latency and DPI protection. 	QuakeLiveVPN.apk 	QR QuakeLive-VPN
📸 SmartPhotoSync 	Automatic photo and video synchronization from smartphone to USB drive on a router. 	SmartPhotoAndroid.apk 	QR SmartPhotoSync
📺 SmartPhotoTV 	Photo gallery and media player for Android TV and game consoles, using a remote control. 	SmartPhotoTV.apk 	QR SmartPhotoTV
💬 Community and Feedback

    📢 Telegram community and updates: t.me/SmartKeenetic
    💬 Forum topic on the Keenetic forum: Smart-Utils, Smart-Route, and Smart-Photo applications.
    🐞 Bug reporting and feature request tracker: github.com/snakelair/Keenetic/issues
    💻 Source code for Smart-Utils: github.com/snakelair/SmartUtils
