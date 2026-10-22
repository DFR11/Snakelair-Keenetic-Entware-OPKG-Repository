# Snakelair, Keenetic, Entware, OPKG Repository

This repository is a fork and English-language localization of the original Snakelair Keenetic ecosystem project.

> Source repository: https://github.com/snakelair/Keenetic
> Special thanks to the original author and contributors for creating and maintaining the original Keenetic, Entware, and OPKG ecosystem.

Snakelair Keenetic Entware OPKG Repository is an OPKG repository for Keenetic routers with Entware installed.

## 📦 Available packages in the repository

1. 🛠️ smart-utils (v1.0.43)

A versatile web-based system for managing and controlling a Keenetic router.

- Two-panel file manager inspired by Total Commander
- Web terminal for both KeeneticOS CLI and Linux/Entware shell
- OPKG package manager with live repository search and installation tools
- System and CPU monitor
- Backup and restore tools
- RAM-based logging
- Web interface: http://192.168.1.1:8001
- Smart-Utils User Guide: smart_utils_user_guide.md

2. ⚡ smart-route (v1.0.229)

A system-level service for dynamic multi-interface routing, seamless failover interception, and hardware-based kernel offloading (IPSet/NDM).

- Automatic selection of the fastest VPN channel during outages and restrictions
- Linux kernel hardware offload
- Exclusion lists for direct WAN access
- Integrated Sing-box, Xray, Shadowsocks, and WireGuard support
- Web interface: http://192.168.1.1:8002
- Smart-Route User Guide: smart_route_user_guide.md

3. 📷 smart-photo (v1.0.165)

A personal photo server for Keenetic routers with USB storage.

- Infinite scrolling photo feed
- Thumbnail generation and caching
- Full-screen viewer with zoom and slideshow
- EXIF metadata support
- Albums and folders
- Web interface: http://192.168.1.1:8003
- Smart-Photo User Guide: smart_photo_USER_GUIDE.md

4. 🛡️ smart-vpn (v1.0.144)

A unified web center for managing VPN connections and anti-censorship modules.

- Native KeeneticOS tunnels: WireGuard, SSTP, OpenVPN, IPsec
- AmneziaWG support
- QuakeLive-VPN support
- Sing-box subsystem
- Remote VPS deployment via SSH
- Web interface: http://192.168.1.1:8004
- Smart-VPN User Guide: USER_GUIDE.md

5. 🎮 ql-vpn (v1.0.144)

A high-speed stealth tunnel engine based on the id Tech 3 NetChan (Quake Live) protocol.

- Traffic masking for tunnel protocols
- Supported on Linux VPS and Windows clients
- Low-latency UDP tunneling
- Built-in web control center
- Automatic self-update support
- Web interface: https://<server-ip>:8005
- QL-VPN User Guide: ql_vpn_user_guide.md

## 🚀 Quick installation

1. Automatic installation for the full ecosystem

Connect to the router or VPS via SSH and run:

```bash
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh
```

2. Install a specific package

```bash
# Install Smart-Utils
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s smart-utils

# Install Smart-Route
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s smart-route

# Install Smart-Photo
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s smart-photo

# Install Smart-VPN
curl -sSL https://raw.githubusercontent.com/snakelair/Keenetic/main/install.sh | sh -s smart-vpn
```

## 🔎 Repository purpose

This fork keeps the original Snakelair/Keenetic distribution accessible via an OPKG repository format while adding documentation and localization improvements for broader accessibility.

## 🙏 Acknowledgements

Thanks to the original author and maintainers of the Snakelair Keenetic project for their excellent work and for making this ecosystem available to the community.
