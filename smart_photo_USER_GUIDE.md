# 📘 Smart-Photo User Guide

**Smart-Photo** is a personal photo server and viewer for Keenetic routers with USB drives and the Entware environment.

---

## 1. Getting started

### Step 1: Connect a USB drive to the Keenetic router
1. Connect a USB flash drive or external HDD/SSD to the USB port of the Keenetic router.
2. In the Keenetic router web interface (in the **Network drives and USB** section), make sure the drive is mounted.
3. The default mount point in Entware is `/tmp/mnt/` (for example, `/tmp/mnt/DISK_NAME/Photos`).

### Step 2: Install Smart-Photo
Run the following command from the router's SSH console:
```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-photo
```

### Step 3: Open the web interface
Open your browser and go to:
👉 `http://192.168.1.1:8089`

---

## 2. Setting up a photo folder and cache

Go to the **⚙️ Settings** tab:
1. **Photo folder**: specify the path to the directory with your photos on the USB drive (for example: `/tmp/mnt/USB_DRIVE/DCIM` or `/tmp/mnt/USB_DRIVE/Photos`).
2. **Cache location**:
   - *At the root of the photo folder (`.smartphoto/thumbs`)*: recommended! Thumbnails are saved directly on the flash drive, do not consume the router memory, and are not recreated after reboot.
   - *Custom path*: you may specify a specific folder (for example `/opt/var/cache/smart-photo`).
3. **Thumbnail generation threads (CPU Throttle)**:
   - For routers with a MIPS processor (Viva, Extra, Speedster, Omni, Giga), **1-2 threads** are recommended.
   - For Hero, Titan, Ultra, and Peak, you may install **2-4 threads**.
4. Click **Save Settings**.

---

## 3. Using the photo viewer

### Infinite timeline
- Photos are automatically arranged in chronological order from newest to oldest.
- When you scroll down the page, new photos are loaded automatically without delay.
- As you scroll, sticky titles with the capture date appear on the screen.

### Full-screen viewer (Lightbox)
- Clicking on any photo opens it in full-screen mode with a darkened background.
- **Zoom**: use the mouse wheel or the `+` / `-` buttons for detailed viewing.
- **Pan**: hold the left mouse button on the enlarged image and move it.
- **Rotate**: the rotate button or key allows you to rotate the image 90 degrees.
- **Slide show**: press the **Play** button or the **Space** key to enable automatic slideshow.
- **Photo details (EXIF)**: press the `(i)` button or the `I` key to open the side panel with camera parameters (shutter speed, ISO, aperture, lens model) and GPS coordinates.

### Hotkeys:
- `Left` / `Right` — previous / next photo
- `Esc` — close full-screen mode
- `Space` — enable/disable slideshow
- `I` — open/hide the EXIF panel
- `+` / `-` — zoom in / out
- `0` — reset zoom to 100%

---

## 4. Managing the service on the router via SSH

```bash
# Start the service
/opt/etc/init.d/S99smart-photo start

# Stop the service
/opt/etc/init.d/S99smart-photo stop

# Restart the service
/opt/etc/init.d/S99smart-photo restart

# Check status and logs
/opt/etc/init.d/S99smart-photo check
```

---

## 5. Complete removal of Smart-Photo

### Automatically:
```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s smart-photo
```

### Manually via SSH:
```bash
/opt/etc/init.d/S99smart-photo stop
killall -9 smart-photo 2>/dev/null
opkg remove smart-photo --force-remove --force-depends
rm -f /opt/etc/init.d/S99smart-photo /tmp/smart-photo.log /opt/var/log/smart-photo.log
rm -rf /opt/etc/smart-photo /opt/var/cache/smart-photo
```
