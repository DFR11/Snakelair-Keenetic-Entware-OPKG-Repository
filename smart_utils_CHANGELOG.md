# 📦 Smart-Utils Changelog

All important changes to the Smart-Utils project are documented in this file.

## [1.0.29] - 2026-09-03

### A full-fledged module for managing the Cron task scheduler
- **Managing the scheduler service (Crond)**:
  - Real-time monitoring of the `crond` service status, showing the PID and schedule file path.
  - Daemon control buttons: “Start”, “Stop”, “Restart”.
  - Automatic initialization of the `/opt/var/spool/cron/crontabs` environment and startup script on first launch.
- **Visual list and task cards**:
  - Toggle switches for instant enable/disable of tasks (commenting or uncommenting the line with `#`).
  - Human-readable translation of the schedule into English (`Every 5 minutes`, `Every day at 04:00`, `On weekdays`, `At every router boot (@reboot)`).
  - Quick copy of a command to the clipboard.
- **Interactive schedule designer and templates (Presets)**:
  - Quick selection of frequency (every minute, every 5/15/30 minutes, every hour, daily, weekly, monthly, @reboot or custom expression).
  - Catalog of ready-made system templates for Keenetic (cleaning `/tmp`, backing up settings, NTP time synchronization, updating Smart-Route lists, checking OPKG, watchdog, scheduled reboot).
- **Test run of the command (▶ Test)**:
  - Ability to run any task directly from the web panel and view console output, stdout/stderr, return code, and elapsed time.
- **Crontab Raw Editor**:
  - Tab for direct editing of the `crontab` file with syntax hints and validation.

## [1.0.28] - 2026-09-03

### Interactive installer and API validation
- **Interactive port selection**:
  - The `install.sh` installer requests the desired web interface port (default `8090`) and checks the previous router settings.
  - The port setting is automatically saved to the service configuration file.
- **Real API response check and synchronized restart**:
  - The installer restarts the service synchronously and polls `/api/status`, confirming the web panel is ready and showing the exact version and router model.
- **Installer console styling**:
  - Added top indentation and ANSI color highlighting for `[OK]`, `[ERROR]`, `[*]` statuses, links, and separators.
  - Duplicate web interface addresses were removed.

## [1.0.27] - 2026-09-03

### Dynamic loading of changelog and optimization of the update modal
- **Automatically downloading a description of the new version from the repository**:
  - The backend and frontend now dynamically request the latest `CHANGELOG.md` from the remote GitHub repository when checking for updates.
  - The update window always displays the exact list of changes of the newly available version, even if an older binary is installed on the router.

## [1.0.26] - 2026-09-03

### Improved web terminal and cross-architecture compatibility
- **Multi-architecture PTY support (ARM, AArch64, MIPS, x86_64)**:
  - Implemented cross-architectural enumeration of `ioctl` (`TIOCGPTN` / `TIOCSPTLCK`) codes and safe fallback when calling `Setctty`/`Setsid`.
  - Forced interactive mode (`-i`) for all shells (`sh`, `ash`, `bash`), preventing instant session closure.
  - Atomic packing of WebSocket frames and protective delays before closing the socket.
  - Improved WebSocket error diagnostics and fast reconnect on Enter.
- **Perfect formatting and indentation**:
  - Line breaks in NDM CLI and Linux/SSH connection banners were adjusted (clean single indentation before the version output and command prompt).

## [1.0.25] - 2026-09-03

### Improving fault tolerance of OPKG and the install.sh installer
- **Built-in self-diagnosis and repair of the OPKG database (Auto-Healing)**:
  - The `install.sh` script and Smart-Utils web interface scan the `/opt/lib/opkg/status` package database and detect incomplete or damaged installations of other packages.
  - Valid stub config scripts are generated automatically, preventing fatal OPKG errors with codes `127` (postinst not found) and `255`.
- **Repository auto-synchronization and seamless restart**:
  - Improved background polling of the repository and instant interface reboot after installing updates.

## [1.0.24] - 2026-09-03

### Automatic repository update & seamless self-update
- **Fixed old version flicker when refreshing the page (F5)**:
  - Removed obsolete hard-coded versions in `index.html` templates.
- **Background periodic repository synchronization**:
  - Smart-Utils automatically synchronizes the repository in the background every 30 minutes (`opkgMgr.StartBackgroundFeedSync`), and also forces a fresh data request when opening the update modal.
- **Instant and correct interface update after self-update**:
  - Once the installation of the `smart-utils` package is complete, the service immediately updates the version badge in the header, hides the update icon, and performs a clean page reload.

## [1.0.23] - 2026-09-03

### Service management: CPU monitoring and background auto-update
- **CPU and RAM load indication for each service**:
  - Integrated `ServicesManager` with `SystemAnalyzer` to measure actual CPU (`%`) and RAM (`RSS`) usage of each running daemon and its child processes.
  - Service cards display interactive metric chips: `⚡ CPU: X.X%`, `💾 RAM: X.X MB`, and `⏱️ PID: XXX`.
- **Background auto-update of service status**:
  - Added the `Auto (3s)` toggle with a live pulsing indicator on the service panel.
  - Automatic smooth updates of process statuses and resource usage without losing focus or search filters when switching tabs.

## [1.0.22] - 2026-09-03

### Disk drives & partition deduplication
- **Clearing the list of disks and drives**:
  - The system firmware image `/` (`/dev/root` squashfs, 100% full) was excluded as it is not a user drive.
  - Deduplication of file systems by device ID was implemented; duplicates between `/opt`, UUID identifiers, and labels were eliminated.
  - Priority is given to custom partition names `/tmp/mnt/<Label>` (for example `/tmp/mnt/Opkg`, `/tmp/mnt/Seagate Expansion Drive`), while preserving real devices (`/dev/sda2`, `/dev/sdb1`).
  - The panel displays only real storage: `/tmp`, `/storage`, and unique connected USB drives.

## [1.0.21] - 2026-09-03

### Disk drives & mounted partitions /tmp/mnt/
- **Display all connected USB drives and partitions**:
  - Added scanning and output of all `/tmp/mnt/*` mount points (USB drives, flash drives, external HDD/SSD in KeeneticOS), as well as the `/storage` partition (internal memory).
  - Improved display of partitions in the **Disk Drives & Partitions** block: specialized icons (💽 USB drives, 📦 `/opt`, ⚡ `/storage`, 📁 root) and a visual progress bar were added.

## [1.0.20] - 2026-09-02

### Section “Thank the author” & project support
- **New section “💖 Thank the author” (`#tab-donate`)**:
  - Located in the interface navigation for convenient voluntary project support.
  - Support for direct transfers through **T-Bank** and **UMoney**, plus **Boosty** subscriptions or one-time donations.
  - Buttons for quickly copying account details to the clipboard.
  - Quick links with a choice of comfortable donation amounts.
  - Map of the Smart ecosystem projects (**Smart-Route**, **Smart-Photo**, **Smart-Utils**) with links to repositories.

## [1.0.19] - 2026-08-28

### “Diagnostics” section & system self-diagnosis (System Doctor)
- **New section “🩺 Diagnostics” (`#tab-diagnostics`)**:
  - Located in the navigation between **Journal** and **Settings**.
- **🩺 System self-diagnosis (System Doctor)**:
  - Automatic check of Keenetic kernel version, RAM/Swap memory, `/opt` mount point (read-write), OPKG environment and repository feeds, `/opt/etc/init.d/` service scripts, SSH and Web UI ports, and DNS.
  - Summary counters (`SUCCESS`, `WARNINGS`, `ERRORS`), plus a button to copy the report for support and view kernel system outputs.
- **🌐 Network node checking tool (Diagnostic Prober)**:
  - Checks availability of any Internet nodes, sites, or IP ports (AUTO, GET, HEAD, TCP).
  - Quick test presets (`google.com`, `icanhazip.com`, `github.com`, `repo.entware.net`, `cloudflare.com`, `1.1.1.1:53`).
  - Measures delay (TCP handshake, TLS handshake, TTFB), determines TLS certificates, status codes, headers, and response snippets.

## [1.0.18] - 2026-08-28

### Real-time live system logs terminal (SmartRoute style)
- **Upgraded event log in SmartRoute style**:
  - Control panel with log-level filtering (`ALL`, `INFO`, `SUCCESS`, `WARN`, `ERROR`, `DEBUG`) and live text search.
  - **Autoscroll**, **Clear**, **Update**, and **Download log** buttons.
  - Styled terminal strings `.log-line` with timestamps, level badges, and module tags.
  - Ring buffer increased to 1000 entries and API endpoints `POST /api/logs/clear` and `GET /api/logs/download` were added.

## [1.0.17] - 2026-08-28

### Fix Web Bind Address
- **Removed extra IP binding parameter (Bind Address)**:
  - The server always listens on all local interfaces `0.0.0.0`.
  - The field was hidden from the settings form to simplify configuration.

## [1.0.16] - 2026-08-28

### Update indicator, changelog, and one-click update
- **New version indicator in the header**:
  - An animated pulsing badge `⚡ Update available: vX.X.X` appears next to the current version number in the header if a newer version is in the repository.
- **Modal window with changelog**:
  - Clicking the indicator opens a dialog with a comparison of versions and a list of changes from the current version to the available one.
- **1-click update directly from the header**:
  - The “🚀 Update Now” button triggers a secure package update via OPKG, shows progress, and automatically reloads the page.

## [1.0.15] - 2026-08-28

### Dynamic page title with router model
- **Dynamic browser tab title**:
  - The page title was updated to `Smart-Utils | Keenetic <Model>` (for example, `Smart-Utils | Keenetic Giga (KN-1011)`).

## [1.0.14] - 2026-08-28

### Multi-column settings grid & interactive folder picker (SmartPhoto style)
- **Multi-column settings grid**:
  - The “Settings” section was switched to an adaptive grid with cards: “Web Interface and Network”, “Directories and Drives”, “Terminal and Logging”.
- **Interactive Folder Picker**:
  - Modal window with quick roots (`/opt`, `/tmp/mnt`, `/tmp`, `/media`, `/`), “Top” navigation, and one-click directory selection.
- **Backend endpoint**: added a lightweight route `GET /api/system/browse`.

## [1.0.13] - 2026-08-28

### Fix navigation tab twitching & scrollbar overflow
- **Eliminated navigation button height jerking**:
  - A constant height `36px` and constant frame `1px solid transparent; box-sizing: border-box` were set to prevent layout shifting when switching tabs.
- **Eliminated horizontal scrollbar**:
  - The menu indents and compact badge for available OPKG updates were optimized.

## [1.0.12] - 2026-08-28

### Animated OPKG loading state & URL hash tab persistence on F5
- **Animation of the OPKG loading state**:
  - An animated spinner with status description and 6 flickering skeleton cards (shimmer effect).
- **URL hash routing and saved tab state on F5**:
  - Hash synchronization in the URL (`#system`, `#files`, `#services`, `#terminal-cli`, `#terminal-ssh`, `#opkg`, `#backup`, `#logs`, `#settings`) and auto-reopen on refresh.

## [1.0.11] - 2026-08-28

### Clean trailing control characters & NUL bytes in router model
- **System string sanitization**:
  - Cleared null bytes (`\x00`) and ASCII control characters from Device Tree (`/proc/device-tree/model`) on the backend and frontend.

## [1.0.10] - 2026-08-28

### Clean semantic package version comparison
- **Semantic comparison of package versions (`comparePkgVersions`)**:
  - The package is marked for update only if `AvailableVersion > InstalledVersion`. False downgrade offers were eliminated.

## [1.0.9] - 2026-08-28

### Remote access safe self-update
- **Secure smart-utils remote update**:
  - `prerm` does not stop the service during the upgrade, and `postinst` starts a delayed background restart of the daemon (`sleep 2; restart &`).

## [1.0.0] - 2026-08-28

### First stable release
- **Web terminal:** PTY/TTY console via WebSocket with support for ANSI colors and hotkeys.
- **Two-panel Total Commander:** hotkeys, built-in editor, archive `.tar.gz`/`.zip`, `chmod`, drag-and-drop.
- **OPKG Manager:** feed management, one-click repository presets, search and installation of packages.
- **CPU and system monitoring:** load by core, RAM/Swap, disks, network interfaces, process kill.
- **Backup and restore:** export packages and configs from `/opt/etc/`.
