# 📘 Smart-Photo User Guide

**Smart-Photo** is a personal photo server and viewer for Keenetic routers with USB drives and Entware environment.

---

## 1. Getting started

### Step 1: Connecting a USB drive to Keenetic
1. Connect a USB flash drive or external HDD/SSD to the USB port of the Keenetic router.
2. In the Keenetic router web interface (in the “Network drives and USB” section), make sure that the drive is mounted.
3. The default mount point in Entware is `/tmp/mnt/` (for example, `/tmp/mnt/DISK_NAME/Photos`).

### Step 2: Install Smart-Photo
Execute through the SSH console of the router:
```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s smart-photo
```

### Step 3: Open the web interface
Open your browser and go to:
👉 `http://192.168.1.1:8089`

---

## 2. Setting up a photo folder and cache

Go to the **⚙️Settings** tab:
1. **Folder with photos**: specify the path to the directory with your photos on the USB drive (for example: `/tmp/mnt/USB_DRIVE/DCIM` or `/tmp/mnt/USB_DRIVE/Photos`).
2. **Cache location**:
   - *At the root of the photo folder (`.smartphoto/thumbs`)*: recommended! Thumbnails are saved directly on the flash drive, do not consume the router’s memory and are not recreated during reboots.
   - *Custom path*: You can specify a specific folder (for example `/opt/var/cache/smart-photo`).
3. **Thumbnail generation threads (CPU Throttle)**:
   - For routers with a MIPS processor (Viva, Extra, Speedster, Omni, Giga) **1-2 streams** are recommended.
   - For Hero, Titan, Ultra, Peak you can install **2-4 streams**.
4. Click **Save Settings**.

---

## 3. Using the photo viewer

### Infinite Timeline
- Photos are automatically arranged in chronological order from top to bottom from newest to oldest.
- When you scroll down the page, new photos are loaded automatically without delay.
- As you scroll, sticky titles with the shooting date appear on the screen.

### Full screen viewer (Lightbox)
- Clicking on any photo opens it in full screen mode with the background darkened.
- **Zoom**: Roll the mouse wheel or press the `+` and `-` buttons to view the photo in detail.
- **Panning**: hold down the left mouse button on the enlarged photo and move it.
- **Rotate**: The rotate button or key allows you to rotate the photo 90 degrees.
- **Slide Show**: Press the `Play` button or the `Пробел` button to enable automatic slide show.
- **Photo Details (EXIF)**: Press the `(i)` button or the `I` key on your keyboard. A side panel will open with camera parameters (shutter speed, ISO, aperture, lens model) and GPS coordinates with a button to go to the map.

### Hotkeys:
- `Влево` / `Вправо` - previous / next photo.
- `Esc` — close full screen mode.
- `Пробел` — enable/disable the slideshow.
- `I` — open/hide the EXIF ​​options panel.
- `+` / `-` — enlarge / reduce the photo.
- `0` — reset the scale to 100%.

---

## 4. Managing the service on the router via SSH

```bash
# Запуск службы
/opt/etc/init.d/S99smart-photo start

# Остановка службы
/opt/etc/init.d/S99smart-photo stop

# Перезапуск службы
/opt/etc/init.d/S99smart-photo restart

# Проверка статуса и логов
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
