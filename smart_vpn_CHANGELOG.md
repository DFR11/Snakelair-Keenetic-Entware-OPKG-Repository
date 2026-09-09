# SmartVPN change history

## [1.0.65] - 2026-09-05
### Fixed and Improved
- **Protecting the main browser (Google Chrome, Edge, Firefox) from closing when exiting the Windows tray**:
  - Fixed an issue where closing from the tray would send a system message `WM_CLOSE` to a Google Chrome window with a configurator tab, causing the user's entire browser to close with all working tabs.
  - Strict window validation has been implemented in `isDedicatedAppWindow()`: browser windows (`Chrome`, `Edge`, `Firefox`, `Opera`, `Brave`, `Yandex`, etc.) are completely excluded from sending `WM_CLOSE`. Only selected standalone application windows are closed in the `--app` mode (with the exact title `QuakeLive-VPN Control Center`).
  - For the scenario where the configurator is opened in a regular browser tab (where the security policy blocks the forced call to `window.close()`), the tab goes into a neat sleep mode with a "🛑 QuakeLive-VPN has completed" screen, completely stopping timers, background polling and keeping the user's browser completely secure.

## [1.0.64] - 2026-09-05
### Added and Improved
- **Automatic closing of the configurator window when exiting the Windows system tray (QL-VPN)**:
  - Implemented instant and guaranteed closing of the configurator window (`http://127.0.0.1:8092`) when you click “Exit” in the tray context menu, upon a process completion signal, or via the `/api/exit` API.
  - A two-level closing mechanism has been introduced:
    1. **Frontend Event**: The web interface is connected to the Server-Sent Events (SSE) stream `/api/events` and monitors the `app_exiting` flag in the status. When a close signal is received, JavaScript `window.close()` is immediately called, immediately closing the application in `--app` mode (Chromium/Edge/Chrome).
    2. **Win32 Message Pump**: The server searches and closes the configurator window via the Win32 API (`OpenDesktopW`, `EnumDesktopWindows` / `EnumWindows`, `GetWindowTextW`), sending a message `WM_CLOSE` (0x0010) to windows with the title "QuakeLive-VPN" Control Center" and "127.0.0.1:8092".
  - Added correct and clean tunnel termination (`state.DisconnectTunnel()`): resetting the routing table, deleting the Wintun interface and closing the tray icon without freezing.

## [1.0.63] - 2026-09-05
### Fixed and Improved
- **Fix traffic routing (0.0.0.0/0) in the Windows QL-VPN client**:
  - Implemented dynamic assignment of an IP address to the Wintun adapter (`SetIP`) immediately after completing a handshake with the server. Previously, for tokens with a dynamic IP (`assigned_ip: ""`), the call to `netsh set address` was skipped, which left the adapter without an address and unable to receive/send traffic.
  - The gateway and route binding have been fixed: the routes `0.0.0.0/1` and `128.0.0.0/1` are now routed to the server gateway `10.80.0.1` with the mandatory indication of the adapter's Wintun index (`if <wintunIfIndex>`). This eliminates spurious ARP requests on the point-to-point Layer 3 interface.
  - Added cleaning of outdated routes before adding them to prevent conflicts.
  - The DNS setting on the Wintun adapter has been switched to safe mode with the `validate=no` flag, eliminating the `netsh` hang.
  - The Wintun interface metric is set to `1` to ensure that the tunnel takes precedence over physical adapters when resolving DNS.
  - Fixed subnet blocking by the built-in server on Windows: the client GUI no longer starts the local `qlsrv0` server by default, freeing up the `10.80.0.0/24` subnet for the `qlvpn0` client tunnel.
- **Automatic NAT MASQUERADE and IPv4-Forwarding on Linux VPS server**:
  - When starting the `ql-vpn` server on the Linux kernel, `net.ipv4.ip_forward = 1` is now automatically enabled through `procfs` and `sysctl`.
  - Added automatic configuration of `iptables` NAT MASQUERADE rules for the `10.80.0.0/24` subnet on all outgoing interfaces (`! -d 10.80.0.0/24 -j MASQUERADE`).
  - Added `FORWARD` chain rules for forward (`-s 10.80.0.0/24`), reverse (`-d 10.80.0.0/24`) and consistent (`-m conntrack --ctstate RELATED,ESTABLISHED`) traffic.
  - Updated systemd and SSH deployment scripts.

## [1.0.62] - 2026-09-05
### Added and Improved
- **Self-updating system in the QL-VPN server (VPS only)**:
  - Implemented version monitoring and automatic display of the “⚡ Available: vX.X.X” badge in the panel header when new releases appear.
  - Built-in interactive modal window displaying the current and available versions, a list of changes (Changelog diff) and a “🚀 Update now” button.
  - Securely download the latest GitHub binary for the server architecture (`amd64` / `arm64`), replace the `/usr/local/bin/ql-vpn` executable, restart the systemd service and live terminal the update process.
  - The self-updating system is active exclusively on VPS (Linux), without interfering with client Windows builds.
- **Self-updating system in SmartVPN (Keenetic routers)**:
  - Added a version badge and a pulsating update badge in the header of the router web interface.
  - Integrated modal window with a detailed list of changes between the installed and new version in the same style of the SmartUtils ecosystem.
  - Support for fast update of OPKG package (`opkg update && opkg install --force-reinstall smart-vpn`) and background restart of service `/opt/etc/init.d/S99smart-vpn`.
  - A backup mechanism for directly downloading a binary for the router processor architecture in the absence of an OPKG repository.
  - Streaming terminal updates and automatic page reload after connection is restored.

## [1.0.61] - 2026-09-04
### Fixed and Improved
- **Synchronization and hot reboot of QL-VPN server tokens (handshake error fix)**:
  - Fixed desynchronization of token stores on the server: the web panel manager and the UDP server now share a single object `TokenStore`. Previously, tokens created through the web interface were saved to a separate file and were not loaded into the running daemon, causing the server to reject connections from created clients with Quake Live status.
  - Implemented automatic polling of the change time of the token database file (`os.Stat` modtime) with each access: any tokens added via the CLI (`token add`) or edited on disk are loaded into memory instantly and without restarting the process.
  - Added automatic merging of adjacent token files (`tokens.json` and `qlvpn-tokens.json`), ensuring the preservation of all previously created clients.
  - Improved client handshake error reporting: if the server rejects a connection due to an unregistered token, the client displays the exact message instead of a generic timeout.
  - In the VPS deployment script, the generation of the first client token was moved before the start of the systemd service.

## [1.0.60] - 2026-09-04
### Added and Improved
- **Full traffic routing on Windows (Wintun TUN + Split Tunneling)**:
  - Integrated high-performance TUN adapter driver Wintun (Microsoft WHQL) without CGO and third-party external dependencies. The official libraries `wintun_amd64.dll` and `wintun_arm64.dll` are built in via the `//go:embed` directive exclusively for building under Windows (without increasing the size of the binaries for routers).
  - Implemented secure routing of all traffic (`0.0.0.0/0`) through two balanced prefixes `/1` (`0.0.0.0/1` and `128.0.0.0/1`), which prevents packet looping and preserves the default physical gateway.
  - Implemented automatic search for the default physical gateway via the Win32 API `GetBestRoute` (`iphlpapi.dll`) and adding a protective host route to the VPN server.
  - Implemented split routing (Split Tunneling) for user-specified CIDR subnets.
  - Added automatic configuration of tunnel DNS servers (1.1.1.1, 8.8.8.8) and clearing of all added routes when the process is disabled or terminated.
- **Windows tray integration and “Run minimized” option**:
  - An item with a dynamic checkbox `[✓] Запускать свернутым` has been added to the Windows system tray context menu.
  - The “Run minimized to Windows system tray” checkbox has been added to the “Traffic Routing (Split Tunneling)” card of the web panel.
  - The option state is automatically saved in the local configuration (`qlvpn_client_settings.json`), synchronized between the tray and the web panel in real time, and prevents the browser window from popping up when the client autostarts.
- **Automatic request for UAC administrator rights**:
  - When the client is launched on Windows in GUI or CLI mode, administrator rights are checked (`OpenProcessToken`, `GetTokenInformation`) and automatic restart with elevated privileges (`ShellExecuteW("runas")`) is implemented to correctly create a network adapter and change the OS routing table.

## [1.0.59] - 2026-09-04
### Added and Corrected
- **Support for adding and saving multiple servers in the “QL-VPN Client”**:
  - The problem of server overwriting has been fixed: client tokens and servers are now identified by the composite key `(Сервер, Имя клиента)`, which allows you to add an unlimited number of different servers even with the same player nickname (`Sarge`, etc.).
  - In the interface of the router and the standalone VPS panel, a **“➕Add to list”** button has been added next to the connection button, which allows you to save servers to the list without immediately breaking the current connection.
  - Added persistent server storage of client servers on the router (`qlvpn-client-servers.json`) and REST API endpoints `GET/POST/DELETE /api/qlvpn/client/servers`.
  - In the cards of saved servers, the ability to edit the server address/domain, copy the token, connect and remove the server from the list has been added.
  - Client connections no longer pollute the white list of tokens on the router's local server.

## [1.0.58] - 2026-09-04
### Corrected
- **Fixed JavaScript syntax and tabs in the VPS web panel**:
  - Fixed a syntax error (missing closing curly brace in the `try/catch` block of the `saveServerPort` method) in the built-in JavaScript of the QL-VPN web admin (`gui.go`), which led to the failure of parsing the script by the browser and blocking the switching of subtabs.
  - Performed JavaScript syntax validation via the Node.js CLI.

## [1.0.57] - 2026-09-04
### Changed and Improved
- **Reorganization of QuakeLive-VPN interfaces on the router and dedicated server**:
  - In the SmartVPN interface on the router, the tab has been renamed from “Server on the router” to “QL-VPN Server”.
  - The Quake Live server game UDP port setting has been moved directly to the “QL-VPN Server” tab with instant application and a reset button to the default port `27960`.
  - In the SmartVPN interface on the router, the unnecessary “Settings” subtab has been removed.
  - On the dedicated server (`ql-vpn`), the tab is renamed to “Control Panel Settings” and contains only the control panel port and web interface password parameters.
  - Added API endpoint `POST /api/qlvpn/server/port` (and `/api/server/port` on the server) for dynamically changing the working UDP port.

## [1.0.56] - 2026-09-04
### Added and Improved
- **Browser of official Quake Live servers from Steam Master Server with ping measurement**:
  - Implemented automatic polling of active public Quake Live servers from the global Steam Master Server catalog, with priority for servers with live players and nearby regions.
  - Built-in Steam A2S_INFO protocol network benchmark (`TSource Engine Query` with support for 4-byte challenge response) with an ultra-fast parallel pool of workers to measure real network latency (RTT ping in milliseconds).
  - Results are automatically sorted by ascending ping (lowest latency on top) with caching of results to reduce network load.
  - In the QL-VPN web admin interface (`gui.go`) and the Keenetic router interface (`index.html` + `qlvpn.js`) the **🌐 Select from Steam** button and a modal window for selecting an upstream server with live search/filtering, country flags, map, game mode, number of players and colored badges have been added ping.
  - Selecting a server in one click substitutes the address into the settings fields of the upstream server and activates proxying.
  - The `GET /api/qlvpn/upstream/servers` route has been added to the API (with support for the `refresh=1` parameter to force delay re-measurement).

## [1.0.55] - 2026-09-04
### Fixed and Improved
- **Binary update fix and guaranteed service restart on VPS**:
  - In the remote installation script `buildRemoteInstallerScript`, added stopping the existing `systemctl stop ql-vpn` service and ending processes before updating, which eliminates the blocking of the `Text file busy` (ETXTBSY) file.
  - Binary loading has been switched to atomic replacement via a temporary file (`ql-vpn.tmp` -> `mv -f`).
  - Instead of `systemctl enable --now`, an explicit call to `systemctl restart ql-vpn` has been added to ensure that the updated service is started immediately with the parameters `-tls` and `-web-pass`.
  - All compiled v1.0.55 binaries are synchronized in a common repository `snakelair/Keenetic`.

## [1.0.54] - 2026-09-04
### Added and Improved
- **Server settings tab in the web admin with the ability to change ports and password**:
  - A separate tab has been added to the QL-VPN standalone web admin (`gui.go`) and the Keenetic router interface (`index.html`, `qlvpn.js`) **⚙️ Server settings**:
    - **Game UDP Port**: Change and save Quake Live server port (default 27960 UDP) with dynamic UDP socket restart on the fly.
    - **Web admin port**: change the control panel port (default 8091) with automatic browser redirection to the new address after saving.
    - **Web admin password**: set, change and delete a password to access the web panel (Basic Auth `admin:<пароль>` and Bearer Token) with a view button (👁️) and a strong random password generator (🎲).
    - **Upstream Quake Live server**: setting up and switching upstream proxy server (`51.195.126.72:27960` or local emulation).
  - On remote Linux VPS, when the settings are changed, the systemd unit file `/etc/systemd/system/ql-vpn.service` is automatically updated, `systemctl daemon-reload` is called, and the firewall rules `iptables` are updated for new ports.
  - Web server authorization `StartGUIServer` has been moved to dynamically validate the password on every request, instantly applying changes without restarting the daemon.
  - Endpoints `GET /api/qlvpn/settings` and `POST /api/qlvpn/settings` have been added to the router API with parameters saved in `qlvpn-server.json`.

## [1.0.53] - 2026-09-04
### Fixed and Improved
- **Password authentication fix when deploying to VPS via SSH**:
  - Fixed error `ssh_askpass: exec(/usr/bin/ssh-askpass): No such file or directory` when connecting via OpenSSH with password authentication.
  - Implemented a cross-platform dynamic helper `SSH_ASKPASS` (`.cmd` on Windows, `POSIX sh` on Linux/macOS), correctly and securely transmitting the password to the client `ssh` in non-interactive mode.
  - On the Keenetic router, explicit recognition of the Dropbear client (`/opt/bin/dbclient`) has been added, with the correct transmission of the `DROPBEAR_PASSWORD` variable.
  - Added `-o PreferredAuthentications=publickey,password,keyboard-interactive` flags to OpenSSH parameters and correct `UserKnownHostsFile` redirection (to `NUL` on Windows and `/dev/null` on Linux).

## [1.0.52] - 2026-09-04
### Added and Improved
- **Deployment of the server web interface on HTTPS (TLS) with password protection**:
  - The QL-VPN subsystem has a built-in generator of self-signed TLS certificates ECDSA P-256 (`internal/qlvpn/tls.go`) with a validity period of 10 years, running on a pure standard Go library (`crypto/tls`, `crypto/x509`, `crypto/ecdsa`) without external utilities (openssl) and temporary files on disk.
  - The management web server `StartGUIServer` supports HTTPS encryption (`tls.NewListener`) and HTTP Basic Auth / Bearer Token authorization using the password `WebPassword`.
  - A web admin password field with a button for quickly generating a strong random password (`🎲 Случайный`) has been added to the deployment form on VPS (“Deploy to VPS via SSH”). If you leave the field empty, the server automatically generates a random password in the format `Pass-xxxxxxxx`.
  - The remote systemd service on the VPS is deployed with the `-tls -web-pass "$WEB_PASS"` flags.
  - After successful completion of deployment, the result card displays a direct HTTPS link (`https://$HOST:$WEB_PORT`), login `admin`, a generated password with a copy button, and an access token `qlvpn://`.
  - Flags `-tls`, `-cert`, `-key-file`, `-web-pass` have been added to the `ql-vpn` binary to manage security and certificates in all modes (`-server`, `-web`, `-gui`).

## [1.0.51] - 2026-09-04
### Fixed and Improved
- **Removing outdated references to the map `q3dm6`**:
  - Mentions of the `q3dm6` map have been completely removed from the web interface, standalone GUI, badges and system logs.
  - In Quake Live, the `getstatus` probe has been installed with the official standard map `campgrounds` instead of the non-existent `pak00.pk3` map `q3dm6`.
  - Updated emulation mode tooltips: removed outdated links to “3-line banner with auto-shutdown 5 sec”, texts are consistent with the current architecture (rejecting connections with server status).

## [1.0.50] - 2026-09-04
### Fixed and Improved
- **Hide the console for the Windows client (`ql-vpn.exe`)**:
  - The Windows binary `ql-vpn.exe` is built with the `-H=windowsgui` flag (Windows GUI subsystem), excluding automatic creation of a console window (`conhost.exe`) by the operating system when launched from Explorer or a shortcut.
  - Added function `hideConsoleWindow()` with calls `GetConsoleWindow()`, `ShowWindow(SW_HIDE)` and `FreeConsole()`, which is guaranteed to hide and detach the console when running a Windows client in GUI/Tray mode.
  - The `attachParentConsole()` function is now called strictly when terminal utilities are explicitly launched (`token`, `-keygen`, `-probe-test`, `-help`), which preserves the convenience of working from the cmd/PowerShell console without opening unnecessary windows.
  - Build scripts `build.bat` and `build.ps1` are synchronized to automatically release a completed `dist/ql-vpn.exe` with GUI flags.

## [1.0.49] - 2026-09-04
### Added and Improved
- **Emulation of connection rejection "Server is full" via OOB print**:
  - The mechanism for rejecting connections in Quake Live / Quake 3 has been investigated: when the server is full or the connection fails, an Out-Of-Band datagram `\xff\xff\xff\xffprint\n<Message>\n` is sent.
  - When receiving `print\n...`, the Quake Live client (`quakelive_steam.exe`) immediately interrupts the connection process (`Com_Error(ERR_DROP)`) and displays the error text in a modal dialog in the game, completely eliminating delays and loading of map resources (`gamestate`).
  - In local emulation mode (without an upstream server), the server responds to `connect` with the server status in the `print\n` package and immediately stops the session.
- **Table “Clients” with live monitoring of status, uptime and speed**:
  - The “Issued client tokens” block has been redesigned into a full-fledged monitoring panel “Clients”.
  - Real-time connection status display (🟢 Online / ⚪ Offline).
  - Displaying network time (Uptime).
  - Displays the current transmission and reception speed (↑ UL / ↓ DL in KB/s and MB/s), as well as the total amount of data transferred.
- **Deleting the scoreboard of active players**:
  - The “🏆 Active players on the server” block has been removed from the web interface, freeing up space for client monitoring.
- **Proxying to an upstream Quake Live server**:
  - Added `🎯 51.195.126.72:27960` preset to the server control panel.
  - With an upstream server installed, real Quake Live players are transparently redirected to the remote server and QL-VPN tunnels are handled locally.

## [1.0.48] - 2026-09-04
### Added and Improved
- **Compact 1-line message `CS_MESSAGE`**:
  - Message `CS_MESSAGE` (ConfigString 3) has been converted to a strict single-line format of compact length (~33 visible characters):
    `^2[ONLINE] ^5SmartVPN :%d ^7|^5Cl: ^3%d^7/^316` (или `^3[PORT] ...` when there is a port conflict).
  - The string fits perfectly along the length of the `^2[ONLINE] ^5SmartVPN Keenetic Server` reference and is transmitted in the first NetChan packet via `cs 3` and `print`.
- **Stop loading until `gamestate`**:
  - The download stops immediately after sending `CS_MESSAGE`, before sending the heavy packet `svcGamestate`.
  - The Quake Live client does not waste time and resources loading the map, textures and shaders, remaining in the waiting phase.
  - A 5-second timer is maintained for safe regular termination of the session with the `disconnect "password protected server"` command.

## [1.0.47] - 2026-09-04
### Fixed and Improved
- **Fix for switching QuakeLive-VPN sub-tabs (Client / Server on router / Deploy to VPS)**:
  - **Fix critical JavaScript error (`SyntaxError: Identifier 'statusVal' has already been declared`)**:
    - In the `renderStatus()` method, the duplicate identifier `statusVal` has been eliminated (the variables `clientStatusVal` for client metrics and `srvStatusVal` for server metrics have been separated).
    - Previously, this syntax error caused the `qlvpn.js` file to crash on the browser side, resulting in the `QLVpn` object not being initialized and `QLVpn.switchSubTab(...)` switch handlers failing with the error `ReferenceError: QLVpn is not defined`.
  - **Global export `window.QLVpn`**:
    - Added explicit export of `window.QLVpn = QLVpn` to the global browser context for guaranteed accessibility from `app.js` and inline handlers `onclick`.

## [1.0.46] - 2026-09-04
### Added and Improved
- **Multi-line `CS_MESSAGE` banner (3 lines) on Quake Live loading screen**:
  - The message `CS_MESSAGE` (index 3) is structured in 3 lines via line feed `\n`:
    - Line 1: `^2[ONLINE] ^5SmartVPN Keenetic Server` (or `^3[PORT CONFLICT]...`).
    - Line 2: `^5Clients: ^3%d^7/^316 ^7| ^3UDP :%d ^7| ^2NetChan Camouflage`.
    - Line 3: `^3Status: ^2Protected ^7| ^5Uptime: ^3%s`.
- **Complete protocol research and shutdown timer after 5 seconds**:
  - The emulation protocol is stopped at the loading screen after sending gamestate (without world snapshots `svcSnapshot`).
  - Exactly 5 seconds later, the server sends the secure command `disconnect "password protected server"`, after which Quake Live returns to the main menu with a message about password protection.
- **Support for Quake Live Upstream Proxy Server**:
  - **Separation of VPN traffic and real game**:
    - Encrypted packets from VPN clients (`qlv1=` and authorized tunnels) are processed strictly locally on the router.
    - Packets from real Quake Live players (OOB probes `getstatus`, `connect`, as well as in-game NetChan packets) are transparently forwarded to the specified upstream server.
    - Response packets from the upstream server are broadcast back to the corresponding client.
  - **Management and persistence**:
    - Configuration in the SmartVPN web interface (card "Upstream Quake Live server (Upstream Proxy)").
    - API endpoint `POST /api/qlvpn/server/upstream` for dynamic updates without breaking VPN connections.
    - CLI flag `-upstream <host:port>` for `ql-vpn.exe`.
    - Automatic saving to `qlvpn-server.json` and restoration when restarting the service.
    - In the absence of an upstream server, local emulation mode works with a 3-line `CS_MESSAGE` and a 5-second shutdown.

## [1.0.45] - 2026-09-04
### Fixed and Improved
- **Fix Quake Live connection drop when going to `CA_PRIMED` (Fix stream cipher `NetchanEncode`)**:
  - **Failure diagnostics `CL_ParseServerMessage: Illegible server message -1`**:
    - Based on the system log of the Quake Live client (`baseq3/error.log`) and the disassembler `quakelive_steam.exe`, the exact cause of the disconnect is localized: when the card is loaded, the client sends a command to check packet checksums `cp 0 <checksums...>`.
    - In the id Tech 3 / Quake Live engine, the NetChan protocol uses a symmetric stream cipher, where the key `key = byte(challenge ^ seq)` dynamically mutates on each byte through `key ^= (s << (i & 1))` from the text of the last confirmed client command (`chan->lastClientCommand`).
    - The server `NetchanEncode` ignored `clientCommandString`, encrypting packets with a static key, which caused the client to decode the opcode bytes as noise and crash the session with `Illegible server message -1`.
  - **Implementation of authentic stream cipher `NetchanEncode`**:
    - `NetchanEncode` has been updated in strict accordance with the `quakelive_steam.exe` disassembler (address `0x004bcf44`), guaranteeing flawless mutual decryption of all keepalive and marquee packets.
  - **Quake Live memory limit protection `MAX_GAMESTATE_CHARS` (16 KB)**:
    - Sending the `CS_MESSAGE` ticker is blocked during the initial loading of the card by the client (`ReliableAcknowledge < 1`), preventing the accumulation of a command queue.
    - Ticker interval adjusted to 1000 ms (comfortable read speed without buffer overflow `cl.gameState.stringData`).

## [1.0.44] - 2026-09-04
### Added and Improved
- **Streaming ticker `CS_MESSAGE` and stopping the protocol on the loading screen stub**:
  - **Marquee Ticker**:
    - A smooth running line has been implemented on the loading screen of the Quake Live client ("Awaiting snapshot") with an update interval of 250 ms (4 characters/sec - a comfortable reading speed).
    - The `GenerateMarqueeSlice` algorithm tokenizes visible characters and preserves Quake color sequences (`^0`..`^9`) without tag breaking or flickering.
    - The full status is cyclically broadcast in the creeping line: `[ONLINE] SmartVPN Keenetic Server | Clients: 1/16 | UDP :27960 | Uptime: 05m:12s | NetChan Camouflage Active`.
  - **Protocol stub on the loading screen (“Awaiting snapshot”)**:
    - World snapshot transmission (`svcSnapshot`) has been disabled due to user request. The protocol keeps the client in the `GameClientPrimed` state on the loading screen with an active ticker.
    - Responses to client packets are transmitted via a lightweight keepalive with command confirmation.
  - **Reliable delivery of Protocol 91 server commands (`BuildReliableCommandsPacket`)**:
    - Implemented guaranteed delivery of server commands (`svcServerCommand`) with repeated sending of unconfirmed commands (`clientRelAck`), which eliminates the client error `Dropped a reliable command`.
  - **Eliminate Windows Firewall access prompt during tests (`ListenIP`)**:
    - In tests, the server binds exclusively to the local interface `127.0.0.1`, which completely prevents the Windows Defender Firewall dialog from appearing for `qlvpn.test`.

## [1.0.43] - 2026-09-04
### Added and Improved
- **Dynamic color server status and number of clients in `CS_MESSAGE`**:
  - The system configuration line `CS_MESSAGE` (index 3), displayed in the center of the map loading screen in the Quake Live client, integrates the server status with the official color marking id Tech 3 (`^1`..`^7`):
    - Server status: `^2[ONLINE]` (green) or `^3[CONFLICT]` (yellow for a backup port).
    - Branding: `^5SmartVPN Keenetic` (turquoise/white).
    - Number of active clients: `^5Clients: ^3%d^7/^316` (counting real connections and scoreboard).
    - Active UDP port and uptime: `^3UDP :%d ^7| ^5Up: ^3%s`.
  - Synchronized also with the welcome message `CS_MOTD` (index 4).

## [1.0.42] - 2026-09-04
### Improved and Unified
- **Complete redesign of the QuakeLive-VPN server card and interface panels**:
  - **Visual unification with SmartVPN style (Glassmorphism Dark UI)**:
    - All QuakeLive-VPN subtab containers have been converted to the standard `.card-panel` class with a translucent background, blur (`backdrop-filter: blur(12px)`), borders and shadows.
    - The `🎮 id Tech 3` (`badge-qlvpn`) brand badge has been added to the server card header, along with neat status, restart and update buttons.
  - **Metrics Grid**:
    - Added 4 parameter cards: **Server Status** (with accurate Uptime output), **UDP Port** (with conflict/backup port indication), **Online Players** (active scoreboard sessions) and **Tokens Issued**.
  - **Stylized block of connections and tips for the game console**:
    - The `#ql-server-port-alert` panel is designed as an accent glass banner with automatic detection of the connection host (LAN IP Keenetic / localhost) and a button for quickly copying the `connect <host>:<port>` command to the clipboard in 1 click.
  - **Server uptime tracking**:
    - The `Server` and `ManagerStatus` structures have been supplemented with recording of the startup time of `StartTime` and dynamic calculation of the continuous operation time of the `server_uptime` daemon.

## [1.0.41] - 2026-09-04
### Fixed and Improved
- **The key reason for the `Awaiting snapshot` freeze has been resolved (deciphering client commands and confirming `relAck`)**:
  - **Correct decryption of the client payload (`ParseClientPayload`)**:
    - In Quake Live Protocol 91 networking, clients send the header bytes `serverId`, `messageAcknowledge`, and `reliableAcknowledge` followed by 1 byte of flags/seeds (0x80/0x81).
    - Starting from byte 12 (`CL_ENCODE_START`), the packet is XOR-encrypted with the key `byte(challenge ^ serverId ^ messageAcknowledge)`, mutating on the characters of the confirmed reliable server command (`lastServerCommand = "priv 0"`).
    - Previously, the parser did not take into account XOR encryption from the 12th byte, did not read the additional byte of the Quake Live seed, and expected the command opcode `2` instead of `4` (`clc_clientCommand`). Because of this, the `userinfo` and `cp` (checkpoint) commands were discarded, and the `lastCmdSeq` number always remained zero.
  - **Timely confirmation of reliable client commands in snapshots (`relAck`)**:
    - The server now correctly reads the client's command number (`cmdSeq = 1` for `userinfo`, `cmdSeq = 2` for `cp`) and immediately confirms it in the `reliableAcknowledge` field of the world snapshot (`BuildSnapshotPacket`), allowing the client to instantly clear the queue of trusted commands and successfully transition from `CA_PRIMED` ("Awaiting snapshot") into the active phase of the game `CA_ACTIVE`.
  - **Pure XOR encryption of outgoing server packets (`NetchanEncode`)**:
    - According to analysis of a real server dump, outgoing Protocol 91 server datagrams are encrypted strictly with the static key `byte(challenge ^ outgoingSequence)` without modification by client command strings. The parasitic corruption of the key by the command line has been eliminated.
### Fixed and Improved
- **Fixed desynchronization of sequence numbers when loading a map**:
  - **Timely sending of the snapshot immediately after gamestate**:
    - The server now sends a world snapshot to `BuildSnapshotPacket` (`seq = 3`) immediately after transmitting all `svc_gamestate` fragments, just like in a real server dump.
  - **Blocking flood of sequence numbers during loading (GameClientPrimed)**:
    - Previously, the `gameClientSnapshotLoop` (20 Hz) worker continuously increased `OutgoingSeq` every 50 ms while the client was loading the card (taking ~2.8 seconds), which caused the sequence number to jump 60 packets ahead and the client to lose synchronization.
    - Background sending 20 Hz is transferred strictly to the `GameClientActive` state (after confirmation of loading and start of `clc_move`).

## [1.0.39] - 2026-09-04
### Fixed and Improved
- **Fixed the cause of `Awaiting snapshot` freezing based on analysis of real Quake Live network traffic**:
  - **Correct size and value `areamask` (`CL_ParseSnapshot`)**:
    - In Quake Live Protocol 91, the area visibility mask `areamask` is strictly 1 byte in size (`0xfd`), not 2 bytes. Passing length 2 caused the game engine to immediately reset the snapshot with an internal error `CL_ParseSnapshot: Invalid size 2 for areamask.`. Corrected to `len = 1, byte = 0xfd`.
  - **Authentic 541-bit snapshot of the player and entity state (`BaseSnapshotPayload`)**:
    - Replaced the 1141-bit snapshot with a bit-validated 541-bit snapshot (68 bytes) of the real Quake Live server with the correct `snapFlags = 7` flags (and `6` in the initial snapshot).
  - **Sending initial snapshot to Packet 1 (`BuildInitialPacket`)**:
    - As the capture of a real server showed, the very first confirmation packet `seq = 1` contains not only `svcServerCommand "priv 0"`, but also an immediate initial `svcSnapshot`, which prepares the client renderer even before the gamestate is transmitted.
  - **ConfigString 2 fix (`CS_MUSIC`)**:
    - Previously, configstring 2 passed the server version, which caused the error `cgame`: `^3WARNING: couldn't open music file SmartVPN-1.ogg`. CS 2 cleared (`""`) and map title moved to `CS_MESSAGE` (3).

## [1.0.38] - 2026-09-04
### Added and Improved
- **Indication of occupied ports and real port of the QuakeLive-VPN server**:
  - **Auto UDP port conflict detection**:
    - When you try to start a server on a busy port (for example, the standard `27960`, when Quake Live is already running on the machine), the system scans free ports (`27961`–`27970`) and switches to an available one without crashing.
    - The fields `RequestedPort`, `PortConflict` and `PortConflictReason` have been added to the structure `Server` and the status `ManagerStatus`.
  - **Visible warnings and prompts in all interfaces**:
    - A noticeable banner is displayed in the server console (`ql-vpn.exe` and `smart-vpn`) with an exact indication of the occupied port, the real listening port and the ready-made console command `connect 127.0.0.1:<port>`.
    - In the standalone Web UI (`:8092`) and SmartVPN web panel (`:8091`), the server status badges are colored amber warning with the prefix `⚠️ :<port>`, and a warning block with a connection command appears under the server title.
    - The Windows Tray tooltip displays the port conflict status and the actual port.

## [1.0.37] - 2026-09-04
### Fixed and Improved
- **Fixed Quake Live client hang at `Awaiting snapshot`**:
  - **Generating and sending authentic snapshots of the Protocol 91 world (`svcSnapshot = 7`)**:
    - Previously, after the map was successfully loaded and the client entered the `CA_PRIMED` state, the server sent empty heartbeat packets (`svcNop`), which caused the `cgamex86.dll` Quake Live module to continuously display *"Awaiting snapshot..."*.
    - The `BuildSnapshotPacket` function has been implemented with the generation of a base snapshot (`deltaNum = 0`, monotone `serverTime`, flags `snapFlags = 3`, area mask `areamask = 0xfe, 0xff`, full snapshot `playerstate` and terminator `packet entities`), recreated with bit-precision from a real Quake Live network exchange dump.
  - **Background loop for sending snapshots (20 Hz Snapshot Loop)**:
    - A background worker `gameClientSnapshotLoop` (20 Hz / 50 ms) has been added to `Server`, which guarantees continuous delivery of world state snapshots to all connected game clients, even if individual UDP packets are lost during map loading.
  - **Client transition to active state (`CA_ACTIVE`)**:
    - Upon receiving `svcSnapshot`, the Quake Live client clears the state of `cg.snap == NULL`, instantly hides the loading screen, and begins actively rendering the game frame on the `campgrounds` map, starting sending custom move commands (`clc_move`).

## [1.0.36] - 2026-09-04
### Fixed and Improved
- **Full support for handshake and gamestate protocol 91 Quake Live (Steam client)**:
  - **Fixed hang `Awaiting connection...`**:
    - Under the Quake Live protocol, the server must immediately send the first NetChan datagram (Packet 1, `seq = 1`, `svcServerCommand "priv 0"`, `svcEOF`) immediately after confirming `connectResponse`. The client enters the `CA_PRIMED` state and responds with an acknowledgment with `seq = 1`.
  - **Fixed bug `CL_ParseGamestate: bad command byte`**:
    - Encryption key mismatch `CL_Netchan_Decode` (`key := byte(challenge) ^ byte(seq)`) has been detected and corrected: the binary Steam auth ticket does not contain the `\challenge\<val>` text field. The server now securely stores the issued `challenge` on the client's IP/port when processing `getchallenge` and uses it when registering a session.
    - The authentic Protocol 91 scheme with the correct checksums of the files `pak00.pk3` (`363034675`) and `bin.pk3` (`2082278750`) has been implemented into the `svc_gamestate` stream, the server version `1069 linux-x64` and `checksumFeed = 0x00003600`.
  - **Support for large message fragmentation (`NETFLAG_FRAGMENT 0x80000000`)**:
    - Implemented correct splitting of long gamestate messages into MTU-safe fragments of 1300 bytes with offset and length headers.
  - **Fixed handling of buffer exhaustion in BitReader**:
    - Fixed `BitReader.ReadByte()` loop when reaching the end of the datagram.
  - **Removing port conflict in `cmd/ql-vpn`**:
    - `runServer` now launches a single server instance on a given port (27960) and passes it to the Web Admin/GUI manager without creating duplicate background processes on port 27961.

## [1.0.35] - 2026-09-04
### Fixed and Improved
- **Solution to `Awaiting connection...` problem when connecting Quake Live to `127.0.0.1:27960`**:
  - **Explicit IPv4 UDP socket binding (`udp4: 0.0.0.0:27960`) to `internal/qlvpn/server.go`**:
    - A fundamental feature of the Windows Winsock networking stack was discovered and fixed: when calling `net.ListenUDP("udp", ...)` from `nil` IP, Go created a socket `AF_INET6` (`[::]:27960`) by default. The Windows kernel was not delivering incoming IPv4 loopback UDP datagrams from the 32-bit Quake Live client (`quakelive_steam.exe`) to socket `AF_INET6`, causing the client to wait indefinitely for a response to `getchallenge` (`Awaiting connection...`).
    - The server is now guaranteed to open the main IPv4 socket `0.0.0.0:27960` (`udp4`), as well as the optional IPv6 socket (`udp6`), ensuring 100% compatibility with all types of clients and OS.
  - **Symmetric routing of responses to clients**:
    - All responses (`challengeResponse`, `connectResponse`, `svc_gamestate`, `svc_nop`, VPN tunnel packets) are sent strictly through the socket (`conn`) through which the client request came, excluding mismatches of sender addresses.
  - **Added REST API endpoint `/api/exit`**:
    - Allows you to correctly terminate the GUI/Web Control Center process via an HTTP request.

## [1.0.34] - 2026-09-04
### Fixed and Improved
- **Automatic start of the Quake Live virtual server (UDP 27960) at startup**:
  - **Server autostart "out of the box" in `internal/qlvpn/manager.go`**:
    - Fixed Quake Live client hanging at `Awaiting connection...` when connecting to `connect 127.0.0.1`.
    - Previously, if there was no server configuration file (`qlvpn-server.json`) and no saved tokens, the `shouldStart` flag remained `false`, causing UDP port 27960 to not open. Now the server starts automatically by default the first time the service starts on `DefaultPort` (27960).
    - The 1-second socket start delay has been eliminated: UDP socket binding is now instantaneous and synchronous when the manager is initialized.
  - **Reliable definition of the data directory (`data`) on Windows**:
    - Added automatic path resolution to the `data/` directory relative to the executable file (`os.Executable()`) in `NewManager` and `NewGUIState`, which eliminates the problem of creating configuration files when launched from shortcuts, other working folders or Explorer.
  - **Informative logging to the console and web interface**:
    - In GUI and Web modes, hints about the readiness of the virtual server for connection are displayed in the console and in the web panel log: `Quake Live Virtual Server listening on UDP :27960 (connect 127.0.0.1)`.

## [1.0.33] - 2026-09-04
### Added and Improved
- **Centralized system of bug reports and auto-diagnostics (integration with SmartUtils and snakelair/Keenetic)**:
  - **Backend using the Go standard library (`internal/api/bugreport.go`)**:
    - Autodiagnostics and system telemetry collection module: auto-detection of Keenetic router model (`/tmp/ndm/sysinfo`, `ndmq`, `summary.RouterModel`), Entware architecture (`mipsel-3.4`, `armv7-3.2`, `aarch64-3.10`, `x86_64`), Linux / KeeneticOS kernel version (`/proc/version`, `uname -sr`), RAM resources (`/proc/meminfo`) and disk partitions (`df -h`).
    - Ecosystem services status poll: `smart-vpn` (self), `sing-box` (PID, Clash API port 9090), `ql-vpn` (UDP 27960, server status), `smart-utils` (8090), `smart-route` (8088), `smart-photo` (8089), `crond`, as well as summaries of active KeeneticOS VPN connections (WireGuard / AWG / SSTP).
    - Poll OPKG repository configurations (`/opt/etc/opkg.conf`, `/opt/etc/opkg/*.conf`).
    - Smart multi-level log sanitization: collecting the last 40 lines from the circular memory buffer `logger.Get().GetHistory()`, log files or `logread` with strict masking of passwords, session tokens, hex hashes and WireGuard / AmneziaWG (Curve25519 Base64) private keys.
    - Automatic generation of pre-filled links for creating an Issue on GitHub (`snakelair/Keenetic/issues/new`), in the Telegram community and the Keenetic forum.
    - Registration of REST API endpoints: `POST/GET /api/doctor/bugreport` and `POST/GET /api/bugreport`.
  - **Web interface (Vanilla JS + Glassmorphism Dark UI)**:
    - Modal window `#modal-bug-report` with interactive chips for selecting projects (`smart-vpn`, `smart-route`, `smart-utils`, `smart-photo`, `keenetic-repo`) and types of requests (`bug`, `enhancement`, `question`).
    - Dynamic calculation and display of badges: router model, RAM volume and occupancy, number of active ecosystem services, number of log lines.
    - Automatic collection of autodiagnostics with debounce when entering the title and description of the problem.
    - Call button `🐞 Баг-репорт` in the panel header (`header-status`) and a community support card in the “Settings” section.
    - A button to quickly copy a formatted Markdown report to the clipboard and proceed to creating a GitHub Issue.
  - **Unit tests (`internal/api/bugreport_test.go`)**:
    - Testing the generation of Markdown report and GitHub Issue links (`TestGenerateBugReport`).
    - Testing sanitization of passwords, tokens, WireGuard PrivateKeys and PSKs (`TestSanitizeLogContent`).

## [1.0.32] - 2026-09-04
### Fixed and Optimized
- **Fix for Quake Live client freezing at `Awaiting connection...` stage and resetting after `FS_Startup`**:
  - **Disassembly and reverse engineering of processing `connectResponse` (`0x004bb540`) and `NET_CompareBaseAdr` (`0x004d6560`)**:
    - It has been discovered that the Quake Live client `quakelive_steam.exe` upon receiving `connectResponse` validates that the base network address `from` matches the destination address `clc.serverAddress`.
    - Fixed blocking of UDP port 27960 by a hung process, preventing delivery of response packets to `127.0.0.1`.
  - **Automatic installation of the `campgrounds` card for Quake Live (protocol 91)**:
    - It has been discovered that in the official `pak00.pk3` Quake Live archive the classic map `q3dm6` is missing and replaced with `maps/campgrounds.bsp`. Sending the `mapname\q3dm6` card to ConfigString 0 caused the client to crash immediately after `FS_Startup` (`Disconnected from server`).
    - `BuildGamestatePacket` implements automatic substitution of the `campgrounds` card for protocol >= 90.
  - **Reliable retransmission of the package `svc_gamestate`**:
    - Added re-sending of the initial `svc_gamestate` packet when receiving repeated client packets from `seq <= 1`, ensuring that the client enters the card loading status even with UDP network losses.
  - **Support for dynamic port 0 in `NewServer`**:
    - The server now supports `port = 0` to automatically assign a dynamic OS UDP port, eliminating port conflicts during local debugging and testing.
  - **End-to-end integration test `TestFullQuakeLiveClientFlow`**:
    - Added a full test to `gamestate_test.go`, emulating the behavior of the Quake Live Steam client from `getchallenge` to loading the map and commands `new` in 0.08 s.

### Fixed and Optimized
- **Fixing the `CL_ParseGamestate: bad command byte` error in the Steam Quake Live client**:
  - **Disassembly and precise reverse engineering `quakelive_steam.exe`**:
    - An exact command read cycle of packet `svc_gamestate` at address `0x004bd790` was detected, allowing only opcodes `svc_configstring (3)`, `svc_baseline (4)` and terminating `svc_EOF (8)`.
    - The function `CL_Netchan_Decode` was found at the address `0x004bcef0`, unmasking the stream starting from byte 8 using a line from the circular buffer of reliable commands `clc.reliableCommands[reliableAcknowledge & 63]`.
  - **Fix `reliableAcknowledge` in server packages (`svc_gamestate` and `keepalive`)**:
    - Fixed a critical error sending `client.IncomingSeq` (1) in the `reliableAcknowledge` field. At startup, the client had not yet sent reliable commands (`reliableSequence = 0`), so accessing at index 1 resulted in reading an uninitialized string and corrupting the Huffman decryption keys for all subsequent bytes.
    - Introduced strict tracking of `ReliableAcknowledge` and `LastClientCommand` in the client session, equal to 0 at the time of connection and updated only when `clc_clientCommand` is received from the client.
  - **Deterministic sorting ConfigStrings**:
    - No random iteration of the Go dictionary when generating a package: configuration lines are passed strictly sorted by indexes (`CS_SERVERINFO`, `CS_SYSTEMINFO`, `CS_GAMEVERSION`, `CS_LEVELSTARTTIME`, `CS_MOTD`, `CS_WARMUP`, `CS_SCORES1`, `CS_SCORES2`, `CS_PLAYERS`).
  - **Quake Live official Huffman frequency table integration**:
    - The authentic 256-element frequency table `msg_hData` from the `.rdata` section of the `quakelive_steam.exe` (`0x00542790`) binary has been checked and confirmed.

## [1.0.30] - 2026-09-04
### Fixed and Optimized
- **Fixing the `CL_ParseServerMessage: Illegible server message 123` error in the Quake Live client**:
  - **Fix masking of `SV_Netchan_Encode` and `CL_Netchan_Decode`** packets:
    - In the id Tech 3/Quake Live network protocol, the client automatically unmasks incoming packets by XORing starting byte 8 (payload byte 4) using the `key = byte(challenge ^ outgoingSequence)` key.
    - The `NetchanEncode` function has been implemented, which correctly applies the original Tech 3 id masking before sending the `svc_gamestate` and `svc_nop/keepalive` packets.
  - **Recovery of 4-byte NetChan header format**:
    - Fixed the erroneous addition of 4 bytes `NETCHAN_GENCHECKSUM` to the stream for Quake Live (this field is used exclusively in the ioquake3 fork, and in the original id Software Quake Live client the header always consists of strictly 4 bytes `OutgoingSequence`).
    - Fixed payload offset causing Huffman stream desynchronization.
  - **Huffman reference frequency table correction `msgHData`**:
    - Corrected frequency weights of characters from index 99 (`'c'`) to 255 in `internal/qlvpn/huffman.go`, completely synchronizing the table with the official `code/qcommon/msg.c` id Tech 3 code.
  - **Correct 6-byte parsing of client NetChan packets**:
    - The client packet header is fixed at 6 bytes (`OutgoingSequence` [4 bytes] + `qport` [2 bytes]) followed by payload unmasking using the formula `challenge ^ serverId ^ messageAcknowledge`.

## [1.0.29] - 2026-09-04
### Fixed and Optimized
- **Correct encoding and line endings in all Windows batch files (`.bat` / `.cmd`)**:
  - All batch files (`build.bat`, `build_all.bat`, `deploy_to_router.bat`, `git_menu.bat`, `git_status.bat`, `.deploy_profile.cmd`) are brought to the strict standard **CRLF (`\r\n`)** and **UTF-8 without BOM**.
  - A critical parser error `cmd.exe` has been fixed, which caused a shift in the line reading pointer for Unix LF endings (errors `'hcp'`, `'tlocal'`, `'tle'`, `'cho'`, `'EM'`).
  - Fixed the output of `->` stream redirection symbols in `echo` commands, causing the file `Building` to be accidentally created.
  - Added `.gitattributes` file with `eol=crlf` rule for all `*.bat` and `*.cmd`, preventing accidental conversion of strings to LF during commits and cloning.
  - Support for non-interactive launch of `build.bat 1` and `build_all.bat 1` without blocking pauses in automatic build scripts.

## [1.0.28] - 2026-09-04
### Added and Improved
- **Level 1: Quake Live / Quake 3 Virtual Server (connect and download map)**:
  - **Native implementation of the id Tech 3 network protocol in pure Go**:
    - Adaptive Huffman Coding (Sayood Adaptive Huffman Coding) with original frequency table `msgHData` id Tech 3 (256 characters) without third-party C/C++ dependencies.
    - Bit-stream reader (`BitReader`) and writer (`BitWriter`) with support for little-endian bit packing.
  - **Authentic multi-stage NetChan network protocol**:
    - Correct processing of `getchallenge <protocol> <clientChallenge>` with return of `challengeResponse <serverChallenge> <clientChallenge>`.
    - Retrieving and echoing `challenge` into the OOB package `connectResponse <challenge>`, allowing the actual Quake Live client to successfully complete the handshake phase and proceed to load.
    - Implementation of UDP anti-spoofing protection `NETCHAN_GENCHECKSUM(challenge, sequence)` for protocols 71, 90 and 91 (Quake Live and modern ioquake3) with backward compatibility with protocol 68 (Quake 3 1.32).
  - **Gamestate Packet Generator (`svc_gamestate`)**:
    - Full broadcast of the game structure (`CS_SERVERINFO`, `CS_SYSTEMINFO`, `CS_PLAYERS`, `CS_MOTD`, `CS_WARMUP`) with automatic selection of standard maps (`campgrounds` for Quake Live, `q3dm6` for Quake 3).
    - Cleaning up strict packet inspection (`sv_pure 0`), ensuring instant loading of local resources by the player without the need to download PK3 archives from the router.
  - **Synchronization and session retention (Keepalive / Heartbeat)**:
    - Exchange of confirmation packets (`svcNop` + `svcEOF`) and parsing of client commands (`donedl`, `cp`, `disconnect`).
    - Real connected players are automatically displayed in the router's score table and built-in web interface with live ping and points.
  - **Multiplexing on one UDP port `:27960`**:
    - Simultaneous operation of an encrypted VPN tunnel (ChaCha20-Poly1305 / AES-128-GCM) and the Quake Live virtual game server without mutual interference.

## [1.0.27] - 2026-09-04
### Added and Improved
- **Single universal executable for all platforms (Windows, Linux, macOS, MIPS, ARM)**:
  - Each binary includes a full **Client**, **Server** and **Remote Setup via SSH**.
  - The web interface of the standalone client `ql-vpn` is completely identical to the QuakeLive-VPN tab in the Keenetic Control Center (3 subtabs: Client, Server, Deploy to VPS via SSH).
  - In the remote SSH configurer, the ability to select the default port for the web administration interface has been added (default is 8091).
- **Integration with the shared repository `snakelair/Keenetic`**:
  - Publishing compiled OPKG packages `.ipk` for all router architectures (MIPS, MIPSLE, ARMv7, AArch64, x86_64) with careful preservation of packages `smart-photo`, `smart-route` and `smart-utils`.
  - Installation via SSH script with port selection support, similar to SmartUtils.
  - Deployment of binaries to remote Linux VPS via a common repository `snakelair/Keenetic`.
- **Quake Live Icon**:
  - Using the Quake Live reference logo (red circle, white ring, dagger and open crescent) in the Windows tray, navigation tab and main banner.

## [1.2.17] - 2026-09-04
### Added and Improved
- **QuakeLive-VPN server stealth and listing protection**:
  - **Exception from global server lists**: the QL-VPN server completely ignores requests `getservers`, `getserversExt`, `heartbeat` and declares flags `\sv_hidden\1`, `\hidden\1`, `\sv_master1\`, `\sv_master2\`, preventing indexing by TSPU scanners and gaming browsers.
  - **Excluding the local server from the client list**: the router’s own server is no longer included in the list of saved client servers on the router; the client list is split and displays only remote connections.
- **Smart creation of client/player tokens**:
  - **Auto-substitution of player names**: automatic selection of the first free classic Quake character (`Sarge`, `Ranger`, `Visor`, `Doom`, `Crash`, `Major`, `Keel`...) when creating tokens.
  - **Auto-detection of external WAN IP router**: the service automatically detects the real white IP of the router via `POST /api/diagnostics/external-ip` and substitutes `${WAN_IP}:27960` in the server address field with the ability to manually update using the “🌐 Determine WAN IP” button.
  - **Editable connection address (Preset)**: the server address in the token is now only a preset - the client (both in the Windows GUI and on the router) can freely specify any other external IP or DDNS domain immediately before connecting.
- **Quake Live Branding (Red Icon)**:
  - **Dynamic Windows system tray icon**: pure Go generation of a red Quake Live chevron (`#dc2626`) with a white gothic "Q" symbol and a dagger via Win32 `CreateIconFromResourceEx`.
  - **Router Vector Icon**: Replaces the 🎮 emoji on the navigation tab and router banner with Quake Live's signature red vector logo.
### Fixed and Optimized
- **Eliminating freezes and stutters in the Windows client (`ql-vpn`)**:
  - **Non-blocking connection**: the `/api/connect` method has been switched to completely asynchronous mode - an instant HTTP response to the client without blocking the interface for the duration of the UDP network handshake (up to 6 seconds).
  - **Process indicator and protection against spam clicks**: the active connection button goes into the `⏳ Подключение...` state with an animated spinner, the remaining buttons are blocked for the duration of the connection.
  - **Eliminate DOM reset every 1.5 seconds**: The server list caches the state hash and is redrawn only on actual changes (adding, deleting, changing status), eliminating focus loss and jittery hover effects.
  - **CSS rendering optimization**: replacing the heavy `backdrop-filter: blur(10px)` with a clean and fast dark background `#121826`, guaranteeing 60 FPS rendering without GPU/CPU micro-stutters.
  - **Win32 Tray Thread Safety**: Moved `SetStatus` calls and context menu actions to non-blocking goroutines, eliminating the deadlock of the Explorer window message thread.
- **Reliability of the QuakeLive-VPN server on the router**:
  - **Persistent saving of server state (`qlvpn-server.json`)**: The QL-VPN server saves the activity flag and automatically starts on the UDP port `:27960` when the router is rebooted or the `smart-vpn` service is restarted.
  - **Informative network handshake timeouts**: detailed messages in the event log when a UDP port is unavailable or the server is disconnected.

## [1.2.15] - 2026-09-04
### Improved
- **Cleaning up QuakeLive-VPN header design**:
  - Removed the `.ql-title-frame` visual frame around the protocol name `QuakeLive-VPN` and the masking tag `id Tech 3 NetChan Camouflage`.
  - Header elements are harmoniously integrated into a single line of the main tab banner without redundant internal borders.

## [1.2.14] - 2026-09-04
### Added
- **Full-fledged QuakeLive-VPN Windows client with tray and event log**:
  - **Without a console window (Silent GUI Launch)**: building with the `-H=windowsgui` subsystem flag prevents the command line window from opening when launched by the client. When called from a terminal, `AttachConsole` is used to support CLI commands.
  - **Windows System Tray icon**: bright system shield icon (`IDI_SHIELD`), right-click context menu (open control panel, quick tunnel switch, exit) and automatic recovery when restarting Explorer (`TaskbarCreated`).
  - **Live Event Log**: built-in event terminal in the web interface (`127.0.0.1:8092`) with auto-scrolling, color differentiation of events and detailed logging of each handshake step.
  - **Automatic normalization of the server address**: the error with the lack of a port when connecting using a token (`missing port in address`) has been fixed; port `:27960` is substituted automatically when generating, importing and establishing a connection.
  - **Secure asynchronous connection model**: elimination of mutex locks during network requests, independent mutex for the circular log buffer, guaranteeing instant status return.

## [1.2.13] - 2026-09-04
### Improved
- **Redesign of the main information banner of QuakeLive-VPN**:
  - Complete redesign of the banner into the `.qlvpn-banner` component according to the high standards of SmartUtils and the catalog style.
  - Neon accent stripe on the left, deep gradient Glassmorphism background with soft shadow.
  - Monolithic name frame with nickname, masking tag and port badge `UDP :27960`.
  - A neat right block with mini-cards of protocol characteristics (Port `27960`, Code `X25519`) and an update button.

## [1.2.12] - 2026-09-04
### Improved
- **Unification of QuakeLive-VPN sub-tabs style**:
  - The sub-tabs “👤 QL-VPN Client”, “🛡️ Server on router” and “🚀 Deploy to VPS via SSH” have been transferred to a single `subtab-btn` style (similar to the “Native VPN” tab).
  - Added dynamic status badges with color indication: `В сети` / `Откл` for the client and `:27960` / `Стоп` for the server.
  - The subtab panel is designed using `.native-subtabs-bar` with a quick refresh button on the right.

## [1.2.11] - 2026-09-04
### Improved
- **Styling the QuakeLive-VPN tab**:
  - Added a stylish neon frame `.ql-title-frame` around the header `QuakeLive-VPN [id Tech 3 NetChan Camouflage]` with Glassmorphism effect, accent glow and monospace masking tag.

## [1.2.10] - 2026-09-04
### Corrected
- **Fix for creating QuakeLive-VPN TUN interface on MIPSLE (Keenetic)**:
  - Error `failed to create server TUN: ioctl TUNSETIFF failed: file descriptor in bad state (EBADFD)` has been fixed.
  - Replacing the hard-coded `0x400454ca` value with the native `syscall.TUNSETIFF`: In MIPS architecture, the ioctl direction bit `_IOC_WRITE` is different from x86/ARM, causing the system call on MIPS to expect the command code `0x800454ca`.
  - Added reliable configuration of the TUN network interface through the search for utilities `ip` and `ifconfig` along the paths `/opt/sbin`, `/sbin`, `/usr/sbin` with preliminary raising of the link (`ip link set up`) and setting the MTU before assignment IP addresses.

## [1.2.9] - 2026-09-04
### Added
- **Full integration of QuakeLive-VPN (QL-VPN) into the SmartVPN control panel**:
  - **Dedicated management tab “QuakeLive-VPN”**:
    - Integration into the general top menu with the display of the `:27960` port in the badge.
    - Support for three modes in sub-tabs: “👤 Client”, “🛡️ Server on router” and “🚀 Deploy to VPS via SSH”.
  - **QL-VPN Client Mode**:
    - Fast connection via token `qlvpn://...` or `Bearer ...`.
    - Real-time tunnel status cards: status, server address, player name, IP and ping (RTT) by sequence ACK.
    - List of saved servers with quick one-click connection and token copying.
    - Configuring split routing (Split Tunneling): all traffic (`0.0.0.0/0`) or selected subnets.
  - **Server mode on the router**:
    - Starting and stopping the Quake Live game server on port 27960 UDP.
    - Interactive live Scoreboard of active players: name, frags, latency (ping), dedicated IP in the tunnel.
    - Built-in Bearer token generator for new players/clients with saving in `qlvpn-tokens.json`.
    - Table of issued tokens with the ability to copy and delete.
  - **Automatic 1-Click deployment to remote VPS via SSH**:
    - Connecting from a router to a remote Linux VPS (Ubuntu/Debian) via SSH with a password or SSH key.
    - Live installation log streaming (live terminal).
    - Automatic configuration of IPv4 forwarding, `iptables` NAT Masquerade rules, systemd service `ql-vpn.service` and player token generation.
    - Automatic import of the created token into the list of router servers and an immediate connection button.
  - **Standalone client for Windows with tray**:
    - Native Win32 tray (CGO-free) with context menu.
    - Local web interface (`127.0.0.1:8092`) for managing tokens and routing.

## [1.2.8] - 2026-09-04
### Added
- **Development of our own VPN protocol “QuakeLive-VPN” (QL-VPN)**:
  - **Full disguise as network traffic of the game Quake Live / id Tech 3**:
    - Using a standard dedicated UDP port `27960 UDP` (priority gaming traffic, no blocking by providers).
    - Quake Live 11-byte header emulation `Netchan` (`OutgoingSequence`, `qport`, `IncomingSequence`, `Opcode`).
    - Masking opcodes under commands `clc_move` (0x02), `clc_clientCommand` (0x03) on the client side and `svc_snapshot` (0x07), `svc_gamestate` (0x04) on the server side.
    - Dynamic padding to eliminate entropy and statistical signatures of packet lengths.
    - Imitation of tickrate (Keepalive usercmd ticks) during idle time to maintain NAT translations without signs of a tunnel.
  - **Active Probe Defense**:
    - The server automatically recognizes OOB scanner packets (`getstatus`, `getinfo`, `getchallenge`) and responds with genuine Quake Live server statuses (`q3dm6` map, server name, player list, ping).
    - Censors and DPI bots see the server as a regular dedicated game server.
  - **Hardware optimization for Keenetic chips**:
    - Auto-negotiation of encryption algorithms for processor architecture:
      - MediaTek MT7621 (MIPSLE softfloat) - **ChaCha20-Poly1305** (fast integer operations, kernel offload via Fastpath/conntrack).
      - MediaTek Filogic / Cortex-A53 (ARM64) - **AES-128-GCM** with ARM Crypto Extensions (ARM-CE) hardware instructions for speeds > 1.8 Gbps at < 5% CPU load.
  - **Cryptographic stack (Zero External Dependencies)**:
    - Curve25519 (X25519) ECDH key exchange via `crypto/ecdh`.
    - HKDF-SHA256 session key derivation and HMAC authentication with Pre-Shared Key (PSK).
    - Protection against replay attacks (Anti-Replay) through a 128-bit sliding window (Sliding Window Bitmap).
  - **Client and Server**:
    - Subsystem `internal/qlvpn/` with direct support for Linux `/dev/net/tun` (`IFF_TUN | IFF_NO_PI`).
    - Console utility `cmd/ql-vpn/` (`-server`, `-client`, `-keygen`, `-probe-test`).

## [1.2.7] - 2026-09-04
### Added
- **Sing-Box core CPU monitoring and automatic router overload protection (Watchdog Guard)**:
  - **Highly accurate real-time CPU load monitoring**:
    - The background supervisor reads the delta of user and system time ticks (`utime` + `stime`) from `/proc/<pid>/stat` and the total sum of router ticks from `/proc/stat` every second.
    - Exact calculation of the percentage of router processor load by processor `sing-box` (from 0.0% to 100.0%).
    - “CPU Load” card in the header of the Sing-Box panel with color indication (green / yellow / red) and supervisor status.
  - **Adjustable overload watchdog (Watchdog Guard)**:
    - Automatically prevents Keenetic router from freezing, Wi-Fi failures and routing crashes due to endless loops or network flooding.
    - Adjustable processor load threshold: from 50% (load of 1 core) to 100% (complete overload of the router), default 95%.
    - Configurable continuous overload interval: 15s, 30s, 60s (default), 120s, 300s. Short-term peaks (such as speed tests) are correctly ignored.
    - Selection of action in case of emergency: automatic restart (`restart`) or protective shutdown (`stop`).
    - Saving parameters to the permanent configuration `config.json` (`singbox_watchdog`).
    - New tab “🛡️ CPU Protection (Watchdog)” with a live status indicator, overload seconds counter and control form.
    - Recording protection trigger events in the system log and daemon log buffer.

## [1.2.6] - 2026-09-04
### Added
- **Sing-Box Extension: ShadowTLS (v3) and TLS Masking Preset Library**:
  - **ShadowTLS (v3) protocol support**:
    - Integration of outgoing nodes of type `shadowtls` with version v3, password protected and TLS socket.
    - Support for importing links like `shadowtls://password@host:port?sni=...&version=3#Name`.
    - Adding ShadowTLS to the Sing-Box visual node builder.
  - **Library of SNI masking presets for popular domains**:
    - Curated directory of verified masking domains for VLESS Reality and ShadowTLS:
      - 🍏 **Apple**: `gateway.icloud.com`, `swdist.apple.com` (uTLS: `ios`, `safari`)
      - 🪟 **Microsoft**: `www.microsoft.com`, `update.microsoft.com` (uTLS: `chrome`)
      - ☁️ **Cloudflare**: `www.cloudflare.com`, `speed.cloudflare.com`, `www.speedtest.net`
      - 🔍 **Google**: `dl.google.com`, `fonts.googleapis.com`
      - 📱 **Samsung / NVIDIA**: `samsung.com`, `images.nvidia.com`
      - 🇷🇺 **White list of the Russian Federation**: `yandex.ru`, `vk.com`, `gosuslugi.ru`, `ozon.ru`
    - Interactive preset chips in the modal window for adding nodes with auto-substitution of SNI and uTLS.
  - **Live TLS handshake check from a router (SNI Probe)**:
    - Endpoint `POST /api/singbox/test-sni` to check the availability of the selected masking domain directly from Keenetic via TLS 1.3 / ALPN `h2`.
    - Measuring the delay (ping ms) of a handshake, checking the protocol version and certificate issuer.
    - Button “⚡ Check SNI” in the form for adding a node and a list with testing in Visual Config.
  - **Link to the Customer Catalog**:
    - ShadowTLS and Xray-core/VLESS Reality cards in the Catalog are marked with the status `⚡ В ядре Sing-Box` with a button to quickly go to configuration.

## [1.2.5] - 2026-09-04
### Added
- **Interactive catalog of VPN / Anti-DPI clients and protocols (Roadmap)**:
  - A new tab “Client Catalog” has been added with the “Plan (12)” badge for clients and utilities that are not included in the standard KeeneticOS firmware.
  - **5 customer categories**:
    1. 🛡️ **DPI protection and traffic masking**: ShadowTLS (v3), Cloak (ck-client), TUIC (v5), Xray-core (VLESS Reality / Vision).
    2. 🌐 **Mesh-nets and P2P-tunnels**: Tailscale (WireGuard Mesh / DERP / Exit Node), Nebula (P2P overlay from Slack Technologies).
    3. ⚡ **Local DPI bypass without VPN and VPS**: Zapret (NFQWS / TPWS from bol-van to unblock YouTube and Discord without losing speed), ByeDPI (ciadpi from hufrea, lightweight C-proxy with < 3 MB RAM consumption).
    4. 🧅 **Anonymous and distributed networks**: Tor with hidden bridges Snowflake and Meek (WebRTC disguise), I2P (i2pd daemon in C++).
    5. 🏢 **Corporate SSL-VPN**: AnyConnect / OpenConnect (Cisco AnyConnect, Fortinet, GlobalProtect client), SoftEther VPN Client (multi-threaded L2 HTTPS tunnel).
  - For each client the following are given:
    - Operating principle and architectural purpose.
    - Justification for the absence of KeeneticOS in the standard firmware.
    - Key advantages and features.
    - Technical requirements: RAM consumption, CPU load, supported architectures (MIPS, ARM, MIPSLE) and binaries.
    - Status: “⏳ In terms of development” (Roadmap v1.3).
  - Interactive filters by category with counters.
  - Quickly search for clients by name, protocol and functionality.
  - Modal window with a detailed plan for integration into the Keenetic router stack.
  - Information banner in the “Other VPNs” section for quick access to the directory.

## [1.2.4] - 2026-09-04
### Added
- **Full integration of the Sing-Box core inside SmartVPN**:
  - **Automatic downloader of official releases**:
    - Intelligent determination of the router processor architecture (`mipsle-softfloat`, `armv7`, `arm64`, `amd64`).
    - Downloading pre-built binaries directly from official releases `SagerNet/sing-box` on GitHub.
    - Built-in streaming unpacking of archives `.tar.gz` using Go without the need for external utilities.
    - Installing the executable file to `/opt/etc/smart-vpn/bin/sing-box`.
  - **Process life cycle management**:
    - Start, stop, restart the daemon process running SmartVPN.
    - Monitoring PID, exact operating time (Uptime) and real memory consumption (RSS) from `/proc/<pid>/statm`.
    - Ring log buffer (500 lines) and live viewing of kernel logs in the web interface.
  - **Sing-Box Configurator**:
    - **Visual designer**: setting up a transparent TUN interface (`singbox-tun`), mixed SOCKS5/HTTP proxy port (`mixed-in`, 10808), Clash API port (9090) and smart traffic routing rules (ad blocking, direct access to Russian subnets and local network).
    - **Raw JSON editor**: JSON formatting, automatic syntax validation by the `sing-box check` utility before running/saving and quick reset to a proven template.
  - **Managing outgoing proxy nodes (Outbounds)**:
    - Support for modern protocols: VLESS Reality (XTLS Vision + uTLS), Shadowsocks, Trojan, Hysteria2.
    - Quick import of nodes from links (`vless://`, `ss://`, `trojan://`) with automatic addition to the selector.
    - Integration with the Clash API controller (`127.0.0.1:9090`) to instantly switch the active node without restarting the process.
    - Live testing of network latency (Ping/Delay) to each proxy node.
  - **Summary Dashboard**:
    - Displaying the Sing-Box card on the main dashboard next to native WireGuard/AmneziaWG and SSTP tunnels.
    - Lists active outgoing channels with protocol badges, network latency and active node switch.

## [1.2.3] - 2026-09-04
### Added and improved
- **Automatic recognition of AmneziaWG (AWG 2.0 / 3.0)**:
  - Intelligent scanning and comparison of native Keenetic router interfaces with Entware AmneziaWG configurations (`/opt/etc/awg-manager/tunnels/*.json`, `/opt/etc/awg-manager/*.conf`, `/opt/etc/amnezia/*.conf`).
  - Match by native interface index (`nwgIndex`), by matching the calculated public key Curve25519 (`DeriveWGPublicKey`), by peer name or endpoint.
  - Enrichment of the interface with hidden parameters: restoration of the private key (`PrivateKey`), keys for preliminary agreement of peers (`PresharedKey`), DNS and obfuscation parameters.
- **Indication of AmneziaWG in the web interface**:
  - VPN cards and the WireGuard table now display a separate purple `🛡️ AmneziaWG` badge instead of the usual "WireGuard".
  - The modal editor window displays the `🛡️ AmneziaWG` badge in the window title.
- **AmnesiaWG Editor**:
  - When AmneziaWG tunnels are opened, the cloaking switch is turned on automatically.
  - Masking fields (`Jc`, `Jmin`, `Jmax`, `S1`–`S4`, `H1`–`H4`, `I1`) are automatically filled in with valid configuration values.
  - Two-way synchronization of configuration updates with `awg-manager` files.

## [1.2.2] - 2026-09-04
### Corrected
- **WireGuard Configuration Editor**:
  - Fixed the false "Masking Disabled" pop-up notification every time you open the WireGuard Interface Editor.
  - Initialization and reset of the editor form has been switched to silent mode (`silent: true`).
  - Notifications about switching presets are now displayed only when the user explicitly clicks on the corresponding buttons.

## [1.2.1] - 2026-09-04
### Interface optimization and acceleration
- **Background loading and caching of VPN connections**:
  - Interface blocking has been removed: polling of the NDM system daemon has been moved to a non-blocking background worker without holding the global manager mutex.
  - Caching heavy router configuration (`show running-config`) with a TTL of 60 seconds. Polling of tunnel statuses has accelerated from 4–5 seconds to ~150 ms.
  - Serialization of CLI command calls to resolve NDM kernel socket lock conflicts.
  - Instant rendering of the dashboard and connection cards from the local cache `localStorage` (0 ms delay when loading the page, the spinner no longer hangs).
- **Reactive update when active**:
  - Tracks user activity (return to tab, window focus, clicks/keystrokes) with automatic silent data updating in the background.
  - Instant optimistic response of tunnel switches (On/Off) without waiting for a response from the router.
  - Instant delivery of state changes via WebSocket broadcast without interface flickering.

## [1.2.0] - 2026-09-03
### Added
- **Definition of WireGuard versions and stack**:
  - Detection of CLI utilities: standard `wireguard-tools` and extended `amneziawg-tools`.
  - Monitoring the loading of Linux kernel modules: `wireguard.ko` and `amneziawg.ko`.
  - Information banner in the editor with a report on support for hardware traffic masking.
- **The most comprehensive WireGuard parameters**:
  - Advanced network settings: FwMark, routing table (Table), MTU with quick presets (1280, 1360, 1420), DNS servers.
  - Support for hooks and launch scripts: `PreUp`, `PostUp`, `PreDown`, `PostDown`.
  - Preshared Key (PSK) management with the ability to automatically generate 32-byte keys.
  - Quick selection of allowed subnets (Allowed IPs) and keepalive intervals.
- **Traffic masking parameters (AmneziaWG / Anti-DPI / Bypassing TSPU blocking)**:
  - Full support for obfuscation parameters: `Jc` (garbage bags), `Jmin`/`Jmax` (garbage size range), `S1`/`S2`/`S3`/`S4` (garbage sizes packet prefixes), `H1`/`H2`/`H3`/`H4` (magic handshake and data headers), `I1` (custom payload simulation).
  - 1-click camouflage presets: “Basic camouflage”, “Anti-TSPU / Advanced”, “Reset camouflage”.
  - Function for generating random masking parameters (Randomize Anti-DPI) to protect against signature analysis.
  - Two-way synchronization of all parameters between visual form and text `.conf`.
  - Template `AmneziaWG (с маскировкой)`.

## [1.1.0] - 2026-09-03
### Added
- **Comprehensive availability check (Ping + HTTP)**:
  - ICMP Ping checking is supplemented by monitoring HTTP responses through sets of popular servers: Global (Google, Cloudflare, Microsoft, Apple), Russian (Yandex, VK, Mail.ru) and IT/Dev (GitHub, Telegram, Wikipedia).
  - A quick "Ping + HTTP" check has been added to each VPN connection card.
- **Full WireGuard configuration editor**:
  - Two-mode editor: visual form (address, port, MTU, DNS, key pair generator) and text editor with standard syntax `.conf`.
  - Manage the list of peers (adding, deleting, Keepalive, AllowedIPs, Endpoint).
  - Ready-made configuration templates (Cloudflare WARP, VPS server).
  - Export configuration to `.conf` and delete interface directly from the interface.
- **Real time network activity graphs (UL/DL)**:
  - High-performance Canvas graph of incoming (DL) and outgoing (UL) traffic on the main page.
  - Dynamic grid with auto-scaling speed units (KB/s, MB/s).
  - Display of current and peak transmission rates, range switching 1 min / 3 min.
- The default web interface port has been changed to **8091**.

## [1.0.0] - 2026-09-03
### Added
- The first official release of SmartVPN for Keenetic (Entware) routers.
- Main dashboard summary (Summary):
  - Metrics for active, disconnected and failed VPN connections.
  - Live monitoring of the speed of incoming and outgoing traffic (RX/TX).
  - Tunnel cards with quick control On/Off in 1 click.
  - Monitoring router processor load, RAM and operating time.
- Section of native WireGuard connections:
  - View peers, AllowedIPs, traffic, and last Handshake time with color-coded activity indicators.
  - Import WireGuard configurations (`.conf` files) with automatic generation of KeenOS NDM commands.
- Section of native Keenetic SSTP connections:
  - Monitor servers, accounts, encryption and connection status.
- Other native VPN connections section:
  - Supports OpenVPN, IPsec/IKEv2, L2TP and PPTP.
- Sing-Box Section:
  - Information panel and binary detection `/opt/bin/sing-box` (development of active logic is planned for the next stage).
- Network diagnostic tools:
  - Ping any node through the selected VPN interface.
  - Determining the external IP address and geolocation through the tunnel.
  - DNS resolution speed test.
- Event and log log:
  - Real-time WebSocket streaming.
  - Level filters (INFO, WARN, ERROR) and downloading logs.
- Self-updating and checking system for new versions.
- Automatic emulation mode (Mock Mode) for local development and testing on PC/Windows.
