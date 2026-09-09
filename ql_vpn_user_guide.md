# 🎮 QuakeLive-VPN - User Guide and Architecture

**QuakeLive-VPN** is a new generation high-speed stealth tunnel, the network traffic of which is completely disguised as the real multiplayer of the cult online shooter **Quake Live** based on the **id Tech 3 NetChan** engine.

---

## 🎯 1. What is the main idea of ​​QuakeLive-VPN?

Modern deep packet analysis (DPI) systems block standard VPN protocols (WireGuard, OpenVPN, IPSec) based on characteristic headers, handshake sizes and payload entropy.

**QuakeLive-VPN solves this problem in a fundamentally different way:**
1. **100% disguised as game traffic:** All tunnel packets are formatted in strict accordance with the Quake Live NetChan protocol (OutOfBand packets `getchallenge`, `challengeResponse`, `connect`, commands `clc_move`, snapshots `svc_snapshot` and `svc_packetentities`).
2. **Absolute resistance to blocking:** Not a single TSPU or DPI filter distinguishes the work of a VPN from a real network match of players on a Quake Live server.
3. **Minimum overhead and ultra-low ping:** Pure UDP protocol without multi-layer TLS overhead, with hardware accelerated AES-128-GCM and ChaCha20-Poly1305 encryption.
4. **Built-in game scoreboard:** The server responds to standard game status requests (`getstatus`/`getinfo`), displaying connected clients as real players (Sarge, Ranger, Crash) in the classic Campgrounds arena (`q3dm6`).

---

## 🚀 2. Quick server installation on Linux VPS

### Automatic installation in one command:

Connect to your VPS server (Ubuntu, Debian, CentOS, Rocky Linux, Alpine) via SSH and run:

```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install-qlvpn.sh | bash
```

*or through the universal repository script:*
```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/install.sh | sh -s ql-vpn
```

### What the installation script does:
1. Automatically detects the server's processor architecture (`x86_64` or `aarch64/arm64`).
2. Requests ports (default: game UDP `:27960`, HTTPS web panel `:8092`) and administrator password.
3. Enables packet forwarding in the Linux kernel (`net.ipv4.ip_forward = 1`).
4. Configures `iptables` firewall rules (NAT MASQUERADE for `10.80.0.0/24` subnet, FORWARD chains and INPUT ports).
5. Loads the optimized `ql-vpn` binary into `/usr/local/bin/ql-vpn`.
6. Creates and starts the system service `systemd` (`ql-vpn.service`) with autostart when the server boots.
7. Generates the first ready client connection token `qlvpn://...` and outputs a summary summary.

---

## 💻 3. Client connection

### 3.1. Windows Client (GUI + Tray)

1. Run `ql-vpn.exe` as an administrator on your computer.
2. The application will minimize to the Windows system tray (an icon with the gothic Quake Live logo).
3. Open the control panel (`http://127.0.0.1:8092`) or click on the tray icon.
4. Insert the `qlvpn://...` token received during installation and click the **Connect** button.
5. Select routing mode:
   - **All traffic (0.0.0.0/0):** All Internet traffic on your PC is protected and goes through the tunnel.
   - **Game traffic only:** Only Quake Live game traffic is redirected.
   - **Custom Routes:** Specify specific IP addresses and subnets to bypass blocking.

> [!TIP]
> **Management through three Windows**:
> When you right-click on the tray icon, the following items are available:
> - “Open control panel”
> - “Connect / Disconnect”
> - “Run minimized”
> - “Exit” - when exiting, the application correctly closes the configurator window, safely disables the Wintun adapter and frees system routes, **without affecting your main browser (Google Chrome, Edge)**.

### 3.2. Keenetic routers (Smart-VPN)

If the **Smart-VPN** package (`http://192.168.1.1:8091`) is installed on the router:
1. Go to the **"QuakeLive-VPN"** tab.
2. Paste the `qlvpn://...` token into the input field and click **Add Server**.
3. The router will establish a tunnel and be able to route home traffic through your VPS.

---

## ⚙️ 4. Web server control panel (HTTPS)

The VPS server has an independent web administration center:
- **URL:** `https://<IP_сервера>:8092`
- **Login:** `admin`
- **Password:** specified during installation

### Web panel features:
- **Token management:** Create unique access keys for different players and devices with a time limit or assigning a permanent virtual IP (`10.80.0.X`).
- **Player board:** Interactive table of connected clients with network handshake status, ping, amount of transmitted traffic and time on the network.
- **Built-in self-updating system:** When new releases appear, an update badge appears in the panel header. Updating the binary and restarting the service are performed in one click directly from the browser.
- **Integration with a real Quake Live server:** Ability to specify the IP of the upstream server for inconspicuous and transparent proxying of matches.

---

## 🛠️ 5. Managing the service on VPS manually

```bash
# Проверить статус службы:
systemctl status ql-vpn

# Перезапустить сервер:
systemctl restart ql-vpn

# Просмотр журналов в реальном времени:
journalctl -u ql-vpn -f

# Генерация нового токена через консоль:
ql-vpn token add -server "ВАШ_IP:27960" -name "PlayerName" -tokens /etc/ql-vpn/tokens.json
```

---

## 📂 6. Where are all the files located on the VPS (detailed system map)

After installation on a Linux VPS, all executable files, databases, startup services and system settings are located in standardized Linux paths:

### 🗺️ Hierarchy of files and directories

```
/
├── usr/local/bin/
│   └── ql-vpn                         # 🟢 Основной бинарный исполняемый файл
│
├── etc/
│   ├── ql-vpn/                        # 📁 Каталог данных и конфигурации
│   │   ├── tokens.json                # 🔑 База клиентских токенов и ключей PSK
│   │   ├── qlvpn-server.json          # ⚙️ Сохраненные настройки сервера и веб-панели
│   │   └── qlvpn-client-servers.json  # 🌐 Список серверов (для режима клиента)
│   │
│   ├── systemd/system/
│   │   └── ql-vpn.service             # 🚀 Юнит-файл автозапуска службы systemd
│   │
│   ├── sysctl.d/
│   │   └── 99-qlvpn.conf              # 🌐 Включение IPv4 Forwarding в ядре Linux
│   │
│   └── iptables/                      # (Debian/Ubuntu)
│       └── rules.v4                   # 🛡️ Персистентные правила NAT MASQUERADE
│
└── tmp/
    └── ql-vpn.new                     # ⏳ Временный файл при самообновлении
```

### 📄 Detailed description of each file and component

#### 1. Server executable file: `/usr/local/bin/ql-vpn`
- **Type:** A compiled Go binary (`ELF 64-bit LSB executable`, `x86-64` or `ARM aarch64`), with no external runtime dependencies.
- **Purpose:**
  - Works in the background as a system server daemon (UDP port `:27960`, web panel `:8092`).
  - Serves as a CLI utility for managing tokens:
    ```bash
    /usr/local/bin/ql-vpn token list -tokens /etc/ql-vpn/tokens.json
    /usr/local/bin/ql-vpn token add -server "IP:27960" -name "Player1" -tokens /etc/ql-vpn/tokens.json
    /usr/local/bin/ql-vpn token del -name "Player1" -tokens /etc/ql-vpn/tokens.json
    ```
  - When you launch an update via the web panel, it is automatically replaced with the latest version from the repository.

#### 2. Client token database: `/etc/ql-vpn/tokens.json`
- **Type:** Database file in JSON format.
- **Example content:**
  ```json
  [
    {
      "name": "Ranger",
      "key": "a61b384becd4b14fe035777d3d5e268e7aba668594ea79b595fe2ffda1b7fdb3",
      "assigned_ip": "10.80.0.2",
      "routes": ["0.0.0.0/0"],
      "dns": ["1.1.1.1", "8.8.8.8"],
      "created": 1788553827,
      "exp": 0
    }
  ]
  ```
- **Purpose:** Stores a list of clients, their pre-shared keys (PSK), allocated static IP addresses within the `10.80.0.0/24` subnet, routes and lifetime. Any changes in the web panel (creation, deletion of a token) are instantly and atomically synchronized with this file.

#### 3. Server settings: `/etc/ql-vpn/qlvpn-server.json`
- **Type:** Status file in JSON format (created when changing parameters via the web panel).
- **Example content:**
  ```json
  {
    "enabled": true,
    "port": 27960,
    "web_port": 8092,
    "web_password": "Pass-ВашПароль",
    "use_tls": true,
    "upstream_server": ""
  }
  ```
- **Purpose:** Provides persistence of web panel settings (ports, administrator password, TLS encryption and Quake Live upstream server address).

#### 4. Systemd service: `/etc/systemd/system/ql-vpn.service`
- **Type:** Standard systemd init service unit file.
- **Content:**
  ```ini
  [Unit]
  Description=QuakeLive-VPN Server and Web Control Daemon
  After=network.target

  [Service]
  Type=simple
  User=root
  ExecStart=/usr/local/bin/ql-vpn -server -port 27960 -web-port 8092 -tls -web-pass "Pass-..." -tun 10.80.0.1/24 -tokens /etc/ql-vpn/tokens.json
  Restart=always
  RestartSec=3

  [Install]
  WantedBy=multi-user.target
  ```
- **Purpose:** Provides automatic start of the service when the OS boots and continuous monitoring of the process (restart after 3 seconds in case of failure or normal restart).

#### 5. Kernel Packet Forwarding (Sysctl): `/etc/sysctl.d/99-qlvpn.conf`
- **Content:**
  ```ini
  net.ipv4.ip_forward = 1
  ```
- **Purpose:** Enables forwarding of IPv4 packets at the Linux kernel level between the virtual tunnel `qlvpn0` and the external physical interface of the server (`eth0` / `ens3`).

#### 6. Firewall rules (IPTables): `/etc/iptables/rules.v4`
- **Purpose:** Saves network address translation rules:
  - **NAT MASQUERADE:** `iptables -t nat -A POSTROUTING -s 10.80.0.0/24 ! -d 10.80.0.0/24 -j MASQUERADE`
  - **FORWARD:** allows packets to pass between `10.80.0.0/24` and the external interface.
  - **INPUT:** opens incoming ports UDP `:27960` and TCP `:8092`.

#### 7. Network virtual interface TUN: `qlvpn0`
- **Type:** Linux kernel virtual network device (`/dev/net/tun`).
- **Options:** IP `10.80.0.1/24`.
- **View:** `ip addr show qlvpn0` or `ip -s link show dev qlvpn0`.

---

### 📋 Cheat sheet on useful admin commands

|Operation|Command to VPS servers|
| :--- | :--- |
|**Check service status**| `systemctl status ql-vpn` |
|**Restart server**| `systemctl restart ql-vpn` |
|**View event log online**| `journalctl -u ql-vpn -f` |
|**Last 50 lines of log**| `journalctl -u ql-vpn -n 50 --no-pager` |
|**View token database**| `cat /etc/ql-vpn/tokens.json` |
|**Create a token manually**| `/usr/local/bin/ql-vpn token add -server "IP:27960" -name "Sarge" -tokens /etc/ql-vpn/tokens.json` |
|**Remove token**| `/usr/local/bin/ql-vpn token del -name "Sarge" -tokens /etc/ql-vpn/tokens.json` |
|**Check network tunnel**| `ip addr show qlvpn0` |
|**Check NAT traffic counters**| `iptables -t nat -L POSTROUTING -n -v` |
|**Complete removal of server from VPS**| `curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh \| sh -s ql-vpn` |

---

## 🗑️ 6. Complete removal of QuakeLive-VPN from the VPS server

### Automatically:
```bash
curl -sSL https://raw.githubusercontent.com/DFR11/Snakelair-Keenetic-Entware-OPKG-Repository/main/uninstall.sh | sh -s ql-vpn
```

### Manually:
```bash
systemctl stop ql-vpn && systemctl disable ql-vpn
killall -9 ql-vpn 2>/dev/null
rm -f /usr/local/bin/ql-vpn /etc/systemd/system/ql-vpn.service /etc/sysctl.d/99-qlvpn.conf
rm -rf /etc/ql-vpn
systemctl daemon-reload
```

