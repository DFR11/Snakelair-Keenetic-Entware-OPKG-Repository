# 📷 Smart-Photo for Keenetic Entware

[![Build & Publish OPKG Packages](https://github.com/snakelair/SmartPhoto/actions/workflows/deploy-packages.yml/badge.svg)](https://github.com/snakelair/SmartPhoto/actions)
[![Release](https://img.shields.io/badge/release-v1.0.39-blue.svg)](https://github.com/snakelair/SmartPhoto/releases)
[![Keenetic Entware](https://img.shields.io/badge/Keenetic-Entware-38d39f.svg)](https://github.com/snakelair/Keenetic)

**Smart-Photo** is a lightweight, fast personal photo server in the style of **Google Photos**, created specifically for **Keenetic** routers with a USB port and **Entware** environment (as well as for Linux and Windows).

The service automatically indexes photos from a connected USB drive (flash drive, external hard drive or SSD), creates an endless photo feed by date, generates and caches thumbnails on the fly, extracts detailed EXIF ​​data and provides a modern web interface in a dark theme (Glassmorphism).

---

## 🌟 Main features

- 📸 **Google Photos-photo feed style**:
  - Infinite smooth scrolling (Infinite Scroll) with loading on the fly without freezing the browser.
  - Sticky headlines grouped by day ("Today", "Yesterday", "August 28, 2026").
  - Adaptive grid of photo cards with lazy loading of thumbnails.
- 🔍 **Full screen viewer (Lightbox)**:
  - Smooth zooming (zoom with the mouse wheel or buttons) and panning.
  - Rotate a photo 90° in one click.
  - Automatic slide show mode with timer.
  - Detailed **EXIF information** panel: camera, lens, shutter speed, aperture, ISO, focal length and direct link to OpenStreetMap if GPS coordinates are available.
  - Full keyboard control (arrows, spacebar, Esc, I, +, -) and swipe support on smartphones and tablets.
- ⚡ **Smart caching and thumbnail generation**:
  - Fast resize algorithm in pure Go without CGO (`CGO_ENABLED=0`).
  - Cache location to choose from: directly on a USB drive in `.smartphoto/thumbs` or in the system folder `/opt/var/cache/smart-photo`.
  - Two-level cache (fast RAM LRU memory + disk).
- 🛡️ **Caring about router resources**:
  - Configurable limiting of background threads (2 threads by default) prevents overheating and slowdown of Internet speed on Keenetic.
  - Storing the event log in RAM (RAM ring buffer) - zero wear on the router's flash memory.
- 📁 **Albums, folders and favorites**:
  - Navigation through the original folder structure on a flash drive.
  - Mark your favorite photos with a star in a separate “Favorites” section.
  - Search by file name, folder, camera model and year.
- 🩺 **Built-in diagnostics and control**:
  - View used disk space and cache size.
  - Auto-detection of connected USB devices (`/tmp/mnt/...`).

---

## 🚀 Quick installation on a Keenetic router

### 1. Automatic installation via OPKG (in 1 command):

Connect to the router via SSH and run:

```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-photo
```

After installation is complete, the web interface will be available at:
👉 **`http://192.168.1.1:8089`** (or the IP of your router).

---

### 2. Manual connection via the OPKG repository:

```bash
# 1. Добавьте репозиторий snakelair/Keenetic в Entware:
ARCH=$(uname -m | sed 's/mips/mipsel-3.4/' | sed 's/aarch64/aarch64-3.10/' | sed 's/armv7l/armv7-3.2/')
echo "src/gz keenetic-custom https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/entware/${ARCH}" > /opt/etc/opkg/keenetic.conf

# 2. Обновите список пакетов и установите:
opkg update
opkg install smart-photo
```

---

## 🌐 Compatible with Keenetic models

|Architecture|Supported router models|
| :--- | :--- |
| **`mipsel-3.4`** | Keenetic Viva, Extra, Speedster, Giga (KN-1010/1011), Omni, Skipper, Air, Buddy |
| **`armv7-3.2`** | Keenetic Hero (KN-1011/KN-1012), Titan (KN-1810), Giant (KN-2610), Ultra (KN-1810) |
| **`aarch64-3.10`** | Keenetic Peak (KN-2710), Ultra (KN-1811), Titan (KN-1812), Hero 4G+ (KN-2311) |
| **`x86_64`** |Virtual machines Keenetic / Entware x86|

---

## 📱 Client applications

- **SmartPhotoSync (Android)**: Background automatic synchronization of photos from smartphones via Wi-Fi.
👉 [Download SmartPhotoAndroid.apk](https://github.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/raw/main/apk/SmartPhotoAndroid.apk)
- **SmartPhotoTV (Android TV)**: View your photo archive on your TV screen with remote control support.
👉 [Download SmartPhotoTV.apk](https://github.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/raw/main/apk/SmartPhotoTV.apk)
- **WebDAV**: Direct connection to your media library on iPhone/iPad (system Files app), macOS and Windows.

---

## 📜 License

MIT License © 2026 snakelair
