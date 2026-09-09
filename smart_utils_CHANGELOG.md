# 📦 Smart-Utils Changelog

All important changes to the Smart-Utils project are documented in this file.

## [1.0.29] - 2026-09-03

### A full-fledged module for managing the Cron task scheduler
- **Managing the scheduler service (Crond)**:
  - Real-time monitoring of `crond` service status, displaying PID and schedule file path.
  - Daemon control buttons: “Start”, “Stop”, “Restart”.
  - Automatic initialization of the `/opt/var/spool/cron/crontabs` environment and start script upon first launch.
- **Visual list and task cards**:
  - Toggle switches for instantly enabling and disabling tasks (commenting/uncommenting the line `#`).
  - Human-readable translation of the schedule into Russian (*“Every 5 minutes.”*, *“Every day at 04:00”*, *“On weekdays”*, *“At every boot of the router (@reboot)”*).
  - Quickly copy a command to the clipboard.
- **Interactive schedule designer and templates (Presets)**:
  - Quickly select frequency (every minute, every 5/15/30 minutes, every hour, daily, weekly, monthly, @reboot or custom expression).
  - Catalog of ready-made system templates for Keenetic (cleaning `/tmp`, backup settings, NTP time synchronization, updating Smart-Route lists, checking OPKG, watchdog, scheduled reboot).
- **Test run of the command (▶ Test)**:
  - The ability to instantly run a command for any task directly from the web panel and view the console output, stdout/stderr, return code and execution time.
- **Crontab Raw Editor**:
  - Tab for direct editing of the `crontab` file with syntax tips and validation.

## [1.0.28] - 2026-09-03


### Interactive installer and API validation
- **Interactive port selection**:
  - The `install.sh` installer requests the desired web interface port (default `8090`), checking the previous router settings.
  - The port setting is automatically saved in the service configuration file.
- **Checking real API response and synchronous restart**:
  - The installer synchronously restarts the service and polls `/api/status`, confirming the readiness of the web panel and displaying the exact version and model of the router.
- **Installer console design**:
  - Added top indentation and ANSI color highlighting for `[OK]`, `[ERROR]`, `[*]` statuses, links and separators.
  - Duplicate web interface address has been eliminated.

## [1.0.27] - 2026-09-03


### Dynamic loading of Changelog and optimization of modal update window
- **Automatically downloading a description of the new version from the repository**:
  - The backend and frontend now dynamically request the latest `CHANGELOG.md` from the remote GitHub repository when checking for updates.
  - The update window always displays the exact list of changes of the new available version, even if the previous version of the binary is installed on the router.

## [1.0.26] - 2026-09-03


### Improved web terminal and cross-architecture compatibility
- **Multi-architecture PTY support (ARM, AArch64, MIPS, x86_64)**:
  - Implemented cross-architectural enumeration of `ioctl` (`TIOCGPTN` / `TIOCSPTLCK`) codes and safe fallback when calling `Setctty`/`Setsid`.
  - Force interactive mode (`-i`) for all shells (`sh`, `ash`, `bash`), preventing instant session closure.
  - Atomic packaging of WebSocket frames and protective delays before closing the socket.
  - Improved diagnostics of WebSocket errors and fast Reconnect by pressing the Enter key.
- **Perfect formatting and indentation**:
  - Line breaks in the NDM CLI and Linux/SSH connection banners have been adjusted (neat single indentation before the version output and the command line prompt).

## [1.0.25] - 2026-09-03


### Improving fault tolerance of OPKG and install.sh installer
- **Built-in self-diagnosis and restoration of the OPKG (Auto-Healing) database**:
  - The `install.sh` script and `Smart-Utils` web interface automatically scan the `/opt/lib/opkg/status` package database and identify incomplete/corrupt installations of other packages (for example, `smart-route` or `smart-photo` with missing `.postinst` files).
  - Valid configuration script stubs are automatically generated, which prevents fatal OPKG errors with codes `127` (*postinst not found*) and `255`.
- **Auto-synchronization of repositories and seamless restart**:
  - Improved background polling of the repository and instant reboot of the interface after installing updates.

## [1.0.24] - 2026-09-03


### Automatic repository update & Seamless self-update
- **Fixed old version blinking when refreshing page (F5)**:
  - Removed obsolete hard-coded versions in `index.html` templates.
- **Background periodic synchronization of the repository**:
  - `Smart-Utils` automatically synchronizes the repository in the background every 30 minutes (`opkgMgr.StartBackgroundFeedSync`), and also forces a request for fresh data when opening the update window (`/api/version/check?refresh=true`). New updates now appear automatically without manually launching `opkg update`.
- **Instant and correct interface update after self-update**:
  - Once the installation of the `smart-utils` package is complete, the service immediately updates the version badge in the header, hides the available update icon, and performs a clean page reload.

## [1.0.23] - 2026-09-03


### Service Management: CPU Monitoring and Background Auto-Update
- **Indication of CPU and RAM load for each service**:
  - Integration of `ServicesManager` with `SystemAnalyzer` to accurately measure the actual CPU (`%`) and RAM (`RSS`) consumption of each running daemon and its child processes.
  - Service cards display interactive metric chips: `⚡ CPU: X.X%`, `💾 RAM: X.X MB` and `⏱️ PID: XXX`.
- **Background auto-update of service status**:
  - Added `Авто (3с)` switch with live pulsating indicator on the services panel.
  - Automatic smooth updating of process statuses and resource consumption without resetting focus or search filters when in a tab.

## [1.0.22] - 2026-09-03


### Disk Drives & Partition Deduplication
- **Clearing the list of disks and drives**:
  - The system firmware image `/` (`/dev/root` squashfs, 100% full), which is not a user drive, has been excluded.
  - Deduplication of file systems by `Device ID` has been implemented: duplication between `/opt`, UUID identifiers and clear volume labels has been eliminated.
  - Priority is given to custom partition names `/tmp/mnt/<Label>` (e.g. `/tmp/mnt/Opkg`, `/tmp/mnt/Seagate Expansion Drive`), preserving real devices (`/dev/sda2`, `/dev/sdb1`).
  - The block displays only real storages: `/tmp` (RAM), `/storage` (internal memory) and unique connected USB drives.

## [1.0.21] - 2026-09-03


### Disk Drives & Mounted Partitions /tmp/mnt/
- **Displays all connected USB drives and partitions**:
  - Added scanning and output of all `/tmp/mnt/*` mount points (USB drives, flash drives, external HDD/SSD in KeeneticOS), as well as the `/storage` partition (internal memory).
  - Improved display of partitions in the **"Disk Drives & Partitions"** block: added specialized icons (💽 USB drives, 📦 `/opt`, ⚡ `/storage`, 📁 root) with a visual progress bar and fill percentage.

## [1.0.20] - 2026-09-02


### Section “Thank the author” & Project support
- **New section “💖 Thank the author” (`#tab-donate`)**:
  - Located in the interface navigation for convenient voluntary development support.
  - Support for direct transfer through **T-Bank** ([tbank.ru/cf/4m4egy66JAy](https://www.tbank.ru/cf/4m4egy66JAy)) - transfer for fundraising without commission through SBP, cards and applications of any banks in the Russian Federation.
  - Support for transfers via **UMoney** (Russian bank cards MIR/Visa/Mastercard, SBP, T-Pay, SberPay, UMoney wallet `4100119618359414`).
  - Support for the **Boosty.to** service ([boosty.to/snake_lair/donate](https://boosty.to/snake_lair/donate)) - one-time donations and regular subscriptions from any bank cards in the world and the Russian Federation.
  - Buttons for quickly copying details (UMoney wallet, T-Bank and Boosty links) to the clipboard.
  - Quick links with a choice of a comfortable donation amount (150 ₽ ☕, 300 ₽ 🍕, 500 ₽ 🚀, 1000 ₽ 👑).
  - Map of the ecosystem of Smart line projects (**Smart-Route**, **Smart-Photo**, **Smart-Utils**) with links to repositories.



## [1.0.19] - 2026-08-28


### “Diagnostics” section & System self-diagnosis (System Doctor)
- **New section “🩺Diagnostics” (`#tab-diagnostics`)**:
  - Located in the navigation between **Journal** and **Settings**.
- **🩺 System self-diagnosis (System Doctor)**:
  - Automatic check of Keenetic kernel version, RAM/Swap memory, `/opt` section (Read-Write), OPKG environment and repository feeds, `/opt/etc/init.d/` service scripts, SSH and Web UI ports, DNS resolve and backup storage.
  - Summary with counters (`УСПЕШНО`, `ПРЕДУПРЕЖДЕНИЯ`, `ОШИБКИ`), button to copy the report to the clipboard for support and viewing kernel system outputs (Raw Outputs).
- **🌐 Network node checking tool (Diagnostic Prober)**:
  - Checking the availability of any Internet nodes, sites or IP ports (methods `AUTO`, `GET`, `HEAD`, `TCP`).
  - Quick testing presets (`google.com`, `icanhazip.com`, `github.com`, `repo.entware.net`, `cloudflare.com`, `1.1.1.1:53`).
  - Measuring delays (TCP handshake, TLS handshake, TTFB), determining TLS certificates, status codes, headers and response snippets.

## [1.0.18] - 2026-08-28


### Real-Time Live System Logs Terminal (SmartRoute Style)
- **Upgraded event log in SmartRoute style**:
  - Control panel: filtering by log level (`ALL`, `INFO`, `SUCCESS`, `WARN`, `ERROR`, `DEBUG`), live text search `input`.
  - **Autoscroll** checkbox, **Clear**, **Update** and **Download log** buttons (`.log` file).
  - Styled terminal strings `.log-line` with timestamp `log-ts`, level badge `log-lvl` and module tags `log-tag`.
  - The ring buffer has been increased to 1000 entries and API endpoints `POST /api/logs/clear` and `GET /api/logs/download` have been added.

## [1.0.17] - 2026-08-28


### Fix Web Bind Address
- **Removed extra IP binding parameter (Bind Address)**:
  - The server is always listening on all local interfaces `0.0.0.0`.
  - The field is hidden from the settings form to simplify configuration.

## [1.0.16] - 2026-08-28


### Update Indicator, Changelog and 1-Click Update
- **New version indicator in the header**:
  - An animated pulsating badge `⚡ Доступно обновление: vX.X.X` appears next to the current version number in the header if there is a more recent version in the repository.
- **Modal window with change history (Changelog)**:
  - Clicking on the indicator opens a dialog with a comparison of versions and a list of changes from the current version to the available one.
- **1-Click update directly from the header**:
  - The "🚀 Update Now" button triggers a secure package update via OPKG, displaying progress and automatically reloading the web page.

## [1.0.15] - 2026-08-28

### Dynamic Page Title with Router Model
- **Dynamic browser tab title**:
  - The page title has been updated to `Smart-Utils | Keenetic <Модель>` format (for example, `Smart-Utils | Keenetic Giga (KN-1011)`).

## [1.0.14] - 2026-08-28

### Multi-Column Settings Grid & Interactive Folder Picker (SmartPhoto Style)
- **Multi-column settings grid**:
  - The “Settings” section has been switched to an adaptive grid with cards: “Web interface and Network”, “Directories and Drives”, “Terminal and Logging”.
- **Interactive Folder Picker**:
  - Modal window with quick roots (`/opt`, `/tmp/mnt`, `/tmp`, `/media`, `/`), “Top” navigation and 1-click directory selection for the starting path of the file manager and backup directory.
- **Backend endpoint**: added lightweight route `GET /api/system/browse`.

## [1.0.13] - 2026-08-28

### Fix Navigation Tab Twitching & Scrollbar Overflow
- **Elimination of navigation button height jerking**:
  - A constant height `36px` and a constant frame `1px solid transparent; box-sizing: border-box` have been set to prevent the layout from shifting when switching tabs.
- **Elimination of horizontal scrollbar**:
  - The menu indents and the compact badge for the counter of available OPKG updates have been optimized.

## [1.0.12] - 2026-08-28

### Animated OPKG Loading State & URL Hash Tab Persistence on F5
- **Animation of loading the OPKG package catalog**:
  - An animated spinner with a description of the status and 6 flickering Skeleton Cards (shimmer effect).
- **URL Hash routing and saving tab with F5**:
  - Hash synchronization in URL (`#system`, `#files`, `#services`, `#terminal-cli`, `#terminal-ssh`, `#opkg`, `#backup`, `#logs`, `#settings`) and automatic re-opening when the page is refreshed.

## [1.0.11] - 2026-08-28

### Clean Trailing Control Characters & NUL Bytes in Router Model
- **System string sanitization**:
  - Clearing null bytes (`\x00`) and ASCII control characters from Device Tree (`/proc/device-tree/model`) on the backend and frontend.

## [1.0.10] - 2026-08-28

### Clean Semantic Package Version Comparison
- **Semantic comparison of package versions (`comparePkgVersions`)**:
  - The package is marked as requiring updating (`has_upgrade: true`) strictly under the condition `AvailableVersion > InstalledVersion`. False downgrade offers have been eliminated.

## [1.0.9] - 2026-08-28

### Remote Access Safe Self-Update
- **Secure smart-utils remote update**:
  - `prerm` does not stop the service during upgrade, and `postinst` starts a delayed background restart of the daemon (`sleep 2; restart &`).

## [1.0.0] - 2026-08-28

### First stable release
- **Web Terminal:** PTY/TTY console via WebSocket with support for ANSI colors and hotkeys.
- **Two-panel Total Commander:** hotkeys, built-in editor, archiver `.tar.gz`/`.zip`, `chmod`, Drag-and-Drop.
- **OPKG Manager:** feed management, 1-click repository presets, search and installation of packages.
- **CPU and system monitoring:** loading by core, RAM/Swap, disks, network interfaces, killing processes.
- **Backup and restore:** export of packages and configurations `/opt/etc/`.

